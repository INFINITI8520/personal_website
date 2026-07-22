# Personal Website

Static HTML/CSS site — no build step required.

## Structure

- `index.html` — About/home page
- `projects.html` — Project index (links to project pages)
- `projects/*.html` — Individual project pages
- `blog.html` — Blog index (links to posts)
- `blog/*.html` — Individual blog posts
- `css/style.css` — All styling
- `scripts/generate_index.py` — Rebuilds the lists in `blog.html`/`projects.html` from the files in `blog/`/`projects/`
- `scripts/hooks/pre-commit`, `scripts/install-hooks.sh` — Git hook that runs the script above automatically

## One-time setup (per clone)

Git doesn't version hooks, so run this once after cloning the repo:

```
sh scripts/install-hooks.sh
```

## Editing content

**About page:** edit the text directly in `index.html`, and update the GitHub/LinkedIn links.

**Add a project:**
1. Copy `projects/example-project.html` to a new file, e.g. `projects/my-project.html`.
2. Edit the title, the `date`/`tags`/`summary` meta tags in `<head>`, and the content.
3. That's it — `projects.html` regenerates automatically on your next commit.

**Add a blog post:**
1. Copy `blog/hello-world.html` to a new file, e.g. `blog/my-post.html`.
2. Edit the title, the `date`/`summary` meta tags in `<head>`, and the content.
3. That's it — `blog.html` regenerates automatically on your next commit.

Entries are sorted newest first by the `date` meta tag. You can also run
`python3 scripts/generate_index.py` manually any time to preview the update
without committing.

The list sections in `blog.html`/`projects.html` are wrapped in
`<!-- AUTO-GENERATED:START/END -->` markers — don't hand-edit content between
them, it gets overwritten.

## Preview locally

Open `index.html` directly in a browser, or run a local server from this folder:

```
python3 -m http.server 8000
```

Then visit `http://localhost:8000`.

## Deploying

Pushed to GitHub and served via GitHub Pages. See deployment steps in the setup conversation, or:

1. `git add . && git commit -m "message" && git push`
2. GitHub Pages redeploys automatically on push to the configured branch.
