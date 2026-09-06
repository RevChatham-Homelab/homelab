# Project Liquid Alert: Website Traffic Metrics

**Document type:** Implementation record
**Status:** Complete and verified
**Implementation date:** 2026-09-06
**Server:** `ubuntu-server`
**Website:** `revchatham.com`

## Purpose

This implementation provides site-specific Nginx traffic metrics to Prometheus for a future Project Liquid Alert (PLA) website-traffic card. The card can show current request rate, 15-minute and 1-hour history, response status classes, transferred data, and origin response time.

Website activity is informational. A new request may trigger a brief orange glow on the website card, but it must not change PLA's overall alert or severity state.

## Result

Traffic follows this monitoring path:

```text
Visitor -> Cloudflare -> Nginx Proxy Manager -> revchatham-site
                                               |
                                               v
                                  dedicated Nginx access log
                                               |
                                               v
                                    nginxlog-exporter:4040
                                               |
                                               v
                             Prometheus job: nginx_website
                                               |
                                               v
                                      PLA traffic card
```

The deployment uses `prometheus-nginxlog-exporter` rather than Nginx `stub_status`. The log exporter preserves the website-specific status, method, byte, and response-time dimensions needed by PLA.

## Pre-change state

- The website ran as the `revchatham-site` container from `/home/angel/website/compose.yml`.
- The site used `nginx:latest` and published host port `8081` to container port `80`.
- Nginx Proxy Manager owned host ports `80` and `443`.
- The website and Prometheus containers shared the external Docker network `homelab`.
- Nginx access logging pointed to `/dev/stdout` through `/var/log/nginx/access.log`.
- Prometheus scraped itself, Node Exporter, and cAdvisor at the global 15-second interval.
- There was no Nginx exporter target and host port `4040` was unused.

## Backups

The original files were copied before editing:

```text
/home/angel/backups/pla-nginx-metrics-20260906/website-compose.yml.original
/home/angel/backups/pla-nginx-metrics-20260906/prometheus.yml.original
```

Recorded SHA-256 checksums:

```text
0656c1c168a467ed01979e3a2aee05be2736e882b7f2c679c39f46487bd931c6  website-compose.yml.original
b6e0a5a32a8e7975b77404ff3179bc2676a411b3e6a7f8189540d7e3ce789f38  prometheus.yml.original
```

## Files added

```text
/home/angel/website/nginx/pla-logging.conf
/home/angel/website/exporter/config.hcl
/home/angel/website/logs/revchatham.access.log
/etc/logrotate.d/revchatham-site
```

## Nginx site-specific logging

`/home/angel/website/nginx/pla-logging.conf`:

```nginx
log_format pla_website
    '$remote_addr - $remote_user [$time_local] "$request" '
    '$status $body_bytes_sent $request_length $request_time '
    '"$http_referer" "$http_user_agent" "$http_x_forwarded_for"';

access_log /var/log/nginx/pla/revchatham.access.log pla_website;
```

The format supplies:

- `$request`: request method, path, and protocol
- `$status`: HTTP response status
- `$body_bytes_sent`: response payload bytes
- `$request_length`: received request bytes
- `$request_time`: total time Nginx spent handling the request
- forwarded-client information for operational troubleshooting

The existing stdout access log remains enabled. The new file log is an additional site-specific source for the exporter.

## Exporter configuration

Image:

```text
quay.io/martinhelmich/prometheus-nginxlog-exporter:v1.11.0
```

Image digest observed during deployment:

```text
sha256:b36976cb58584529381a92404a7ba9868b03e1a321c9dc7228cc9ecd93a80440
```

`/home/angel/website/exporter/config.hcl`:

```hcl
listen {
  port             = 4040
  address          = "0.0.0.0"
  metrics_endpoint = "/metrics"
}

namespace "revchatham" {
  format = "$remote_addr - $remote_user [$time_local] \"$request\" $status $body_bytes_sent $request_length $request_time \"$http_referer\" \"$http_user_agent\" \"$http_x_forwarded_for\""

  source {
    files = [
      "/mnt/nginxlogs/revchatham.access.log"
    ]
  }

  labels {
    site        = "revchatham.com"
    environment = "production"
  }

  histogram_buckets = [
    0.005,
    0.01,
    0.025,
    0.05,
    0.1,
    0.25,
    0.5,
    1,
    2.5,
    5
  ]
}
```

The exporter listens on all interfaces inside its container so Prometheus can reach it through Docker. Compose publishes the port only on host loopback:

```yaml
ports:
  - "127.0.0.1:4040:4040"
```

Therefore:

- Docker endpoint: `http://nginxlog-exporter:4040/metrics`
- Host-local endpoint: `http://127.0.0.1:4040/metrics`
- No public or LAN-wide exporter listener is created

## Website Compose changes

The website service gained two mounts:

```yaml
volumes:
  - ./html:/usr/share/nginx/html:ro
  - ./nginx/pla-logging.conf:/etc/nginx/conf.d/00-pla-logging.conf:ro
  - ./logs:/var/log/nginx/pla
```

The following service was added to `/home/angel/website/compose.yml`:

```yaml
nginxlog-exporter:
  image: quay.io/martinhelmich/prometheus-nginxlog-exporter:v1.11.0
  container_name: nginxlog-exporter
  restart: unless-stopped
  depends_on:
    - website
  networks:
    - homelab
  ports:
    - "127.0.0.1:4040:4040"
  volumes:
    - ./logs:/mnt/nginxlogs:ro
    - ./exporter/config.hcl:/etc/prometheus-nginxlog-exporter.hcl:ro
  command:
    - -config-file
    - /etc/prometheus-nginxlog-exporter.hcl
```

Both `revchatham-site` and `nginxlog-exporter` use `restart: unless-stopped` and the `homelab` network.

## Prometheus configuration

The following job was added to `/home/angel/prometheus/prometheus.yml`:

```yaml
- job_name: nginx_website
  scrape_interval: 5s
  static_configs:
    - targets:
        - nginxlog-exporter:4040
```

Prometheus retained its global 15-second interval for all other jobs. Only `nginx_website` scrapes every five seconds.

A one-second scrape interval would make a PLA activity pulse more immediate, but it would create five times as many samples and five times the scrape activity for this job. Five seconds is the selected balance.

## Log rotation

`/etc/logrotate.d/revchatham-site`:

```text
/home/angel/website/logs/revchatham.access.log {
    daily
    maxsize 10M
    rotate 14
    missingok
    notifempty
    compress
    delaycompress
    copytruncate
    su angel angel
}
```

The log rotates daily, rotates early above 10 MiB, and retains 14 rotations. `copytruncate` preserves the active pathname and open file behavior for both Nginx and the exporter.

A forced rotation test succeeded. The exporter reported that it reopened the truncated file, processed the next request, increased the request counter from `8` to `9`, and retained a parse-error count of `0`.

## Exact observed metrics

Prometheus adds these target labels to scraped series:

```text
job="nginx_website"
instance="nginxlog-exporter:4040"
```

Application metrics have these additional labels where applicable:

```text
environment="production"
site="revchatham.com"
method="GET"
status="200" | "404" | other observed HTTP status
```

Observed metric families:

| Metric | Type | Purpose |
| --- | --- | --- |
| `revchatham_http_response_count_total` | Counter | Requests grouped by method and status |
| `revchatham_http_response_size_bytes` | Counter | Response payload bytes |
| `revchatham_http_request_size_bytes` | Counter | Received request bytes |
| `revchatham_http_response_time_seconds` | Summary | Origin response-time quantiles |
| `revchatham_http_response_time_seconds_sum` | Summary counter | Accumulated origin response time |
| `revchatham_http_response_time_seconds_count` | Summary counter | Timed request count |
| `revchatham_http_response_time_seconds_hist_bucket` | Histogram bucket | Origin response-time distribution |
| `revchatham_http_response_time_seconds_hist_sum` | Histogram counter | Histogram response-time sum |
| `revchatham_http_response_time_seconds_hist_count` | Histogram counter | Histogram observation count |
| `revchatham_parse_errors_total` | Counter | Access-log lines the exporter could not parse |

Although `revchatham_http_response_size_bytes` and `revchatham_http_request_size_bytes` do not end in `_total`, the exporter declares them as Prometheus counters. `rate()` and `increase()` are appropriate; Prometheus 3 may emit an informational naming-convention message.

## PLA PromQL handoff

All examples are scoped to the specific job and website.

### Current request rate

Requests per second, smoothed across one minute:

```promql
sum(rate(revchatham_http_response_count_total{job="nginx_website",site="revchatham.com"}[1m])) or vector(0)
```

### Total requests

Current exporter counter total:

```promql
sum(revchatham_http_response_count_total{job="nginx_website",site="revchatham.com"}) or vector(0)
```

This instantaneous total is since the exporter last started. Prometheus range functions handle exporter counter resets when calculating rates and window totals.

### Requests during the last 15 minutes

```promql
round(sum(increase(revchatham_http_response_count_total{job="nginx_website",site="revchatham.com"}[15m]))) or vector(0)
```

### Requests during the last hour

```promql
round(sum(increase(revchatham_http_response_count_total{job="nginx_website",site="revchatham.com"}[1h]))) or vector(0)
```

`increase()` extrapolates at range boundaries and can return fractional values. `round()` is appropriate when PLA displays a request count. Do not round rate graphs.

### Fifteen-minute and one-hour history charts

Use this expression as a range query:

```promql
sum(rate(revchatham_http_response_count_total{job="nginx_website",site="revchatham.com"}[1m])) or vector(0)
```

Recommended query-range settings:

| History | Range | Step |
| --- | ---: | ---: |
| Short history | 15 minutes | 5 seconds |
| Long history | 1 hour | 15 seconds |

### Status-class rates

```promql
# 2xx
sum(rate(revchatham_http_response_count_total{job="nginx_website",site="revchatham.com",status=~"2.."}[1m])) or vector(0)

# 3xx
sum(rate(revchatham_http_response_count_total{job="nginx_website",site="revchatham.com",status=~"3.."}[1m])) or vector(0)

# 4xx
sum(rate(revchatham_http_response_count_total{job="nginx_website",site="revchatham.com",status=~"4.."}[1m])) or vector(0)

# 5xx
sum(rate(revchatham_http_response_count_total{job="nginx_website",site="revchatham.com",status=~"5.."}[1m])) or vector(0)
```

Successful versus error traffic:

```promql
# Success: 2xx and 3xx
sum(rate(revchatham_http_response_count_total{job="nginx_website",site="revchatham.com",status=~"[23].."}[1m])) or vector(0)

# Error: 4xx and 5xx
sum(rate(revchatham_http_response_count_total{job="nginx_website",site="revchatham.com",status=~"[45].."}[1m])) or vector(0)
```

The zero fallback prevents a missing status class—for example, no observed `5xx`—from appearing as missing data.

### Transferred data

Current response-byte rate:

```promql
sum(rate(revchatham_http_response_size_bytes{job="nginx_website",site="revchatham.com"}[1m])) or vector(0)
```

Total response bytes since exporter start:

```promql
sum(revchatham_http_response_size_bytes{job="nginx_website",site="revchatham.com"}) or vector(0)
```

Response bytes during the last 15 minutes:

```promql
sum(increase(revchatham_http_response_size_bytes{job="nginx_website",site="revchatham.com"}[15m])) or vector(0)
```

Response bytes during the last hour:

```promql
sum(increase(revchatham_http_response_size_bytes{job="nginx_website",site="revchatham.com"}[1h])) or vector(0)
```

Received request-byte rate is available by substituting `revchatham_http_request_size_bytes`.

### Origin response time

Average Nginx processing time across five minutes:

```promql
(sum(rate(revchatham_http_response_time_seconds_sum{job="nginx_website",site="revchatham.com"}[5m]))
 /
 clamp_min(sum(rate(revchatham_http_response_time_seconds_count{job="nginx_website",site="revchatham.com"}[5m])), 0.000000001))
or vector(0)
```

Optional p95 origin response time:

```promql
histogram_quantile(
  0.95,
  sum by (le) (
    rate(revchatham_http_response_time_seconds_hist_bucket{job="nginx_website",site="revchatham.com"}[5m])
  )
)
```

The site is static and local Nginx processing completed in less than the log's millisecond precision during testing, producing `0.000` seconds. These metrics represent origin processing—not the visitor's full Cloudflare and network round-trip time. End-user-style latency would require a separate external or black-box probe.

### Orange request pulse

Recommended signal:

```promql
sum(revchatham_http_response_count_total{job="nginx_website",site="revchatham.com"}) or vector(0)
```

PLA should poll this raw counter at the same five-second cadence and retain the previous value:

1. On the first sample, store the value without glowing.
2. If `current > previous`, glow the website card orange briefly.
3. If `current == previous`, do nothing.
4. If `current < previous`, treat it as an exporter counter reset and replace the baseline without glowing.
5. If the query is unavailable, do not interpret missing traffic data as activity.

The pulse is a card-local visual event only. It must not feed PLA's warning/critical state machine, global edge glow, taskbar alert pulse, or overall severity calculation.

PromQL-only fallback:

```promql
(sum(increase(revchatham_http_response_count_total{job="nginx_website",site="revchatham.com"}[15s])) > bool 0) or vector(0)
```

This returns `1` when Prometheus observed a counter increase during the last 15 seconds and `0` otherwise. Because `increase()` extrapolates, its numeric increase is not an exact event count; use only the Boolean result. It may also keep the glow state active longer than a client-side counter comparison.

### Exporter health and parser integrity

```promql
up{job="nginx_website"}
```

```promql
revchatham_parse_errors_total{job="nginx_website"}
```

The verified parser-error value was `0`.

## Verification evidence

The following checks passed:

- `nginx -t`: configuration syntax successful
- Exporter `-verify-config`: configuration valid
- `docker compose config --quiet`: website Compose valid
- `promtool check config`: Prometheus configuration valid
- Prometheus hot reload with `SIGHUP`: successful
- `up{job="nginx_website"}`: `1`
- Five-second scrape cadence: three samples observed in 16 seconds
- Controlled burst: four `200` responses and two `404` responses
- Total request counter after burst: `8`
- Test request rate: `0.24` requests/second
- Test successful rate: `0.16` requests/second
- Test error rate: `0.08` requests/second
- Test response-byte rate: `59.6` bytes/second
- Total response bytes at final query: `1,939`
- Total received request bytes at final query: `1,073`
- Idle Boolean pulse: `0`
- Exporter parse errors: `0`
- Forced log rotation: successful
- Post-rotation request counter: increased from `8` to `9`
- Exporter log: truncated file reopened successfully
- Host port `4040`: bound only to `127.0.0.1`

## Traffic interpretation

The card measures requests that reach the `revchatham-site` origin container. It includes legitimate visitors, search crawlers, vulnerability scanners, bots, and monitoring probes. Requests satisfied entirely from Cloudflare cache may not reach the origin and therefore may not appear.

During initial inspection, public probes and scanners generated genuine `404` traffic. Consequently, orange activity may occur without a human visitor. This is expected unless a later design introduces carefully bounded filtering.

No request path or client address is used as a Prometheus label. This avoids unbounded label cardinality and prevents visitor IP addresses from entering Prometheus time-series labels.

## Security properties

- The exporter endpoint is not exposed publicly.
- Host access is restricted to `127.0.0.1:4040`.
- Prometheus reaches the exporter through the private `homelab` Docker network.
- The exporter mounts the access-log directory read-only.
- The exporter configuration is mounted read-only.
- The Nginx logging configuration is mounted read-only.
- No Nginx `stub_status` endpoint was enabled.
- No secrets are required by this exporter.

## Operations

Container status:

```bash
cd /home/angel/website
docker compose ps
```

Exporter logs:

```bash
docker logs --tail 100 nginxlog-exporter
```

Raw metrics from the Ubuntu host:

```bash
curl -fsS http://127.0.0.1:4040/metrics
```

Validate Nginx:

```bash
docker exec revchatham-site nginx -t
```

Validate the exporter configuration:

```bash
docker run --rm \
  -v /home/angel/website/exporter/config.hcl:/etc/prometheus-nginxlog-exporter.hcl:ro \
  -v /home/angel/website/logs:/mnt/nginxlogs:ro \
  quay.io/martinhelmich/prometheus-nginxlog-exporter:v1.11.0 \
  -config-file /etc/prometheus-nginxlog-exporter.hcl \
  -verify-config
```

Validate Prometheus:

```bash
docker run --rm \
  --entrypoint promtool \
  -v /home/angel/prometheus/prometheus.yml:/etc/prometheus/prometheus.yml:ro \
  prom/prometheus:v3.13.0 \
  check config /etc/prometheus/prometheus.yml
```

Reload Prometheus after a validated configuration edit:

```bash
docker kill --signal=HUP prometheus
```

## Rollback

Rollback removes the exporter and dedicated log while restoring the original website and Prometheus configurations. The website container will be recreated briefly.

```bash
cp -a /home/angel/backups/pla-nginx-metrics-20260906/website-compose.yml.original \
  /home/angel/website/compose.yml

cp -a /home/angel/backups/pla-nginx-metrics-20260906/prometheus.yml.original \
  /home/angel/prometheus/prometheus.yml

cd /home/angel/website
docker compose up -d --remove-orphans

docker kill --signal=HUP prometheus

sudo rm /etc/logrotate.d/revchatham-site
```

Before performing rollback, validate both restored configuration files. The new `nginx`, `exporter`, and `logs` directories may be retained as inactive evidence or removed manually after confirming the rollback.

## PLA implementation boundary

This work completes the server-side metrics pipeline only. PLA implementation remains separate. PLA should consume Prometheus queries rather than connect directly to port `4040`, and the traffic pulse must remain isolated from the global alert-state logic.

## References

- [prometheus-nginxlog-exporter](https://github.com/martin-helmich/prometheus-nginxlog-exporter/)
- [NGINX Prometheus Exporter](https://github.com/nginx/nginx-prometheus-exporter)
