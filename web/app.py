"""Marketing Brain web interface.

Thin Flask wrapper over `tools/marketing_brain.py`. All search / scoring /
parsing logic lives in the CLI module; this file only translates HTTP
requests into Brain calls and renders results.

Designed for self-hosted deploy on any small VPS under an unguessable
subdomain. nginx in front handles HTTPS + HTTP basic auth + rate limiting.
The Flask app binds to 127.0.0.1:8081 only.

Routes:
    GET /                   - search page (renders results if ?q= present)
    GET /icp                - the 6 content vectors + ICP definition + walls
    GET /tactic/<name>      - everything tagged with this tactic
    GET /for-vector/<name>  - everything serving this content vector
    GET /for-stage/<name>   - everything tagged for this funnel stage
    GET /canon              - canon principles, optional ?school=
    GET /assets             - visual identity: colour, type, logo, photo direction
    GET /guidelines         - brand voice + the 7 hard rules
    GET /howto              - how to use the Brain from a fresh Claude session
    GET /stats              - index stats
    GET /healthz            - liveness probe (no auth, used by deploy script)

JSON API (mirror of HTML routes, returns application/json, same basic-auth):
    GET /api/search?q=<query>&top=<n>  - search across all 4 Brain layers
    GET /api/icp                       - positioning anchors (Layer 0)
    GET /api/canon?school=<key>        - canon principles, optional school filter
    GET /api/tactic/<name>             - everything tagged with this tactic
    GET /api/for-vector/<name>         - everything serving this content vector
    GET /api/for-stage/<name>          - everything tagged for this funnel stage
    GET /api/stats                     - index counts + version

The API surface is for tooling: David and your designer hit it from their own
codebases (Next.js site, Claude session, scripts) without cloning the
repo. Same basic-auth as HTML; pass `-u user:pass` to curl. Responses
are stable JSON keyed by record id - safe to consume from any client.

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
from flask import Flask, abort, jsonify, render_template, request
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


def _parse_manifesto() -> dict[str, Any]:
    """Read 00-foundations/manifesto.md and return rendered HTML + authored flag.

    Heuristic: the manifesto is considered "authored" once the placeholder
    `{{ HERO_LINE_1 }}` has been replaced with real content. Until then the
    home page renders an instructional stub instead of the manifesto.
    """
    manifesto_path = REPO_ROOT / "00-foundations" / "manifesto.md"
    if not manifesto_path.exists():
        return {"authored": False, "html": ""}
    content = manifesto_path.read_text(encoding="utf-8")
    if "{{ HERO_LINE_1 }}" in content:
        return {"authored": False, "html": ""}
    md = markdown.Markdown(extensions=["tables", "fenced_code"])
    return {"authored": True, "html": md.convert(content)}


def _common_ctx() -> dict[str, Any]:
    """Context every template gets - nav links + vocab dropdowns."""
    idx = mb.load_index()
    return {
        "nav": [
            {"href": "/", "label": "Manifesto"},
            {"href": "/search", "label": "Search"},
            {"href": "/icp", "label": "ICP & vectors"},
            {"href": "/canon", "label": "Canon"},
            {"href": "/assets", "label": "Assets"},
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
    """Home page renders the brand manifesto if authored, else a stub."""
    ctx = _common_ctx()
    manifesto = _parse_manifesto()
    ctx["manifesto_authored"] = manifesto["authored"]
    ctx["manifesto_html"] = Markup(manifesto["html"])
    return render_template("manifesto.html", **ctx)


@app.route("/search")
def search_page():
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


@app.route("/assets")
def assets_page():
    """Visual identity dashboard - template stub.

    In the brand-os-template version, this route renders a stub that documents
    what the page is supposed to surface (palette, type, wordmark rules,
    photography direction, social template, site-building directive) and how to
    populate it.

    When you fork the template for your brand, replace this handler to build a
    context dict with your locked visual-identity tokens (colour hex, typography
    weights, wordmark rules, photography do/dont, social template, site-building
    gates), then render the same template. A reference implementation does this
    for a real brand at the Brand OS upstream this template was extracted from.
    """
    ctx = _common_ctx()
    return render_template("assets.html", **ctx)


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


# ---------------------------------------------------------------------------
# JSON API routes - mirror of the HTML routes for programmatic clients
# (David's Claude session, your designer's Next.js site, scripts).  Same basic-auth.
# ---------------------------------------------------------------------------


def _json_meta() -> dict[str, Any]:
    """Common envelope metadata for all API responses."""
    idx = mb.load_index()
    return {
        "index_version": idx.get("version", "?"),
        "counts": {
            "positioning": idx.get("positioning_count", 0),
            "cocktails": idx.get("cocktail_count", 0),
            "canon": idx.get("canon_count", 0),
            "rows": idx.get("raw_row_count", 0),
        },
        "repo": "https://github.com/YOUR-ORG/YOUR-BRAND-OS-REPO",
        "endpoint_doc": "/howto",
    }


@app.route("/api/search")
def api_search():
    """Returns positioning + cocktails + canon + raw rows for a query.

    Query params:
        q (required): natural-language query
        top (optional, default 5): how many of each layer to return
    """
    query = (request.args.get("q") or "").strip()
    try:
        top = max(1, min(20, int(request.args.get("top") or 5)))
    except ValueError:
        top = 5

    if not query:
        return jsonify({
            "error": "missing query parameter `q`",
            "example": "/api/search?q=anchoring%20on%20PDP&top=5",
            "_meta": _json_meta(),
        }), 400

    positioning = [_enriched_positioning(p) for p in mb.search_positioning(query, top_n=top)]
    cocktails = [_enriched_cocktail(c) for c in mb.search_cocktails(query, top_n=top)]
    canons = [_enriched_canon(k) for k in mb.search_canons(query, top_n=top)]
    rows = [_enriched_row(r) for r in mb.search(query, top_n=top)]
    detected = _vector_labels(mb.detect_vectors(query))

    return jsonify({
        "query": query,
        "top": top,
        "detected_vectors": detected,
        "positioning": positioning,
        "cocktails": cocktails,
        "canons": canons,
        "rows": rows,
        "_meta": _json_meta(),
    })


@app.route("/api/icp")
def api_icp():
    idx = mb.load_index()
    positioning = [_enriched_positioning(p) for p in idx.get("positioning", [])]
    return jsonify({
        "positioning": positioning,
        "content_vectors": list(mb.CONTENT_VECTORS.values()),
        "_meta": _json_meta(),
    })


@app.route("/api/canon")
def api_canon():
    idx = mb.load_index()
    school_arg = (request.args.get("school") or "").lower()
    schools_alias = {
        "be": "behavioral_economics",
        "nstd": "nstd_voss",
        "voss": "nstd_voss",
        "cialdini": "cialdini_sutherland",
        "sutherland": "cialdini_sutherland",
        "llm": "llm_seo",
        "seo": "llm_seo",
        "geo": "llm_seo",
        "ai-seo": "llm_seo",
    }
    canons = idx.get("canons", [])
    if school_arg:
        school_key = schools_alias.get(school_arg, school_arg)
        canons = [k for k in canons if k.get("school") == school_key]
    canons = [_enriched_canon(k) for k in canons]
    return jsonify({
        "school": school_arg or None,
        "canons": canons,
        "_meta": _json_meta(),
    })


@app.route("/api/tactic/<name>")
def api_tactic(name: str):
    idx = mb.load_index()
    name_clean = re.sub(r"[^a-z0-9_]", "", name.lower().replace("-", "_"))
    if name_clean not in mb.TACTICS:
        return jsonify({
            "error": f"tactic `{html.escape(name)}` not in vocabulary",
            "vocabulary": sorted(mb.TACTICS.keys()),
            "_meta": _json_meta(),
        }), 404
    cocktails = [_enriched_cocktail(c) for c in idx.get("cocktails", []) if name_clean in c.get("tactics", [])]
    canons = [_enriched_canon(k) for k in idx.get("canons", []) if name_clean in k.get("tactics", [])]
    rows = [_enriched_row(r) for r in idx.get("rows", []) if name_clean in r.get("tactics", [])]
    rows.sort(key=lambda r: (r.get("rank_stars", 0), int(r.get("easy_to_apply", False))), reverse=True)
    return jsonify({
        "tactic": name_clean,
        "aliases": mb.TACTICS[name_clean],
        "cocktails": cocktails,
        "canons": canons,
        "rows": rows[:20],
        "_meta": _json_meta(),
    })


@app.route("/api/for-vector/<name>")
def api_vector(name: str):
    canonical = mb.resolve_vector(name)
    if not canonical:
        return jsonify({
            "error": f"vector `{html.escape(name)}` not recognised",
            "vocabulary": list(mb.CONTENT_VECTORS.keys()),
            "_meta": _json_meta(),
        }), 404
    bundle = mb.by_content_vector(canonical)
    vec = mb.CONTENT_VECTORS[canonical]
    rows = [_enriched_row(r) for r in bundle["rows"]]
    rows.sort(key=lambda r: r.get("rank_stars", 0), reverse=True)
    return jsonify({
        "vector": canonical,
        "name": vec["name"],
        "description": vec["description"],
        "aliases": vec["aliases"],
        "anchor": _enriched_positioning(bundle["anchor"]) if bundle.get("anchor") else None,
        "cocktails": [_enriched_cocktail(c) for c in bundle["cocktails"]],
        "canons": [_enriched_canon(k) for k in bundle["canons"]],
        "rows": rows[:20],
        "_meta": _json_meta(),
    })


@app.route("/api/for-stage/<name>")
def api_stage(name: str):
    canonical = mb.resolve_stage(name)
    if not canonical:
        return jsonify({
            "error": f"stage `{html.escape(name)}` not in vocabulary",
            "vocabulary": sorted(mb.STAGES.keys()),
            "_meta": _json_meta(),
        }), 404
    idx = mb.load_index()
    cocktails = [_enriched_cocktail(c) for c in idx.get("cocktails", []) if canonical in c.get("stages", [])]
    canons = [_enriched_canon(k) for k in idx.get("canons", []) if canonical in k.get("stages", [])]
    rows = [_enriched_row(r) for r in idx.get("rows", []) if canonical in r.get("stages", [])]
    rows.sort(key=lambda r: (r.get("rank_stars", 0), int(r.get("easy_to_apply", False))), reverse=True)
    return jsonify({
        "stage": canonical,
        "aliases": mb.STAGES[canonical],
        "cocktails": cocktails,
        "canons": canons,
        "rows": rows[:20],
        "_meta": _json_meta(),
    })


@app.route("/api/stats")
def api_stats():
    return jsonify(_json_meta())


@app.route("/api/explain")
def api_explain():
    """Question -> recommended cocktail + supporting canons + evidence rows + output contract.

    Mirrors `marketing_brain.py explain` CLI subcommand. Query params:
        q (required): natural-language question
    """
    question = (request.args.get("q") or "").strip()
    if not question:
        return jsonify({
            "error": "missing query parameter `q`",
            "example": "/api/explain?q=how%20do%20we%20re-engage%20cart%20abandoners",
            "_meta": _json_meta(),
        }), 400

    positioning = [_enriched_positioning(p) for p in mb.search_positioning(question, top_n=3)]
    cocktails = mb.search_cocktails(question, top_n=1)
    top_cocktail = _enriched_cocktail(cocktails[0]) if cocktails else None
    canons = [_enriched_canon(k) for k in mb.search_canons(question, top_n=3)]
    rows = [_enriched_row(r) for r in mb.search(question, top_n=3)]
    detected = _vector_labels(mb.detect_vectors(question))

    output_contract = [
        "Cite the primary source, not Phill / Nudge / VaultsGPT",
        "Short hyphens only - run `skills/marketing-apply-brand-voice/SKILL.md`",
        "Wall-1 check: no medicinal vocabulary (remedy / heal / wellness / cure)",
        "Wall-2 check: no salt-category / spice-category comparisons - use per-meal anchors",
        "Cocktail > canon principle > raw Vault row when picking what to ship",
        "If proposing a NEW cocktail (Layer 1 no-match), add to `01-canon/cocktail-recipes.md` AFTER the founder review",
    ]

    no_match = top_cocktail is None and not canons and not rows
    return jsonify({
        "question": question,
        "detected_vectors": detected,
        "positioning": positioning,
        "recommended_cocktail": top_cocktail,
        "canons": canons,
        "rows": rows,
        "no_match": no_match,
        "output_contract": output_contract,
        "_meta": _json_meta(),
    }), (200 if not no_match else 404)


@app.route("/api/list-tactics")
def api_list_tactics():
    """Return the tactic vocabulary (canonical name -> aliases)."""
    return jsonify({
        "tactics": {key: list(mb.TACTICS[key]) for key in sorted(mb.TACTICS.keys())},
        "_meta": _json_meta(),
    })


@app.route("/api/list-stages")
def api_list_stages():
    """Return the funnel-stage vocabulary (canonical name -> aliases)."""
    return jsonify({
        "stages": {key: list(mb.STAGES[key]) for key in sorted(mb.STAGES.keys())},
        "_meta": _json_meta(),
    })


@app.errorhandler(404)
def _not_found(e):
    # JSON for /api/* paths, HTML for everything else
    if request.path.startswith("/api/"):
        return jsonify({
            "error": str(e.description) if hasattr(e, "description") else "not found",
            "_meta": _json_meta(),
        }), 404
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
