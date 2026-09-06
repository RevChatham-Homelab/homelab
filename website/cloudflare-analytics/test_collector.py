#!/usr/bin/env python3

import grp
import os
import sqlite3
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

import collector


class CollectorTests(unittest.TestCase):
    def test_collector_service_can_publish_api_snapshot(self):
        unit = (Path(__file__).parent / "pla-cloudflare-analytics.service").read_text()
        self.assertIn(
            "ReadWritePaths=/var/lib/pla/analytics /var/lib/pla-api",
            unit,
        )

    def test_atomic_sqlite_snapshot(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            source = Path(temp_dir) / "source.sqlite"
            snapshot = Path(temp_dir) / "published" / "traffic.sqlite"
            connection = collector.connect_database(source)
            connection.close()
            group_name = grp.getgrgid(os.getgid()).gr_name
            collector.sqlite_snapshot(source, snapshot, group_name)
            read_only = sqlite3.connect(f"file:{snapshot}?mode=ro&immutable=1", uri=True)
            self.assertEqual(read_only.execute("PRAGMA integrity_check").fetchone()[0], "ok")
            read_only.close()
            self.assertEqual(snapshot.stat().st_mode & 0o777, 0o640)

    def test_normalize_and_upsert_is_idempotent(self):
        start = datetime(2026, 9, 6, 10, tzinfo=timezone.utc)
        end = datetime(2026, 9, 6, 11, tzinfo=timezone.utc)
        payload = {
            "totals": [{
                "count": 10,
                "avg": {"sampleInterval": 1, "originResponseDurationMs": 12.5},
                "quantiles": {
                    "originResponseDurationMsP50": 10,
                    "originResponseDurationMsP95": 20,
                    "originResponseDurationMsP99": 25,
                },
                "sum": {"visits": 3, "edgeRequestBytes": 500, "edgeResponseBytes": 5000},
                "dimensions": {"datetimeHour": "2026-09-06T10:00:00Z"},
            }],
            "cache": [
                {"count": 6, "sum": {"edgeResponseBytes": 3000}, "dimensions": {"datetimeHour": "2026-09-06T10:00:00Z", "cacheStatus": "hit"}},
                {"count": 4, "sum": {"edgeResponseBytes": 2000}, "dimensions": {"datetimeHour": "2026-09-06T10:00:00Z", "cacheStatus": "miss"}},
            ],
            "statuses": [
                {"count": 8, "dimensions": {"datetimeHour": "2026-09-06T10:00:00Z", "edgeResponseStatus": 200}},
                {"count": 1, "dimensions": {"datetimeHour": "2026-09-06T10:00:00Z", "edgeResponseStatus": 404}},
                {"count": 1, "dimensions": {"datetimeHour": "2026-09-06T10:00:00Z", "edgeResponseStatus": 500}},
            ],
            "security": [{"count": 2, "dimensions": {"datetimeHour": "2026-09-06T10:00:00Z", "securityAction": "block"}}],
            "origin": [
                {"count": 7, "dimensions": {"datetimeHour": "2026-09-06T10:00:00Z", "originResponseStatus": 200}},
                {"count": 3, "dimensions": {"datetimeHour": "2026-09-06T10:00:00Z", "originResponseStatus": 0}},
            ],
        }
        rows = collector.normalize_rows("revchatham.com", start, end, payload, "2026-09-06T11:30:00Z")
        self.assertEqual(rows[0]["cached_requests"], 6)
        self.assertEqual(rows[0]["uncached_requests"], 4)
        self.assertEqual(rows[0]["origin_requests"], 7)
        self.assertEqual(rows[0]["status_4xx"], 1)
        self.assertEqual(rows[0]["status_5xx"], 1)
        self.assertEqual(rows[0]["blocked_requests"], 2)

        with tempfile.TemporaryDirectory() as temp_dir:
            connection = collector.connect_database(Path(temp_dir) / "traffic.sqlite")
            connection.execute(collector.UPSERT_SQL, rows[0])
            connection.execute(collector.UPSERT_SQL, rows[0])
            connection.commit()
            self.assertEqual(connection.execute("SELECT COUNT(*) FROM hourly_traffic").fetchone()[0], 1)
            self.assertEqual(collector.database_check(connection, full=True), "ok")
            connection.close()

    def test_week_starts_monday(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            connection = collector.connect_database(Path(temp_dir) / "traffic.sqlite")
            row = {
                "hour_utc": "2026-09-06T10:00:00Z",
                "hostname": "revchatham.com",
                "requests": 1,
                "visits": 1,
                "edge_request_bytes": 1,
                "edge_response_bytes": 1,
                "cached_requests": 0,
                "uncached_requests": 1,
                "origin_requests": 1,
                "cached_response_bytes": 0,
                "uncached_response_bytes": 1,
                "blocked_requests": 0,
                "status_4xx": 0,
                "status_5xx": 0,
                "origin_response_avg_ms": 1.0,
                "origin_response_p50_ms": 1.0,
                "origin_response_p95_ms": 1.0,
                "origin_response_p99_ms": 1.0,
                "sample_interval": 1.0,
                "is_sampled": 0,
                "source_dataset": "httpRequestsAdaptiveGroups",
                "collected_at_utc": "2026-09-06T11:00:00Z",
            }
            connection.execute(collector.UPSERT_SQL, row)
            connection.commit()
            value = connection.execute("SELECT period_start_utc FROM traffic_weekly").fetchone()[0]
            self.assertEqual(value, "2026-08-31")
            connection.close()


if __name__ == "__main__":
    unittest.main()
