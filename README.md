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
   date: 2026-11-14
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

## Editorial rules

- **Chart spacing (house rule, set by ysk 2026-11-14):** prose between
  consecutive graphics must run **800–1,200 Japanese characters** (or
  **160–240 English words**). Verify segment lengths before publishing;
  count prose only, excluding figure markup and captions.
- Numbers in charts must be real, sourced figures — same standard as the
  text. Interpretation may be poetry; data may not.
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
