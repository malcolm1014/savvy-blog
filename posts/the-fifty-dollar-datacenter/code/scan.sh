#!/usr/bin/env bash
# Attack your own app. Run from ~/lab with the lab up.
# One scanner at a time: this is a small box.
set -u
mkdir -p reports

echo "== 1/3 Semgrep: reading the source for known-bad patterns =="
docker run --rm -v "$PWD/app:/src" semgrep/semgrep \
  semgrep scan --config auto --quiet /src | tee reports/semgrep.txt

echo "== 2/3 Trivy: known CVEs in dependencies and the image =="
docker run --rm -v "$PWD:/src" aquasec/trivy:latest \
  fs --scanners vuln,secret,misconfig --quiet /src | tee reports/trivy.txt

echo "== 3/3 ZAP baseline: probing the running app from inside lab_net =="
docker run --rm --network lab_net -v "$PWD/reports:/zap/wrk:rw" \
  ghcr.io/zaproxy/zaproxy:stable \
  zap-baseline.py -t http://app:8000 -r zap.html -m 2 || true

echo "Reports are in ./reports"
