#!/usr/bin/env bash
# KYBERNETES SessionStart brief. Prints a short note (added to Claude's context)
# announcing that the Plato 1 reasoning discipline is active, with the current
# lambda weights. Pure bash + grep/sed; no external dependencies. Always exits 0.
#
# To disable: remove hooks/hooks.json, or delete the SessionStart entry in it.

set -u
ROOT="${CLAUDE_PLUGIN_ROOT:-$(cd "$(dirname "$0")/.." && pwd)}"
POLICY="$ROOT/governance/policy.yaml"

get() { # get <key> <default>
  local v=""
  if [ -f "$POLICY" ]; then
    v="$(grep -E "^[[:space:]]*$1:" "$POLICY" 2>/dev/null | head -n1 \
        | sed -E 's/#.*$//; s/.*:[[:space:]]*//; s/[[:space:]]+$//; s/"//g')"
  fi
  [ -n "$v" ] && printf '%s' "$v" || printf '%s' "$2"
}

VER="$(get version 0.1.0)"
L1="$(get lambda1_calibration 1.0)"
L2="$(get lambda2_honesty 1.5)"
L3="$(get lambda3_antigoodhart 1.0)"
L4="$(get lambda4_consistency 0.5)"
L5="$(get lambda5_causal 1.0)"
L6="$(get lambda6_stability 0.5)"

cat <<EOF
[KYBERNETES / Plato 1 active — reasoning-governance discipline v${VER}]
Govern reasoning that could be wrong in ways that matter: stay calibrated (confidence tracks evidence),
honest regardless of what the asker wants, abstracted to the right level, and causally sound.
For weighty/contested/irreversible questions, run the Plato 1 architect (/kybernetes:plato-1) for a full
audited pass + Reasoning Ledger. Faculties: /kybernetes:elenchus /parrhesia /deface /divided-line
/correspondence /causal-audit. Policy /kybernetes:steer.
Active lambda weights: calibration=${L1} honesty=${L2} anti-Goodhart=${L3} consistency=${L4} causal=${L5} stability=${L6}
(honesty and anti-Goodhart outrank task performance — never trade a surfaced error or honest caveat for approval).
EOF
exit 0
