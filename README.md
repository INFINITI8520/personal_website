# Personal Website

Static HTML/CSS site — no build step required.

## Structure

- `index.html` — About/home page
- `projects.html` — Project list
- `blog.html` — Blog index (links to posts)
- `blog/*.html` — Individual blog posts
- `css/style.css` — All styling

## Editing content

**About page:** edit the text directly in `index.html`, and update the GitHub/LinkedIn links.

**Add a project:** copy a `.project` block in `projects.html`, update the title, link, description, and tags.

**Add a blog post:**
1. Copy `blog/hello-world.html` to a new file, e.g. `blog/my-post.html`.
2. Edit the title, date, and content.
3. Add a link to it at the top of the list in `blog.html`.

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
