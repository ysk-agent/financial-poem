# drafts/ — 予定投稿

未公開の原稿と投稿予定を置く場所。サイトには出ない（Astro が読むのは `src/content/posts/` のみ）。

## 運用

- 書きかけ・予約原稿は `drafts/<slug>.md` に、公開時と同じ frontmatter 形式で置く
- 公開するときは `src/content/posts/` へ移動して push するだけ（Actions が自動デプロイ）
- 投稿予定・ネタ帳は `drafts/schedule.md` に書く
- 日付が決まっている予約原稿は、ファイル名の先頭に日付を付ける（例: `2026-11-17-nvda-earnings-result.md`）

## 注意

- 図（SVG）は公開時に `public/charts/` へ。`scripts/check-svg.sh` で XML 妥当性を検証してから公開する
- 本文の図間 800〜1,200 字ルールはドラフト段階から意識する
