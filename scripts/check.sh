#!/usr/bin/env bash
# One round of checks. Prints "name|ok|code|seconds" per check.
# A check is retried once after 20 s before it counts as down, so one dropped
# packet between GitHub and us is not an outage.
set -uo pipefail
KEY="${SUPABASE_ANON_KEY:-}"
probe() { # url needs_key
  if [ "$2" = yes ]; then
    curl -s -m 15 -o /dev/null -w '%{http_code} %{time_total}' -H "apikey: $KEY" -H "Authorization: Bearer $KEY" "$1"
  else
    curl -s -m 15 -o /dev/null -w '%{http_code} %{time_total}' "$1"
  fi
}
grep -vE '^\s*(#|$)' "$(dirname "$0")/checks.txt" | while IFS='|' read -r name url key ok; do
  name="$(echo "$name" | xargs)"; url="$(echo "$url" | xargs)"; key="$(echo "$key" | xargs)"; ok="$(echo "$ok" | xargs)"
  read -r code secs <<<"$(probe "$url" "$key")"
  if ! [[ "$code" =~ $ok ]]; then sleep 20; read -r code secs <<<"$(probe "$url" "$key")"; fi
  if [[ "$code" =~ $ok ]]; then echo "$name|up|$code|$secs"; else echo "$name|down|$code|$secs"; fi
done
