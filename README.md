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

- **Chart density (house rule, set by ysk 2026-11-14):** insert one chart or
  graphic per **800 characters of Japanese** text, or per **160 words of
  English** text. A ~2,200-character poem therefore carries 2–3 graphics.
- Numbers in charts must be real, sourced figures — same standard as the
  text. Interpretation may be poetry; data may not.

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
