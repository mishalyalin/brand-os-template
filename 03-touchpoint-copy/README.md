# Touchpoint copy

Owner: {{ YOUR_NAME }}.

This folder holds the verbatim customer-facing copy organised by channel. Subfolders:

- `emails/` - lifecycle, transactional, broadcast
- `sms/` - one-line texts
- `social/` - Instagram captions, TikTok scripts, ad creative

Every file should pin to a brand-voice version in the front matter:

```yaml
---
voice_version: voice-v1.0.0
last_updated: YYYY-MM-DD
status: draft | review | shipped
---
```

The Brain does not parse this folder as a source layer. It is downstream output. Cocktails (`01-canon/cocktail-recipes.md`) and decisions (`06-decisions/`) capture the patterns; this folder captures the rendered copy.
