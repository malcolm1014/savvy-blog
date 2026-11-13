# The Fifty-Dollar Datacenter: lab kit

Files from the article
[The Fifty-Dollar Datacenter](https://malcolm1014.github.io/savvy-blog/posts/the-fifty-dollar-datacenter/)
by Malcolm R. Smith, Savvy Security LLC.

| File | What it is |
|---|---|
| `cloud-init.yaml` | Paste into Hetzner's "Cloud config" box. Builds a locked-down server. |
| `docker-compose.yml` | The lab: your app, Postgres, one private network. |
| `env.example` | Copy to `.env` and change every value. |
| `CLAUDE.md` | House rules Claude Code reads at the start of every session. |
| `smoke.sh` | Five-second check. Run after every change. |
| `scan.sh` | Semgrep, Trivy, and OWASP ZAP against your own app. |

Only test what you own. Free to use and change.
