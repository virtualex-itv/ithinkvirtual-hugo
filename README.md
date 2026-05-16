# iThinkVirtual Hugo

Hugo source for [ithinkvirtual.com](https://ithinkvirtual.com) — VMware, virtualization, and home lab blog.

## Requirements

- [Hugo](https://gohugo.io/) extended, 0.161.0 or newer
- [Node.js](https://nodejs.org/) — for the linters
- [Python](https://www.python.org/) 3.10+ — for the HTML→Markdown migration script

## Develop

Live-reload preview at <http://localhost:1313>:

```powershell
hugo server                # excludes drafts
hugo server --buildDrafts  # includes drafts
```

Create a new post (leaf bundle):

```powershell
hugo new posts/my-post-slug/index.md
```

This creates a folder `content/posts/my-post-slug/` containing an `index.md`. Drop any screenshots or images directly into that same folder and reference them inline as page-bundle resources:

```markdown
![alt text](image.png)
```

(For listing-card featured images, set `featured_image = "image.png"` in front matter — same rule, no path needed.)

## Publish

When the post is ready:

1. Flip `"draft": true` → `"draft": false` (or remove the field entirely) in the post's front matter.
2. Stage, commit, and push:

   ```powershell
   git add content/posts/my-post-slug
   git commit -m "feat(content): my post slug"
   git push
   ```

Cloudflare Pages auto-deploys on every push to `main`. The site is live ~30 seconds later.

## Build

```powershell
hugo --gc --minify
```

Output is written to `public/` (gitignored). Cloudflare Pages runs this command on every push to `main`.

## Lint

```powershell
# Python (scripts/)
python -m ruff check scripts/
python -m ruff format scripts/

# CSS / JS / JSON / YAML
npx prettier --check "**/*.{js,css,json,jsonc,yaml,yml}"

# Markdown
npx markdownlint-cli2 "content/**/*.md" "README.md"
```

Configs: [`ruff.toml`](ruff.toml), [`.prettierrc.json`](.prettierrc.json) + [`.prettierignore`](.prettierignore), [`.markdownlint.jsonc`](.markdownlint.jsonc). Hugo templates and front matter are validated by `hugo` at build time.

## Deploy

Live site runs on [Cloudflare Pages](https://pages.cloudflare.com/), auto-deploying on every push to `main`:

- Build command: `hugo --gc --minify`
- Output directory: `public`
- Environment variable: `HUGO_VERSION=0.161.0`

[`static/_headers`](static/_headers) and [`static/_redirects`](static/_redirects) are processed by Cloudflare's edge.

## Comments

New comments are powered by [Giscus](https://giscus.app/) against GitHub Discussions on this repo. Fill in the four `params.giscus*` keys in [`hugo.toml`](hugo.toml) — the [`giscus.html`](layouts/partials/giscus.html) partial only renders once all four are set.

Old WordPress comments are preserved in each post's JSON front matter and rendered separately under a "Historical Comments" heading via [`layouts/partials/historical-comments.html`](layouts/partials/historical-comments.html).

## Migration history

This repo was migrated from a WordPress site in May 2026. The HTML→Markdown converter lives at [`scripts/html_to_markdown.py`](scripts/html_to_markdown.py) and is idempotent — safe to re-run on individual files. The original `wordpress-export.xml` is gitignored and stays on disk locally.
