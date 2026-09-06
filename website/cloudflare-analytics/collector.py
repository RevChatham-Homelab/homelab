#!/usr/bin/env python3
"""Durable Cloudflare edge-traffic collector for Project Liquid Alert."""

from __future__ import annotations

import argparse
import configparser
import grp
import json
import logging
import os
import random
import sqlite3
import sys
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Iterable


LOG = logging.getLogger("pla-cloudflare-analytics")
UTC = timezone.utc
SCHEMA_VERSION = "1"
COLLECTOR_VERSION = "1.1.1"
CACHED_REQUEST_STATUSES = {"hit", "stale", "updating", "ignored"}
CACHED_BYTE_STATUSES = CACHED_REQUEST_STATUSES | {"revalidated"}
BLOCK_ACTIONS = {"block"}


class CollectorError(RuntimeError):
    pass


@dataclass(frozen=True)
class Settings:
    zone_id: str
    account_id: str
    hostnames: tuple[str, ...]
    api_url: str
    request_source: str
    database_path: Path
    timezone_name: str
    settlement_delay_minutes: int
    overlap_hours: int
    request_timeout_seconds: int
    retry_attempts: int
    retry_base_seconds: float
    backup_dir: Path
    backup_retention_count: int
    api_snapshot_path: Path
    api_snapshot_group: str


SETTINGS_QUERY = """
query Limits($zoneTag: string) {
  viewer {
    zones(filter: {zoneTag: $zoneTag}) {
      settings {
        httpRequestsAdaptiveGroups {
          enabled
          availableFields
          maxDuration
          maxNumberOfFields
          maxPageSize
          notOlderThan
        }
      }
    }
  }
}
"""


TRAFFIC_QUERY = """
query HourlyTraffic($zoneTag: string, $filter: filter) {
  viewer {
    zones(filter: {zoneTag: $zoneTag}) {
      totals: httpRequestsAdaptiveGroups(limit: 10000, filter: $filter) {
        count
        avg {
          sampleInterval
          originResponseDurationMs
        }
        quantiles {
          originResponseDurationMsP50
          originResponseDurationMsP95
          originResponseDurationMsP99
        }
        sum {
          visits
          edgeRequestBytes
          edgeResponseBytes
        }
        dimensions {
          datetimeHour
        }
      }
      cache: httpRequestsAdaptiveGroups(limit: 10000, filter: $filter) {
        count
        sum {
          edgeResponseBytes
        }
        dimensions {
          datetimeHour
          cacheStatus
        }
      }
      statuses: httpRequestsAdaptiveGroups(limit: 10000, filter: $filter) {
        count
        dimensions {
          datetimeHour
          edgeResponseStatus
        }
      }
      security: httpRequestsAdaptiveGroups(limit: 10000, filter: $filter) {
        count
        dimensions {
          datetimeHour
          securityAction
        }
      }
      origin: httpRequestsAdaptiveGroups(limit: 10000, filter: $filter) {
        count
        dimensions {
          datetimeHour
          originResponseStatus
        }
      }
    }
  }
}
"""


REQUIRED_FIELDS = {
    "count",
    "avg_sampleInterval",
    "avg_originResponseDurationMs",
    "quantiles_originResponseDurationMsP50",
    "quantiles_originResponseDurationMsP95",
    "quantiles_originResponseDurationMsP99",
    "sum_visits",
    "sum_edgeRequestBytes",
    "sum_edgeResponseBytes",
    "dimensions_datetimeHour",
    "dimensions_cacheStatus",
    "dimensions_edgeResponseStatus",
    "dimensions_securityAction",
    "dimensions_originResponseStatus",
}


SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS metadata (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL,
    updated_at_utc TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS hourly_traffic (
    hour_utc TEXT NOT NULL,
    hostname TEXT NOT NULL,
    requests INTEGER NOT NULL DEFAULT 0 CHECK (requests >= 0),
    visits INTEGER NOT NULL DEFAULT 0 CHECK (visits >= 0),
    edge_request_bytes INTEGER NOT NULL DEFAULT 0 CHECK (edge_request_bytes >= 0),
    edge_response_bytes INTEGER NOT NULL DEFAULT 0 CHECK (edge_response_bytes >= 0),
    cached_requests INTEGER NOT NULL DEFAULT 0 CHECK (cached_requests >= 0),
    uncached_requests INTEGER NOT NULL DEFAULT 0 CHECK (uncached_requests >= 0),
    origin_requests INTEGER NOT NULL DEFAULT 0 CHECK (origin_requests >= 0),
    cached_response_bytes INTEGER NOT NULL DEFAULT 0 CHECK (cached_response_bytes >= 0),
    uncached_response_bytes INTEGER NOT NULL DEFAULT 0 CHECK (uncached_response_bytes >= 0),
    blocked_requests INTEGER NOT NULL DEFAULT 0 CHECK (blocked_requests >= 0),
    status_4xx INTEGER NOT NULL DEFAULT 0 CHECK (status_4xx >= 0),
    status_5xx INTEGER NOT NULL DEFAULT 0 CHECK (status_5xx >= 0),
    origin_response_avg_ms REAL,
    origin_response_p50_ms REAL,
    origin_response_p95_ms REAL,
    origin_response_p99_ms REAL,
    sample_interval REAL NOT NULL DEFAULT 1.0 CHECK (sample_interval >= 1.0),
    is_sampled INTEGER NOT NULL DEFAULT 0 CHECK (is_sampled IN (0, 1)),
    source_dataset TEXT NOT NULL DEFAULT 'httpRequestsAdaptiveGroups',
    collected_at_utc TEXT NOT NULL,
    PRIMARY KEY (hour_utc, hostname),
    CHECK (substr(hour_utc, 18, 2) = '00' AND substr(hour_utc, 20, 1) = 'Z')
) WITHOUT ROWID;

CREATE INDEX IF NOT EXISTS idx_hourly_traffic_hostname_hour
    ON hourly_traffic(hostname, hour_utc);

CREATE TABLE IF NOT EXISTS collection_runs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    started_at_utc TEXT NOT NULL,
    finished_at_utc TEXT,
    status TEXT NOT NULL CHECK (status IN ('running', 'success', 'failed')),
    range_start_utc TEXT,
    range_end_utc TEXT,
    api_requests INTEGER NOT NULL DEFAULT 0,
    rows_upserted INTEGER NOT NULL DEFAULT 0,
    error_message TEXT
);

CREATE VIEW IF NOT EXISTS traffic_daily AS
SELECT
    substr(hour_utc, 1, 10) AS period_start_utc,
    hostname,
    SUM(requests) AS requests,
    SUM(visits) AS visits,
    SUM(edge_request_bytes) AS edge_request_bytes,
    SUM(edge_response_bytes) AS edge_response_bytes,
    SUM(cached_requests) AS cached_requests,
    SUM(uncached_requests) AS uncached_requests,
    SUM(origin_requests) AS origin_requests,
    SUM(cached_response_bytes) AS cached_response_bytes,
    SUM(uncached_response_bytes) AS uncached_response_bytes,
    SUM(blocked_requests) AS blocked_requests,
    SUM(status_4xx) AS status_4xx,
    SUM(status_5xx) AS status_5xx,
    CASE WHEN SUM(origin_requests) > 0
         THEN SUM(COALESCE(origin_response_avg_ms, 0) * origin_requests) / SUM(origin_requests)
    END AS origin_response_weighted_avg_ms,
    MAX(is_sampled) AS contains_sampled_data
FROM hourly_traffic
GROUP BY substr(hour_utc, 1, 10), hostname;

CREATE VIEW IF NOT EXISTS traffic_weekly AS
SELECT
    date(hour_utc, '-' || ((CAST(strftime('%w', hour_utc) AS INTEGER) + 6) % 7) || ' days') AS period_start_utc,
    hostname,
    SUM(requests) AS requests,
    SUM(visits) AS visits,
    SUM(edge_request_bytes) AS edge_request_bytes,
    SUM(edge_response_bytes) AS edge_response_bytes,
    SUM(cached_requests) AS cached_requests,
    SUM(uncached_requests) AS uncached_requests,
    SUM(origin_requests) AS origin_requests,
    SUM(cached_response_bytes) AS cached_response_bytes,
    SUM(uncached_response_bytes) AS uncached_response_bytes,
    SUM(blocked_requests) AS blocked_requests,
    SUM(status_4xx) AS status_4xx,
    SUM(status_5xx) AS status_5xx,
    CASE WHEN SUM(origin_requests) > 0
         THEN SUM(COALESCE(origin_response_avg_ms, 0) * origin_requests) / SUM(origin_requests)
    END AS origin_response_weighted_avg_ms,
    MAX(is_sampled) AS contains_sampled_data
FROM hourly_traffic
GROUP BY period_start_utc, hostname;

CREATE VIEW IF NOT EXISTS traffic_monthly AS
SELECT
    substr(hour_utc, 1, 7) || '-01' AS period_start_utc,
    hostname,
    SUM(requests) AS requests,
    SUM(visits) AS visits,
    SUM(edge_request_bytes) AS edge_request_bytes,
    SUM(edge_response_bytes) AS edge_response_bytes,
    SUM(cached_requests) AS cached_requests,
    SUM(uncached_requests) AS uncached_requests,
    SUM(origin_requests) AS origin_requests,
    SUM(cached_response_bytes) AS cached_response_bytes,
    SUM(uncached_response_bytes) AS uncached_response_bytes,
    SUM(blocked_requests) AS blocked_requests,
    SUM(status_4xx) AS status_4xx,
    SUM(status_5xx) AS status_5xx,
    CASE WHEN SUM(origin_requests) > 0
         THEN SUM(COALESCE(origin_response_avg_ms, 0) * origin_requests) / SUM(origin_requests)
    END AS origin_response_weighted_avg_ms,
    MAX(is_sampled) AS contains_sampled_data
FROM hourly_traffic
GROUP BY substr(hour_utc, 1, 7), hostname;

CREATE VIEW IF NOT EXISTS traffic_yearly AS
SELECT
    substr(hour_utc, 1, 4) || '-01-01' AS period_start_utc,
    hostname,
    SUM(requests) AS requests,
    SUM(visits) AS visits,
    SUM(edge_request_bytes) AS edge_request_bytes,
    SUM(edge_response_bytes) AS edge_response_bytes,
    SUM(cached_requests) AS cached_requests,
    SUM(uncached_requests) AS uncached_requests,
    SUM(origin_requests) AS origin_requests,
    SUM(cached_response_bytes) AS cached_response_bytes,
    SUM(uncached_response_bytes) AS uncached_response_bytes,
    SUM(blocked_requests) AS blocked_requests,
    SUM(status_4xx) AS status_4xx,
    SUM(status_5xx) AS status_5xx,
    CASE WHEN SUM(origin_requests) > 0
         THEN SUM(COALESCE(origin_response_avg_ms, 0) * origin_requests) / SUM(origin_requests)
    END AS origin_response_weighted_avg_ms,
    MAX(is_sampled) AS contains_sampled_data
FROM hourly_traffic
GROUP BY substr(hour_utc, 1, 4), hostname;
"""


UPSERT_SQL = """
INSERT INTO hourly_traffic (
    hour_utc, hostname, requests, visits, edge_request_bytes, edge_response_bytes,
    cached_requests, uncached_requests, origin_requests,
    cached_response_bytes, uncached_response_bytes, blocked_requests,
    status_4xx, status_5xx, origin_response_avg_ms, origin_response_p50_ms,
    origin_response_p95_ms, origin_response_p99_ms, sample_interval, is_sampled,
    source_dataset, collected_at_utc
) VALUES (
    :hour_utc, :hostname, :requests, :visits, :edge_request_bytes, :edge_response_bytes,
    :cached_requests, :uncached_requests, :origin_requests,
    :cached_response_bytes, :uncached_response_bytes, :blocked_requests,
    :status_4xx, :status_5xx, :origin_response_avg_ms, :origin_response_p50_ms,
    :origin_response_p95_ms, :origin_response_p99_ms, :sample_interval, :is_sampled,
    :source_dataset, :collected_at_utc
)
ON CONFLICT(hour_utc, hostname) DO UPDATE SET
    requests = excluded.requests,
    visits = excluded.visits,
    edge_request_bytes = excluded.edge_request_bytes,
    edge_response_bytes = excluded.edge_response_bytes,
    cached_requests = excluded.cached_requests,
    uncached_requests = excluded.uncached_requests,
    origin_requests = excluded.origin_requests,
    cached_response_bytes = excluded.cached_response_bytes,
    uncached_response_bytes = excluded.uncached_response_bytes,
    blocked_requests = excluded.blocked_requests,
    status_4xx = excluded.status_4xx,
    status_5xx = excluded.status_5xx,
    origin_response_avg_ms = excluded.origin_response_avg_ms,
    origin_response_p50_ms = excluded.origin_response_p50_ms,
    origin_response_p95_ms = excluded.origin_response_p95_ms,
    origin_response_p99_ms = excluded.origin_response_p99_ms,
    sample_interval = excluded.sample_interval,
    is_sampled = excluded.is_sampled,
    source_dataset = excluded.source_dataset,
    collected_at_utc = excluded.collected_at_utc;
"""


def utc_now() -> datetime:
    return datetime.now(UTC)


def iso_utc(value: datetime) -> str:
    return value.astimezone(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def parse_utc(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(UTC)


def floor_hour(value: datetime) -> datetime:
    return value.astimezone(UTC).replace(minute=0, second=0, microsecond=0)


def ceil_hour(value: datetime) -> datetime:
    floored = floor_hour(value)
    return floored if value == floored else floored + timedelta(hours=1)


def hour_range(start: datetime, end: datetime) -> Iterable[datetime]:
    current = floor_hour(start)
    while current < end:
        yield current
        current += timedelta(hours=1)


def read_settings(path: Path) -> Settings:
    parser = configparser.ConfigParser()
    if not parser.read(path):
        raise CollectorError(f"configuration file not found or unreadable: {path}")

    hostnames = tuple(
        item.strip().lower()
        for item in parser.get("cloudflare", "hostnames").split(",")
        if item.strip()
    )
    if not hostnames:
        raise CollectorError("at least one hostname is required")

    timezone_name = parser.get("storage", "timezone", fallback="UTC")
    if timezone_name.upper() != "UTC":
        raise CollectorError("storage timezone must be UTC")

    return Settings(
        zone_id=parser.get("cloudflare", "zone_id").strip(),
        account_id=parser.get("cloudflare", "account_id").strip(),
        hostnames=hostnames,
        api_url=parser.get("cloudflare", "api_url").strip(),
        request_source=parser.get("cloudflare", "request_source", fallback="eyeball").strip(),
        database_path=Path(parser.get("storage", "database_path")).expanduser(),
        timezone_name="UTC",
        settlement_delay_minutes=parser.getint("collection", "settlement_delay_minutes", fallback=15),
        overlap_hours=parser.getint("collection", "overlap_hours", fallback=6),
        request_timeout_seconds=parser.getint("collection", "request_timeout_seconds", fallback=30),
        retry_attempts=parser.getint("collection", "retry_attempts", fallback=5),
        retry_base_seconds=parser.getfloat("collection", "retry_base_seconds", fallback=2.0),
        backup_dir=Path(parser.get("backup", "directory", fallback="/var/backups/pla-analytics")),
        backup_retention_count=parser.getint("backup", "retention_count", fallback=14),
        api_snapshot_path=Path(
            parser.get(
                "api",
                "snapshot_path",
                fallback="/var/lib/pla-api/traffic.sqlite",
            )
        ),
        api_snapshot_group=parser.get("api", "snapshot_group", fallback="pla-analytics-api"),
    )


class CloudflareClient:
    def __init__(self, settings: Settings, token: str):
        if not token:
            raise CollectorError("CLOUDFLARE_API_TOKEN is not set")
        self.settings = settings
        self._token = token
        self.request_count = 0

    def query(self, query: str, variables: dict[str, Any]) -> dict[str, Any]:
        payload = json.dumps({"query": query, "variables": variables}).encode("utf-8")
        last_error: Exception | None = None

        for attempt in range(1, self.settings.retry_attempts + 1):
            request = urllib.request.Request(
                self.settings.api_url,
                data=payload,
                headers={
                    "Authorization": f"Bearer {self._token}",
                    "Accept": "application/json",
                    "Content-Type": "application/json",
                    "User-Agent": f"PLA-Cloudflare-Analytics/{COLLECTOR_VERSION}",
                },
                method="POST",
            )
            self.request_count += 1
            try:
                with urllib.request.urlopen(
                    request, timeout=self.settings.request_timeout_seconds
                ) as response:
                    result = json.load(response)
                errors = result.get("errors") or []
                if errors:
                    messages = "; ".join(str(item.get("message", "GraphQL error")) for item in errors)
                    raise CollectorError(f"Cloudflare GraphQL error: {messages[:1000]}")
                return result
            except urllib.error.HTTPError as error:
                body = error.read(4096).decode("utf-8", errors="replace")
                last_error = CollectorError(f"Cloudflare HTTP {error.code}: {body[:1000]}")
                retryable = error.code == 429 or 500 <= error.code <= 599
                if not retryable:
                    raise last_error
                retry_after = error.headers.get("Retry-After")
                delay = float(retry_after) if retry_after and retry_after.isdigit() else None
            except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as error:
                last_error = error
                delay = None

            if attempt >= self.settings.retry_attempts:
                break
            if delay is None:
                delay = self.settings.retry_base_seconds * (2 ** (attempt - 1))
                delay += random.uniform(0, min(1.0, delay * 0.2))
            LOG.warning("Cloudflare request attempt %d failed; retrying in %.1fs", attempt, delay)
            time.sleep(delay)

        raise CollectorError(f"Cloudflare request failed after retries: {last_error}")

    def capabilities(self) -> dict[str, Any]:
        response = self.query(SETTINGS_QUERY, {"zoneTag": self.settings.zone_id})
        zones = response.get("data", {}).get("viewer", {}).get("zones", [])
        if len(zones) != 1:
            raise CollectorError(f"expected one accessible zone, received {len(zones)}")
        dataset = zones[0].get("settings", {}).get("httpRequestsAdaptiveGroups")
        if not dataset or not dataset.get("enabled"):
            raise CollectorError("httpRequestsAdaptiveGroups is not enabled")
        missing = REQUIRED_FIELDS - set(dataset.get("availableFields") or [])
        if missing:
            raise CollectorError("required Cloudflare fields unavailable: " + ", ".join(sorted(missing)))
        return dataset

    def traffic(self, hostname: str, start: datetime, end: datetime) -> dict[str, Any]:
        variables = {
            "zoneTag": self.settings.zone_id,
            "filter": {
                "datetime_geq": iso_utc(start),
                "datetime_lt": iso_utc(end),
                "clientRequestHTTPHost": hostname,
                "requestSource": self.settings.request_source,
            },
        }
        response = self.query(TRAFFIC_QUERY, variables)
        zones = response.get("data", {}).get("viewer", {}).get("zones", [])
        if len(zones) != 1:
            raise CollectorError(f"traffic query expected one zone, received {len(zones)}")
        return zones[0]


def connect_database(path: Path) -> sqlite3.Connection:
    path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(path, timeout=30)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    connection.execute("PRAGMA busy_timeout = 30000")
    connection.execute("PRAGMA journal_mode = WAL")
    connection.execute("PRAGMA synchronous = FULL")
    connection.executescript(SCHEMA_SQL)
    set_metadata(connection, "schema_version", SCHEMA_VERSION)
    set_metadata(connection, "storage_timezone", "UTC")
    connection.commit()
    return connection


def set_metadata(connection: sqlite3.Connection, key: str, value: Any) -> None:
    connection.execute(
        """
        INSERT INTO metadata(key, value, updated_at_utc) VALUES (?, ?, ?)
        ON CONFLICT(key) DO UPDATE SET value=excluded.value, updated_at_utc=excluded.updated_at_utc
        """,
        (key, str(value), iso_utc(utc_now())),
    )


def database_check(connection: sqlite3.Connection, full: bool = False) -> str:
    pragma = "integrity_check" if full else "quick_check"
    rows = connection.execute(f"PRAGMA {pragma}").fetchall()
    result = "; ".join(str(row[0]) for row in rows)
    if result.lower() != "ok":
        raise CollectorError(f"SQLite {pragma} failed: {result}")
    return result


def sqlite_snapshot(source_path: Path, destination: Path, group_name: str | None = None) -> None:
    """Create an integrity-checked SQLite snapshot and publish it atomically."""
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = destination.with_name(destination.name + ".tmp")
    if temporary.exists():
        temporary.unlink()
    source_connection = sqlite3.connect(source_path, timeout=30)
    destination_connection = sqlite3.connect(temporary)
    try:
        database_check(source_connection, full=True)
        source_connection.backup(destination_connection)
        database_check(destination_connection, full=True)
    finally:
        destination_connection.close()
        source_connection.close()
    os.chmod(temporary, 0o640)
    if group_name:
        os.chown(temporary, -1, grp.getgrnam(group_name).gr_gid)
    temporary.replace(destination)


def _integer(value: Any) -> int:
    if value is None:
        return 0
    return max(0, int(round(float(value))))


def _number(value: Any) -> float | None:
    return None if value is None else float(value)


def _hour_key(item: dict[str, Any]) -> str | None:
    return (item.get("dimensions") or {}).get("datetimeHour")


def normalize_rows(
    hostname: str, start: datetime, end: datetime, payload: dict[str, Any], collected_at: str
) -> list[dict[str, Any]]:
    rows: dict[str, dict[str, Any]] = {}
    for hour in hour_range(start, end):
        key = iso_utc(hour)
        rows[key] = {
            "hour_utc": key,
            "hostname": hostname,
            "requests": 0,
            "visits": 0,
            "edge_request_bytes": 0,
            "edge_response_bytes": 0,
            "cached_requests": 0,
            "uncached_requests": 0,
            "origin_requests": 0,
            "cached_response_bytes": 0,
            "uncached_response_bytes": 0,
            "blocked_requests": 0,
            "status_4xx": 0,
            "status_5xx": 0,
            "origin_response_avg_ms": None,
            "origin_response_p50_ms": None,
            "origin_response_p95_ms": None,
            "origin_response_p99_ms": None,
            "sample_interval": 1.0,
            "is_sampled": 0,
            "source_dataset": "httpRequestsAdaptiveGroups",
            "collected_at_utc": collected_at,
        }

    for item in payload.get("totals") or []:
        key = _hour_key(item)
        if key not in rows:
            continue
        avg = item.get("avg") or {}
        quantiles = item.get("quantiles") or {}
        sums = item.get("sum") or {}
        interval = max(1.0, float(avg.get("sampleInterval") or 1.0))
        rows[key].update(
            requests=_integer(item.get("count")),
            visits=_integer(sums.get("visits")),
            edge_request_bytes=_integer(sums.get("edgeRequestBytes")),
            edge_response_bytes=_integer(sums.get("edgeResponseBytes")),
            origin_response_avg_ms=_number(avg.get("originResponseDurationMs")),
            origin_response_p50_ms=_number(quantiles.get("originResponseDurationMsP50")),
            origin_response_p95_ms=_number(quantiles.get("originResponseDurationMsP95")),
            origin_response_p99_ms=_number(quantiles.get("originResponseDurationMsP99")),
            sample_interval=interval,
            is_sampled=int(interval > 1.000001),
        )

    cache_totals: dict[str, int] = {key: 0 for key in rows}
    cache_bytes: dict[str, int] = {key: 0 for key in rows}
    for item in payload.get("cache") or []:
        key = _hour_key(item)
        if key not in rows:
            continue
        status = str((item.get("dimensions") or {}).get("cacheStatus") or "").lower()
        count = _integer(item.get("count"))
        response_bytes = _integer((item.get("sum") or {}).get("edgeResponseBytes"))
        if status in CACHED_REQUEST_STATUSES:
            rows[key]["cached_requests"] += count
        else:
            rows[key]["uncached_requests"] += count
        if status in CACHED_BYTE_STATUSES:
            rows[key]["cached_response_bytes"] += response_bytes
        else:
            rows[key]["uncached_response_bytes"] += response_bytes
        cache_totals[key] += count
        cache_bytes[key] += response_bytes

    for item in payload.get("statuses") or []:
        key = _hour_key(item)
        if key not in rows:
            continue
        status = _integer((item.get("dimensions") or {}).get("edgeResponseStatus"))
        count = _integer(item.get("count"))
        if 400 <= status <= 499:
            rows[key]["status_4xx"] += count
        elif 500 <= status <= 599:
            rows[key]["status_5xx"] += count

    for item in payload.get("security") or []:
        key = _hour_key(item)
        if key not in rows:
            continue
        action = str((item.get("dimensions") or {}).get("securityAction") or "").lower()
        if action in BLOCK_ACTIONS:
            rows[key]["blocked_requests"] += _integer(item.get("count"))

    for item in payload.get("origin") or []:
        key = _hour_key(item)
        if key not in rows:
            continue
        status = _integer((item.get("dimensions") or {}).get("originResponseStatus"))
        if status != 0:
            rows[key]["origin_requests"] += _integer(item.get("count"))

    for key, row in rows.items():
        # Cache groupings should cover the total. Fall back conservatively if Cloudflare
        # omits cacheStatus groups for a zero/edge-generated result.
        if cache_totals[key] == 0 and row["requests"] > 0:
            row["uncached_requests"] = row["requests"]
        if cache_bytes[key] == 0 and row["edge_response_bytes"] > 0:
            row["uncached_response_bytes"] = row["edge_response_bytes"]

    return [rows[key] for key in sorted(rows)]


def get_latest_hour(connection: sqlite3.Connection) -> datetime | None:
    value = connection.execute("SELECT MAX(hour_utc) FROM hourly_traffic").fetchone()[0]
    return parse_utc(value) if value else None


def collection_bounds(
    connection: sqlite3.Connection, settings: Settings, capabilities: dict[str, Any], now: datetime
) -> tuple[datetime, datetime]:
    retention_seconds = int(capabilities["notOlderThan"])
    retention_start = ceil_hour(now - timedelta(seconds=retention_seconds))
    end = floor_hour(now - timedelta(minutes=settings.settlement_delay_minutes))
    latest = get_latest_hour(connection)
    if latest is None:
        start = retention_start
    else:
        overlap = max(1, settings.overlap_hours)
        start = latest - timedelta(hours=overlap - 1)
        start = max(start, retention_start)
    return start, max(start, end)


def iter_chunks(start: datetime, end: datetime, max_duration_seconds: int) -> Iterable[tuple[datetime, datetime]]:
    max_hours = max(1, max_duration_seconds // 3600)
    current = start
    while current < end:
        chunk_end = min(end, current + timedelta(hours=max_hours))
        yield current, chunk_end
        current = chunk_end


def collect(settings: Settings, token: str) -> None:
    client = CloudflareClient(settings, token)
    capabilities = client.capabilities()
    connection = connect_database(settings.database_path)
    database_check(connection, full=False)
    now = utc_now()
    start, end = collection_bounds(connection, settings, capabilities, now)
    started_at = iso_utc(now)
    cursor = connection.execute(
        "INSERT INTO collection_runs(started_at_utc, status, range_start_utc, range_end_utc) VALUES (?, 'running', ?, ?)",
        (started_at, iso_utc(start), iso_utc(end)),
    )
    run_id = int(cursor.lastrowid)
    connection.commit()
    rows_upserted = 0

    try:
        set_metadata(connection, "cloudflare_dataset", "httpRequestsAdaptiveGroups")
        set_metadata(connection, "cloudflare_not_older_than_seconds", capabilities["notOlderThan"])
        set_metadata(connection, "cloudflare_max_duration_seconds", capabilities["maxDuration"])
        set_metadata(connection, "configured_hostnames", ",".join(settings.hostnames))
        connection.commit()

        if start >= end:
            LOG.info("No completed hour is ready for collection")
        for chunk_start, chunk_end in iter_chunks(start, end, int(capabilities["maxDuration"])):
            LOG.info("Collecting %s through %s", iso_utc(chunk_start), iso_utc(chunk_end))
            for hostname in settings.hostnames:
                payload = client.traffic(hostname, chunk_start, chunk_end)
                rows = normalize_rows(hostname, chunk_start, chunk_end, payload, iso_utc(utc_now()))
                with connection:
                    connection.executemany(UPSERT_SQL, rows)
                rows_upserted += len(rows)
                LOG.info("Upserted %d hourly rows for %s", len(rows), hostname)

        database_check(connection, full=False)
        connection.execute(
            """
            UPDATE collection_runs
               SET finished_at_utc=?, status='success', api_requests=?, rows_upserted=?
             WHERE id=?
            """,
            (iso_utc(utc_now()), client.request_count, rows_upserted, run_id),
        )
        connection.commit()
        sqlite_snapshot(
            settings.database_path,
            settings.api_snapshot_path,
            settings.api_snapshot_group,
        )
        LOG.info("Published read-only API snapshot: %s", settings.api_snapshot_path)
        LOG.info("Collection complete: %d rows upserted using %d API requests", rows_upserted, client.request_count)
    except Exception as error:
        connection.execute(
            """
            UPDATE collection_runs
               SET finished_at_utc=?, status='failed', api_requests=?, rows_upserted=?, error_message=?
             WHERE id=?
            """,
            (iso_utc(utc_now()), client.request_count, rows_upserted, str(error)[:1000], run_id),
        )
        connection.commit()
        raise
    finally:
        connection.close()


def print_capabilities(settings: Settings, token: str) -> None:
    client = CloudflareClient(settings, token)
    capabilities = client.capabilities()
    safe = {key: value for key, value in capabilities.items() if key != "availableFields"}
    safe["availableFieldCount"] = len(capabilities.get("availableFields") or [])
    print(json.dumps(safe, indent=2, sort_keys=True))


def check_database(settings: Settings, full: bool) -> None:
    connection = connect_database(settings.database_path)
    try:
        print(database_check(connection, full=full))
    finally:
        connection.close()


def backup_database(settings: Settings) -> None:
    if not settings.database_path.exists():
        raise CollectorError(f"database does not exist: {settings.database_path}")
    settings.backup_dir.mkdir(parents=True, exist_ok=True)
    timestamp = utc_now().strftime("%Y%m%dT%H%M%SZ")
    destination = settings.backup_dir / f"traffic-{timestamp}.sqlite"
    sqlite_snapshot(settings.database_path, destination)

    backups = sorted(settings.backup_dir.glob("traffic-*.sqlite"), reverse=True)
    for old_backup in backups[max(1, settings.backup_retention_count) :]:
        old_backup.unlink()
    LOG.info("Created consistent SQLite backup: %s", destination)


def status(settings: Settings) -> None:
    if not settings.database_path.exists():
        print(f"Database not created: {settings.database_path}")
        return
    connection = sqlite3.connect(f"file:{settings.database_path}?mode=ro", uri=True)
    connection.row_factory = sqlite3.Row
    try:
        summary = connection.execute(
            """
            SELECT COUNT(*) AS rows,
                   MIN(hour_utc) AS earliest_hour_utc,
                   MAX(hour_utc) AS latest_hour_utc,
                   COUNT(DISTINCT hostname) AS hostnames,
                   COALESCE(SUM(requests), 0) AS requests
              FROM hourly_traffic
            """
        ).fetchone()
        print(json.dumps(dict(summary), indent=2))
        print(f"database_bytes: {settings.database_path.stat().st_size}")
        recent = connection.execute(
            """
            SELECT id, started_at_utc, finished_at_utc, status, range_start_utc,
                   range_end_utc, api_requests, rows_upserted, error_message
              FROM collection_runs ORDER BY id DESC LIMIT 5
            """
        ).fetchall()
        print("recent_runs:")
        for row in recent:
            print(json.dumps(dict(row), sort_keys=True))
    finally:
        connection.close()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--config",
        type=Path,
        default=Path("/etc/pla/cloudflare-analytics.conf"),
        help="collector INI configuration",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("collect", help="collect and upsert available hourly data")
    subparsers.add_parser("capabilities", help="show non-secret Cloudflare dataset limits")
    check_parser = subparsers.add_parser("check", help="run a SQLite integrity check")
    check_parser.add_argument("--full", action="store_true", help="run full integrity_check")
    subparsers.add_parser("backup", help="create and retain transaction-safe local backups")
    subparsers.add_parser("status", help="show database and recent-run status")
    return parser


def main() -> int:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )
    args = build_parser().parse_args()
    try:
        settings = read_settings(args.config)
        token = os.environ.get("CLOUDFLARE_API_TOKEN", "")
        if args.command == "collect":
            collect(settings, token)
        elif args.command == "capabilities":
            print_capabilities(settings, token)
        elif args.command == "check":
            check_database(settings, full=args.full)
        elif args.command == "backup":
            backup_database(settings)
        elif args.command == "status":
            status(settings)
        return 0
    except Exception as error:
        LOG.error("%s", error)
        return 1


if __name__ == "__main__":
    sys.exit(main())
