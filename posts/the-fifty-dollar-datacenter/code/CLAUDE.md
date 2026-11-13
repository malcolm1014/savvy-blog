# Lab rules

This server is a disposable test lab. Read these before doing anything.

## What this box is
- A rented cloud server used only for testing. Nothing here is production.
- Fake data only. Never real customer data, real card numbers, or real secrets.

## Hard rules
- Only test targets inside the Docker network `lab_net`. Never scan, probe,
  or send traffic to any host I do not own.
- Never publish a container port to 0.0.0.0. Bind to 127.0.0.1 only.
- Never change ufw, sshd, or fail2ban settings without asking me first.
- Secrets live in `.env`. Never print them, never commit them.
- Ask before deleting volumes, images, or anything under `~/lab`.

## How to work
- After every change: `docker compose up -d --build`, then `./smoke.sh`.
- When a scanner reports a finding: show it to me in plain English, say how
  bad it is, propose the fix, and wait for a yes.
- Keep a running log of findings and fixes in `FINDINGS.md`.
- I am on a phone. Keep output short. Summaries first, detail when I ask.
