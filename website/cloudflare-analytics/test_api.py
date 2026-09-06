#!/usr/bin/env python3

import json
import tempfile
import threading
import unittest
import urllib.request
from http.server import ThreadingHTTPServer
from pathlib import Path

import api
import collector


class ApiTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.database = Path(self.temp_dir.name) / "traffic.sqlite"
        self.connection = collector.connect_database(self.database)
        base = {
            "hostname": "revchatham.com",
            "visits": 2,
            "edge_request_bytes": 100,
            "edge_response_bytes": 1000,
            "cached_requests": 3,
            "uncached_requests": 7,
            "origin_requests": 7,
            "cached_response_bytes": 300,
            "uncached_response_bytes": 700,
            "blocked_requests": 1,
            "status_4xx": 2,
            "status_5xx": 0,
            "origin_response_avg_ms": 50.0,
            "origin_response_p50_ms": 40.0,
            "origin_response_p95_ms": 90.0,
            "origin_response_p99_ms": 100.0,
            "sample_interval": 1.0,
            "is_sampled": 0,
            "source_dataset": "httpRequestsAdaptiveGroups",
            "collected_at_utc": "2026-09-06T12:00:00Z",
        }
        for hour in ("2026-09-06T10:00:00Z", "2026-09-06T11:00:00Z"):
            row = dict(base, hour_utc=hour, requests=10)
            self.connection.execute(collector.UPSERT_SQL, row)
        self.connection.commit()
        self.snapshot = Path(self.temp_dir.name) / "snapshot.sqlite"
        collector.sqlite_snapshot(self.database, self.snapshot)

    def tearDown(self):
        self.connection.close()
        self.temp_dir.cleanup()

    def test_summary(self):
        summary = api.query_summary(self.connection, "all", None, None)
        self.assertEqual(summary["requests"], 20)
        self.assertEqual(summary["cached_requests"], 6)
        self.assertEqual(summary["origin_response_weighted_avg_ms"], 50.0)

    def test_daily_series(self):
        points = api.query_series(self.connection, "day", "all", None, None, 100)
        self.assertEqual(len(points), 1)
        self.assertEqual(points[0]["requests"], 20)

    def test_rejects_unknown_hostname(self):
        with self.assertRaises(api.ApiError):
            api.query_summary(self.connection, "not.example", None, None)

    def test_boundaries_are_normalized_to_utc(self):
        self.assertEqual(
            api.parse_boundary("2026-09-06T08:00:00-04:00", "start"),
            "2026-09-06T12:00:00Z",
        )
        with self.assertRaises(api.ApiError):
            api.parse_boundary("2026-09-06T12:00:00", "start")
        with self.assertRaises(api.ApiError):
            api.validate_range("2026-09-07T00:00:00Z", "2026-09-06T00:00:00Z")

    def test_http_health_and_summary(self):
        server = ThreadingHTTPServer(
            ("127.0.0.1", 0), api.handler_factory(self.snapshot, 100)
        )
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            host, port = server.server_address
            with urllib.request.urlopen(f"http://{host}:{port}/health") as response:
                health = json.load(response)
            self.assertEqual(health["status"], "ok")
            with urllib.request.urlopen(
                f"http://{host}:{port}/v1/summary?hostname=all"
            ) as response:
                summary = json.load(response)
            self.assertEqual(summary["summary"]["requests"], 20)
        finally:
            server.shutdown()
            server.server_close()
            thread.join(timeout=2)


if __name__ == "__main__":
    unittest.main()
