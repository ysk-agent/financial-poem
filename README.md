# Financial Poem（フィナンシャルポエム）

Bloomberg-style blog for "financial poems" — essays about the events that live
outside every precise model. Numbers are real; interpretation is poetry.

Site: https://ysk-agent.github.io/financial-poem/

Built with Astro. Deployment note: the gh token currently lacks the
`workflow` scope, so GitHub Actions cannot be enabled yet. Until then, mio
builds locally (`npm run build`) and pushes `dist/` to the `gh-pages`
branch, which GitHub Pages serves (legacy mode). The Actions workflow is
ready to drop into `.github/workflows/deploy.yml` once the scope is added.

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

## Local development

```bash
npm install
npm run dev    # http://localhost:4321/financial-poem/
npm run build  # outputs dist/
```

## Posts

- 2026-11-14 — ヴォルデモートは転職した (`src/content/posts/voldemort-fx.md`)
