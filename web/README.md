# Brand OS - local web interface

A small Flask app that wraps `tools/marketing_brain.py` and serves the Brain in a browser. Same search / scoring / parsing logic as the CLI - the web layer only translates HTTP requests into Brain calls and renders results.

Designed for local development out of the box. To deploy to a server, see the "Production deploy" section below.

## Pages

| Path | What it shows |
|---|---|
| `/` | Search box across all four layers. ?q= shows ranked results. |
| `/icp` | The canonical ICP, content vectors, walls, founder anchor, forbids, licenses, voice register refs. |
| `/canon` | All canon principles, filter by `?school=be` / `voss` / `cialdini`. |
| `/tactic/<name>` | Everything tagged with one tactic. |
| `/for-vector/<key>` | Everything serving one content vector. |
| `/for-stage/<name>` | Everything tagged for one funnel stage. |
| `/guidelines` | The 4 canonical foundation files rendered as HTML. |
| `/howto` | How to use the Brain - browser / Claude session / building a customer site. |
| `/stats` | Live index counts + content-vector coverage + top tactics. |
| `/healthz` | Liveness probe, no auth. |

## Local development

```bash
cd <repo>
python3 -m venv .venv
.venv/bin/pip install -r web/requirements.txt
.venv/bin/python web/app.py
# Open http://127.0.0.1:8081/
```

The Flask app binds to 127.0.0.1 only by default. If you need to expose it on your local network for screen sharing, change the bind in `web/app.py` last block from `host="127.0.0.1"` to `host="0.0.0.0"`. Do not do this in production without authentication.

## Architecture

```
Browser
  -> nginx (HTTPS + auth + rate limit + security headers, optional)
  -> 127.0.0.1:8081 (gunicorn, 2 workers x 2 threads)
  -> web/app.py (Flask)
  -> tools/marketing_brain.py (composite-scoring search)
  -> 01-canon/_brain-index.json + .db (rebuilt on every deploy)
  -> 00-foundations/*.md + 01-canon/*.md + 08-templates/vocab/*.json (source of truth)
```

The Flask app is read-only from the user's perspective. Index rebuilds happen via `python3 tools/marketing_brain.py rebuild-index`, not at request time.

## Production deploy

This template ships the Flask app + Jinja templates only. Production deployment (VPS, Vercel, Cloudflare Workers, Render, etc.) is up to you. A working VPS reference implementation exists - ask the template author if you want a copy of the deploy script and matching nginx + systemd config.

Recommended defence in depth when putting the interface on the public internet:

1. **Unguessable URL / subdomain.** Generate a random 16-character suffix.
2. **HTTP basic auth.** Single shared credential for the founding team. Rotate when team changes.
3. **noindex header.** `add_header X-Robots-Tag "noindex, nofollow, noarchive" always;`
4. **HSTS + X-Frame-Options DENY + X-Content-Type-Options nosniff + Referrer-Policy no-referrer.**
5. **127.0.0.1 binding for the Python process.** Public traffic must traverse the reverse proxy.
6. **Read-only filesystem for the service user** (systemd `ProtectSystem=strict` with explicit `ReadWritePaths` for the index dir).
7. **Rate limit** (nginx `limit_req` zone) to discourage credential brute force.

The Brain interface contains your brand's full strategic playbook. Treat it like internal docs.
