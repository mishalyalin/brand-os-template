"""Marketing Brain web interface.

Thin Flask wrapper over `tools/marketing_brain.py`. All search / scoring /
parsing logic lives in the CLI module; this file only translates HTTP
requests into Brain calls and renders results.

Designed for local-first deploy; the production deploy pattern is documented in web/README.md under an
unguessable subdomain. nginx in front handles HTTPS + HTTP basic auth +
rate limiting. The Flask app binds to 127.0.0.1:8081 only.

Routes:
    GET /                   - search page (renders results if ?q= present)
    GET /icp                - the 6 content vectors + ICP definition + walls
    GET /tactic/<name>      - everything tagged with this tactic
    GET /for-vector/<name>  - everything serving this content vector
    GET /for-stage/<name>   - everything tagged for this funnel stage
    GET /canon              - canon principles, optional ?school=
    GET /guidelines         - brand voice + the 7 hard rules
    GET /howto              - how to use the Brain from a fresh Claude session
    GET /stats              - index stats
    GET /healthz            - liveness probe (no auth, used by deploy script)

The app is read-only from the user's perspective. The underlying index
rebuilds via `python3 tools/marketing_brain.py rebuild-index` after each
GitHub push (handled by the deploy hook, not this app).
"""

from __future__ import annotations

import html
import re
import sys
from pathlib import Path
from typing import Any

import markdown
from flask import Flask, abort, render_template, request
from markupsafe import Markup

# Make tools/marketing_brain.py importable. The web/ folder sits at repo
# root alongside tools/, so go up one level and add tools/ to sys.path.
REPO_ROOT = Path(__file__).resolve().parent.parent
TOOLS_DIR = REPO_ROOT / "tools"
sys.path.insert(0, str(TOOLS_DIR))

import marketing_brain as mb  # noqa: E402  - sys.path mutation required above


app = Flask(
    __name__,
    template_folder=str(Path(__file__).resolve().parent / "templates"),
    static_folder=str(Path(__file__).resolve().parent / "static"),
    static_url_path="/static",
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _vector_labels(vector_keys: list[str]) -> list[str]:
    """Translate vector keys to display labels for the template."""
    out = []
    for k in vector_keys:
        vec = mb.CONTENT_VECTORS.get(k)
        if vec:
            out.append(vec["name"])
    return out


def _vector_dropdown() -> list[dict[str, str]]:
    return [
        {"key": k, "name": v["name"]} for k, v in mb.CONTENT_VECTORS.items()
    ]


def _stage_dropdown() -> list[str]:
    return sorted(mb.STAGES.keys())


def _tactic_dropdown() -> list[str]:
    return sorted(mb.TACTICS.keys())


def _enriched_row(r: dict[str, Any]) -> dict[str, Any]:
    """Add display labels for vector keys before template render."""
    r = dict(r)  # shallow copy so we don't mutate the index
    r["vector_labels"] = _vector_labels(r.get("vectors", []))
    return r


def _enriched_cocktail(c: dict[str, Any]) -> dict[str, Any]:
    c = dict(c)
    c["vector_labels"] = _vector_labels(c.get("vectors", []))
    return c


def _enriched_canon(k: dict[str, Any]) -> dict[str, Any]:
    k = dict(k)
    k["vector_labels"] = _vector_labels(k.get("vectors", []))
    return k


def _enriched_positioning(p: dict[str, Any]) -> dict[str, Any]:
    p = dict(p)
    p["vector_labels"] = _vector_labels(p.get("vectors", []))
    return p


def _common_ctx() -> dict[str, Any]:
    """Context every template gets - nav links + vocab dropdowns."""
    idx = mb.load_index()
    return {
        "nav": [
            {"href": "/", "label": "Search"},
            {"href": "/icp", "label": "ICP & vectors"},
            {"href": "/canon", "label": "Canon"},
            {"href": "/guidelines", "label": "Guidelines"},
            {"href": "/howto", "label": "How to use"},
        ],
        "stats": {
            "positioning": idx.get("positioning_count", 0),
            "cocktails": idx.get("cocktail_count", 0),
            "canon": idx.get("canon_count", 0),
            "rows": idx.get("raw_row_count", 0),
            "version": idx.get("version", "?"),
        },
        "tactic_choices": _tactic_dropdown(),
        "stage_choices": _stage_dropdown(),
        "vector_choices": _vector_dropdown(),
    }


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------


@app.route("/healthz")
def healthz() -> tuple[str, int]:
    """No-auth liveness probe. Used by deploy.sh to confirm app is up."""
    try:
        idx = mb.load_index()
        return (f"ok rows={idx.get('raw_row_count', 0)}", 200)
    except Exception as e:  # pragma: no cover - defensive
        return (f"error {e}", 500)


@app.route("/")
def index():
    query = (request.args.get("q") or "").strip()
    ctx = _common_ctx()
    ctx["query"] = query
    ctx["detected_vectors"] = []

    if query:
        positioning = [_enriched_positioning(p) for p in mb.search_positioning(query, top_n=3)]
        cocktails = [_enriched_cocktail(c) for c in mb.search_cocktails(query, top_n=3)]
        canons = [_enriched_canon(k) for k in mb.search_canons(query, top_n=5)]
        rows = [_enriched_row(r) for r in mb.search(query, top_n=5)]
        ctx["positioning"] = positioning
        ctx["cocktails"] = cocktails
        ctx["canons"] = canons
        ctx["rows"] = rows
        ctx["detected_vectors"] = _vector_labels(mb.detect_vectors(query))
        ctx["any_results"] = bool(positioning or cocktails or canons or rows)
    else:
        ctx["positioning"] = []
        ctx["cocktails"] = []
        ctx["canons"] = []
        ctx["rows"] = []
        ctx["any_results"] = False

    return render_template("search.html", **ctx)


@app.route("/icp")
def icp_page():
    ctx = _common_ctx()
    idx = mb.load_index()
    positioning = [_enriched_positioning(p) for p in idx.get("positioning", [])]
    # Order anchors the same way the CLI does
    order = [
        "positioning_line", "icp_definition", "content_vector",
        "wall_rule", "founder_anchor", "forbids_list", "licenses_list",
        "voice_register", "never_name_brands",
    ]
    grouped: dict[str, list[dict[str, Any]]] = {kind: [] for kind in order}
    for p in positioning:
        if p["kind"] in grouped:
            grouped[p["kind"]].append(p)
        else:
            grouped.setdefault("other", []).append(p)
    ctx["positioning_groups"] = [(kind, grouped[kind]) for kind in order if grouped.get(kind)]
    return render_template("icp.html", **ctx)


@app.route("/tactic/<name>")
def tactic_page(name: str):
    ctx = _common_ctx()
    idx = mb.load_index()
    name_clean = re.sub(r"[^a-z0-9_]", "", name.lower().replace("-", "_"))
    if name_clean not in mb.TACTICS:
        abort(404, description=f"Tactic `{html.escape(name)}` not in vocabulary")
    cocktails = [_enriched_cocktail(c) for c in idx.get("cocktails", []) if name_clean in c.get("tactics", [])]
    canons = [_enriched_canon(k) for k in idx.get("canons", []) if name_clean in k.get("tactics", [])]
    rows = [_enriched_row(r) for r in idx.get("rows", []) if name_clean in r.get("tactics", [])]
    rows.sort(key=lambda r: (r.get("rank_stars", 0), int(r.get("easy_to_apply", False))), reverse=True)
    ctx["tactic_name"] = name_clean
    ctx["tactic_aliases"] = mb.TACTICS[name_clean]
    ctx["cocktails"] = cocktails
    ctx["canons"] = canons
    ctx["rows"] = rows[:20]
    return render_template("tactic.html", **ctx)


@app.route("/for-vector/<name>")
def vector_page(name: str):
    ctx = _common_ctx()
    canonical = mb.resolve_vector(name)
    if not canonical:
        abort(404, description=f"Vector `{html.escape(name)}` not recognised")
    bundle = mb.by_content_vector(canonical)
    vec = mb.CONTENT_VECTORS[canonical]
    ctx["vector_key"] = canonical
    ctx["vector_name"] = vec["name"]
    ctx["vector_description"] = vec["description"]
    ctx["vector_aliases"] = vec["aliases"]
    ctx["anchor"] = _enriched_positioning(bundle["anchor"]) if bundle.get("anchor") else None
    ctx["cocktails"] = [_enriched_cocktail(c) for c in bundle["cocktails"]]
    ctx["canons"] = [_enriched_canon(k) for k in bundle["canons"]]
    rows = [_enriched_row(r) for r in bundle["rows"]]
    rows.sort(key=lambda r: r.get("rank_stars", 0), reverse=True)
    ctx["rows"] = rows[:20]
    return render_template("vector.html", **ctx)


@app.route("/for-stage/<name>")
def stage_page(name: str):
    ctx = _common_ctx()
    canonical = mb.resolve_stage(name)
    if not canonical:
        abort(404, description=f"Stage `{html.escape(name)}` not in vocabulary")
    idx = mb.load_index()
    cocktails = [_enriched_cocktail(c) for c in idx.get("cocktails", []) if canonical in c.get("stages", [])]
    canons = [_enriched_canon(k) for k in idx.get("canons", []) if canonical in k.get("stages", [])]
    rows = [_enriched_row(r) for r in idx.get("rows", []) if canonical in r.get("stages", [])]
    rows.sort(key=lambda r: (r.get("rank_stars", 0), int(r.get("easy_to_apply", False))), reverse=True)
    ctx["stage_name"] = canonical
    ctx["stage_aliases"] = mb.STAGES[canonical]
    ctx["cocktails"] = cocktails
    ctx["canons"] = canons
    ctx["rows"] = rows[:20]
    return render_template("stage.html", **ctx)


@app.route("/canon")
def canon_page():
    ctx = _common_ctx()
    idx = mb.load_index()
    school_arg = (request.args.get("school") or "").lower()
    schools_alias = {
        "be": "behavioral_economics",
        "nstd": "nstd_voss",
        "voss": "nstd_voss",
        "cialdini": "cialdini_sutherland",
        "sutherland": "cialdini_sutherland",
    }
    canons = idx.get("canons", [])
    if school_arg:
        school_key = schools_alias.get(school_arg, school_arg)
        canons = [k for k in canons if k.get("school") == school_key]
        ctx["filter_school"] = school_arg
    else:
        ctx["filter_school"] = None
    # Group by school for nicer rendering
    grouped: dict[str, list[dict[str, Any]]] = {}
    labels: dict[str, str] = {}
    for k in canons:
        school = k["school"]
        grouped.setdefault(school, []).append(_enriched_canon(k))
        labels[school] = k.get("school_label", school)
    ctx["canon_groups"] = [(labels[s], grouped[s]) for s in grouped]
    return render_template("canon.html", **ctx)


@app.route("/guidelines")
def guidelines_page():
    ctx = _common_ctx()
    # Render content from positioning + brand-voice + voice-anti-patterns
    foundations_dir = REPO_ROOT / "00-foundations"
    files_to_render = [
        ("positioning", foundations_dir / "positioning.md"),
        ("brand_voice", foundations_dir / "brand-voice.md"),
        ("voice_anti_patterns", foundations_dir / "voice-anti-patterns.md"),
        ("regulatory_frames", foundations_dir / "regulatory-frames.md"),
    ]
    md = markdown.Markdown(extensions=["tables", "fenced_code", "toc"])
    contents = {}
    for key, path in files_to_render:
        if path.exists():
            md.reset()
            contents[key] = Markup(md.convert(path.read_text(encoding="utf-8")))
        else:
            contents[key] = Markup(f"<p><em>file not found: {html.escape(path.name)}</em></p>")
    ctx["contents"] = contents
    return render_template("guidelines.html", **ctx)


@app.route("/howto")
def howto_page():
    ctx = _common_ctx()
    return render_template("howto.html", **ctx)


@app.route("/stats")
def stats_page():
    ctx = _common_ctx()
    idx = mb.load_index()
    # Re-compute vector coverage like the CLI does
    vector_coverage: dict[str, dict[str, int]] = {
        k: {"cocktails": 0, "canons": 0, "rows": 0} for k in mb.CONTENT_VECTORS
    }
    for c in idx.get("cocktails", []):
        for v in c.get("vectors", []):
            if v in vector_coverage:
                vector_coverage[v]["cocktails"] += 1
    for k in idx.get("canons", []):
        for v in k.get("vectors", []):
            if v in vector_coverage:
                vector_coverage[v]["canons"] += 1
    for r in idx.get("rows", []):
        for v in r.get("vectors", []):
            if v in vector_coverage:
                vector_coverage[v]["rows"] += 1
    ctx["vector_coverage"] = [
        {
            "key": k,
            "name": mb.CONTENT_VECTORS[k]["name"],
            "cocktails": counts["cocktails"],
            "canons": counts["canons"],
            "rows": counts["rows"],
        }
        for k, counts in vector_coverage.items()
    ]

    tactic_counts: dict[str, int] = {}
    for r in idx.get("rows", []):
        for t in r.get("tactics", []):
            tactic_counts[t] = tactic_counts.get(t, 0) + 1
    ctx["top_tactics"] = sorted(tactic_counts.items(), key=lambda x: -x[1])[:15]
    return render_template("stats.html", **ctx)


@app.errorhandler(404)
def _not_found(e):
    ctx = _common_ctx()
    ctx["error_message"] = str(e.description) if hasattr(e, "description") else "Not found."
    return render_template("error.html", **ctx), 404


@app.errorhandler(500)
def _server_error(e):  # pragma: no cover - defensive
    ctx = _common_ctx()
    ctx["error_message"] = "Internal error. Check server logs."
    return render_template("error.html", **ctx), 500


if __name__ == "__main__":
    # Local dev only. Production runs via systemd + gunicorn (see deploy.sh).
    app.run(host="127.0.0.1", port=8081, debug=True)
