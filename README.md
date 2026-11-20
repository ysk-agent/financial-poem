# Financial Poem（フィナンシャルポエム）

Bloomberg-style blog for "financial poems" — essays about the events that live
outside every precise model. Numbers are real; interpretation is poetry.

Site: https://ysk-agent.github.io/financial-poem/

Built with Astro. Deployed to GitHub Pages by GitHub Actions
(`.github/workflows/deploy.yml`, pnpm) on every push to `main`.

## Adding a new poem

1. Create `src/content/posts/<slug>.md` with frontmatter:

   ```markdown
   ---
   title: "タイトル"
   dek: "見出しの下に出る要約（デック）"
   date: 2026-11-14T09:00:00+09:00
   kicker: "Markets / Essay"
   author: "mio"
   tags: ["taco"]
   ---

   本文は Markdown で。## が記事内の見出しになります。
   ```

2. Commit and push. The newest post automatically becomes the lead story on
   the top page; older posts drop into the grid.

Frontmatter schema lives in `src/content.config.ts`. Set `draft: true` to
keep a post out of the build.

**Always give `date` a time of day** (JST, as above). The top page sorts by
`date` only, so posts that share a bare calendar date have no defined order
and a new post can land in the middle of older ones. The display format
shows the calendar date only, so the time is invisible to readers. Existing
posts were backfilled with their first-commit times on 2026-11-14 (moka).

## Editorial rules

- **Chart spacing (house rule, set by ysk 2026-11-20; supersedes the
  800–1,200 range set 2026-11-14):** prose between consecutive graphics
  should run **about 800 Japanese characters** (or **about 160 English
  words**). Verify segment lengths before publishing; count prose only,
  excluding figure markup and captions.
- Numbers in charts must be real, sourced figures — same standard as the
  text. Interpretation may be poetry; data may not.
- **Source check (set by ysk 2026-11-20, after the FOMC review was written
  from the 2025 minutes and published as the 2026 review):** event posts
  (tagged `fomc` / `minutes` / `earnings`, dated 2026-11-20 or later) must
  carry a `<!-- source-check -->` block declaring the primary source URL,
  the event date, the source's own date text, the chair, and the key
  numbers/phrases relied on. Run `python3 scripts/check-sources.py` before
  publishing; it also runs in CI and a failure blocks deployment. The
  script fetches the primary source and verifies the declared date text,
  chair, numbers and phrases against it, checks the URL's embedded date
  against the event date, rejects stale events (>45 days), and lints all
  posts for officeholder anachronisms (e.g. "パウエル議長" after Powell's
  chair term ended 2026-05-22).
- Chart SVGs must be valid XML. Escape `&` in labels (`M&A` → `M&amp;A`):
  an invalid SVG is still served with HTTP 200, but browsers refuse to
  render it. Run `sh scripts/check-svg.sh` before publishing.

## Local development

Package manager is **pnpm** (pinned by the `packageManager` field in
`package.json`; do not use npm or leave a `package-lock.json` behind).

```bash
pnpm install
pnpm dev    # http://localhost:4321/financial-poem/
pnpm build  # outputs dist/
```

## Posts

- 2026-11-14 — ヴォルデモートは転職した (`src/content/posts/voldemort-fx.md`)
