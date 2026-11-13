#!/usr/bin/env bash
# Five-second sanity check. Run it after every change.
set -u
fail=0
pass() { printf 'PASS  %s\n' "$1"; }
flunk() { printf 'FAIL  %s\n' "$1"; fail=1; }

# 1. The app answers on loopback.
code=$(curl -s -o /dev/null -w '%{http_code}' --max-time 5 http://127.0.0.1:8000/ || true)
if [ "$code" -ge 200 ] 2>/dev/null && [ "$code" -lt 400 ]; then pass "app answers ($code)"; else flunk "app answers (got ${code:-nothing})"; fi

# 2. Nothing but SSH listens on a public address.
open=$(ss -Htln | awk '{print $4}' | grep -Ev '^(127\.|\[::1\])' | grep -Ev ':22$' || true)
if [ -z "$open" ]; then pass "only port 22 is public"; else flunk "public listeners: $(echo $open)"; fi

# 3. The database is not published to the host at all.
if docker compose port db 5432 >/dev/null 2>&1; then flunk "db is published to the host"; else pass "db not exposed"; fi

# 4. Basic security headers are present.
hdrs=$(curl -sI --max-time 5 http://127.0.0.1:8000/ | tr -d '\r' | tr '[:upper:]' '[:lower:]')
for h in x-content-type-options content-security-policy x-frame-options; do
  if printf '%s\n' "$hdrs" | grep -q "^$h:"; then pass "header $h"; else flunk "header $h missing"; fi
done

# 5. The firewall is on.
if sudo ufw status | grep -q '^Status: active'; then pass "ufw active"; else flunk "ufw is not active"; fi

exit $fail
