#!/usr/bin/env python3
"""Tailscale-only, read-only JSON API for PLA historical traffic graphs."""

from __future__ import annotations

import argparse
import configparser
import json
import logging
import sqlite3
import sys
from datetime import datetime, timezone
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, urlparse


LOG = logging.getLogger("pla-traffic-api")
UTC = timezone.utc
API_VERSION = "1.0"

INTERVALS = {
    "hour": {
        "source": "hourly_traffic",
        "period": "hour_utc",
        "latency": "origin_response_avg_ms",
        "sampled": "is_sampled",
    },
    "day": {
        "source": "traffic_daily",
        "period": "period_start_utc",
        "latency": "origin_response_weighted_avg_ms",
        "sampled": "contains_sampled_data",
    },
    "week": {
        "source": "traffic_weekly",
        "period": "period_start_utc",
        "latency": "origin_response_weighted_avg_ms",
        "sampled": "contains_sampled_data",
    },
    "month": {
        "source": "traffic_monthly",
        "period": "period_start_utc",
        "latency": "origin_response_weighted_avg_ms",
        "sampled": "contains_sampled_data",
    },
    "year": {
        "source": "traffic_yearly",
        "period": "period_start_utc",
        "latency": "origin_response_weighted_avg_ms",
        "sampled": "contains_sampled_data",
    },
}

SUM_FIELDS = (
    "requests",
    "visits",
    "edge_request_bytes",
    "edge_response_bytes",
    "cached_requests",
    "uncached_requests",
    "origin_requests",
    "cached_response_bytes",
    "uncached_response_bytes",
    "blocked_requests",
    "status_4xx",
    "status_5xx",
)


class ApiError(ValueError):
    pass


def read_config(path: Path) -> dict[str, Any]:
    parser = configparser.ConfigParser()
    if not parser.read(path):
        raise ApiError(f"configuration file not found: {path}")
    config = {
        "bind_address": parser.get("api", "bind_address"),
        "port": parser.getint("api", "port", fallback=9468),
        "database_path": Path(parser.get("api", "database_path")),
        "max_rows": parser.getint("api", "max_rows", fallback=5000),
    }
    if not 1 <= config["port"] <= 65535:
        raise ApiError("port must be between 1 and 65535")
    if config["max_rows"] < 1:
        raise ApiError("max_rows must be positive")
    return config


def connect_read_only(path: Path) -> sqlite3.Connection:
    if not path.is_file():
        raise ApiError("published traffic snapshot is unavailable")
    uri = f"file:{path}?mode=ro&immutable=1"
    connection = sqlite3.connect(uri, uri=True, timeout=5)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA query_only = ON")
    return connection


def parse_boundary(value: str | None, name: str) -> str | None:
    if not value:
        return None
    candidate = value.strip()
    try:
        parsed = datetime.fromisoformat(candidate.replace("Z", "+00:00"))
    except ValueError as error:
        raise ApiError(f"invalid {name} timestamp") from error
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise ApiError(f"{name} timestamp must include a timezone")
    return parsed.astimezone(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def validate_range(start: str | None, end: str | None) -> None:
    if start and end and start >= end:
        raise ApiError("start timestamp must be earlier than end timestamp")


def available_hostnames(connection: sqlite3.Connection) -> set[str]:
    return {row[0] for row in connection.execute("SELECT DISTINCT hostname FROM hourly_traffic")}


def validate_hostname(connection: sqlite3.Connection, hostname: str) -> str:
    hostname = hostname.strip().lower()
    if hostname == "all":
        return hostname
    if hostname not in available_hostnames(connection):
        raise ApiError("unknown hostname")
    return hostname


def query_series(
    connection: sqlite3.Connection,
    interval: str,
    hostname: str,
    start: str | None,
    end: str | None,
    max_rows: int,
) -> list[dict[str, Any]]:
    if interval not in INTERVALS:
        raise ApiError("interval must be hour, day, week, month, or year")
    spec = INTERVALS[interval]
    source = spec["source"]
    period = spec["period"]
    latency = spec["latency"]
    sampled = spec["sampled"]
    hostname = validate_hostname(connection, hostname)

    where: list[str] = []
    parameters: list[Any] = []
    if hostname != "all":
        where.append("hostname = ?")
        parameters.append(hostname)
    if start:
        where.append(f"{period} >= ?")
        parameters.append(start)
    if end:
        where.append(f"{period} < ?")
        parameters.append(end)
    where_sql = " WHERE " + " AND ".join(where) if where else ""
    sums = ", ".join(f"SUM({field}) AS {field}" for field in SUM_FIELDS)
    query = f"""
        SELECT {period} AS period_start_utc,
               {sums},
               CASE WHEN SUM(origin_requests) > 0
                    THEN SUM(COALESCE({latency}, 0) * origin_requests) / SUM(origin_requests)
               END AS origin_response_weighted_avg_ms,
               MAX({sampled}) AS contains_sampled_data
          FROM {source}
          {where_sql}
         GROUP BY {period}
         ORDER BY {period}
         LIMIT ?
    """
    parameters.append(max_rows + 1)
    rows = [dict(row) for row in connection.execute(query, parameters)]
    if len(rows) > max_rows:
        raise ApiError("requested series exceeds maximum row count; narrow the time range")
    return rows


def query_summary(
    connection: sqlite3.Connection,
    hostname: str,
    start: str | None,
    end: str | None,
) -> dict[str, Any]:
    hostname = validate_hostname(connection, hostname)
    where: list[str] = []
    parameters: list[Any] = []
    if hostname != "all":
        where.append("hostname = ?")
        parameters.append(hostname)
    if start:
        where.append("hour_utc >= ?")
        parameters.append(start)
    if end:
        where.append("hour_utc < ?")
        parameters.append(end)
    where_sql = " WHERE " + " AND ".join(where) if where else ""
    sums = ", ".join(f"COALESCE(SUM({field}), 0) AS {field}" for field in SUM_FIELDS)
    query = f"""
        SELECT {sums},
               MIN(hour_utc) AS earliest_hour_utc,
               MAX(hour_utc) AS latest_hour_utc,
               CASE WHEN SUM(origin_requests) > 0
                    THEN SUM(COALESCE(origin_response_avg_ms, 0) * origin_requests) / SUM(origin_requests)
               END AS origin_response_weighted_avg_ms,
               COALESCE(MAX(is_sampled), 0) AS contains_sampled_data
          FROM hourly_traffic
          {where_sql}
    """
    return dict(connection.execute(query, parameters).fetchone())


def query_health(connection: sqlite3.Connection) -> dict[str, Any]:
    row = connection.execute(
        """
        SELECT COUNT(*) AS rows,
               MIN(hour_utc) AS earliest_hour_utc,
               MAX(hour_utc) AS latest_hour_utc,
               MAX(collected_at_utc) AS last_collected_at_utc
          FROM hourly_traffic
        """
    ).fetchone()
    check = connection.execute("PRAGMA quick_check").fetchone()[0]
    return {
        "status": "ok" if check == "ok" else "error",
        "api_version": API_VERSION,
        "storage_timezone": "UTC",
        "database_integrity": check,
        **dict(row),
    }


def handler_factory(database_path: Path, max_rows: int):
    class Handler(BaseHTTPRequestHandler):
        server_version = "PLA-Traffic-API/1.0"
        sys_version = ""

        def log_message(self, fmt: str, *args: Any) -> None:
            LOG.info("%s - %s", self.client_address[0], fmt % args)

        def send_json(self, status: HTTPStatus, payload: dict[str, Any]) -> None:
            body = json.dumps(payload, separators=(",", ":"), sort_keys=True).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.send_header("X-Content-Type-Options", "nosniff")
            self.end_headers()
            self.wfile.write(body)

        def do_GET(self) -> None:
            parsed = urlparse(self.path)
            parameters = parse_qs(parsed.query, keep_blank_values=False)
            try:
                with connect_read_only(database_path) as connection:
                    if parsed.path == "/health":
                        payload = query_health(connection)
                    elif parsed.path == "/v1/summary":
                        hostname = parameters.get("hostname", ["all"])[0].strip().lower()
                        start = parse_boundary(parameters.get("start", [None])[0], "start")
                        end = parse_boundary(parameters.get("end", [None])[0], "end")
                        validate_range(start, end)
                        payload = {
                            "hostname": hostname,
                            "start": start,
                            "end": end,
                            "summary": query_summary(connection, hostname, start, end),
                        }
                    elif parsed.path == "/v1/series":
                        interval = parameters.get("interval", ["day"])[0]
                        hostname = parameters.get("hostname", ["all"])[0].strip().lower()
                        start = parse_boundary(parameters.get("start", [None])[0], "start")
                        end = parse_boundary(parameters.get("end", [None])[0], "end")
                        validate_range(start, end)
                        payload = {
                            "interval": interval,
                            "hostname": hostname,
                            "start": start,
                            "end": end,
                            "points": query_series(connection, interval, hostname, start, end, max_rows),
                        }
                    else:
                        self.send_json(HTTPStatus.NOT_FOUND, {"error": "not found"})
                        return
                self.send_json(HTTPStatus.OK, payload)
            except ApiError as error:
                self.send_json(HTTPStatus.BAD_REQUEST, {"error": str(error)})
            except Exception:
                LOG.exception("request failed")
                self.send_json(HTTPStatus.INTERNAL_SERVER_ERROR, {"error": "internal error"})

    return Handler


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=Path("/etc/pla-api/traffic-api.conf"))
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    try:
        config = read_config(args.config)
        handler = handler_factory(config["database_path"], config["max_rows"])
        server = ThreadingHTTPServer((config["bind_address"], config["port"]), handler)
        LOG.info("Listening on %s:%d", config["bind_address"], config["port"])
        server.serve_forever()
        return 0
    except KeyboardInterrupt:
        return 0
    except Exception as error:
        LOG.error("%s", error)
        return 1


if __name__ == "__main__":
    sys.exit(main())
