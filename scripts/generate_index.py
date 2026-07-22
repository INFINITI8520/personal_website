#!/usr/bin/env python3
"""
Regenerates the auto-generated list sections in blog.html and projects.html
by scanning the blog/ and projects/ folders for entries.

Each entry file (blog/*.html or projects/*.html) is expected to have:
  - a <title>...</title> tag (the site suffix, e.g. " — Darius Chan", is stripped)
  - <meta name="date" content="YYYY-MM-DD">
  - <meta name="summary" content="...">
  - projects only: <meta name="tags" content="Comma, separated, list">

Entries are sorted by date, newest first. Content between the
"<!-- AUTO-GENERATED:START -->" / "<!-- AUTO-GENERATED:END -->" markers
in blog.html / projects.html is replaced; nothing else in those files is touched.

Run manually with:  python3 scripts/generate_index.py
It also runs automatically via the git pre-commit hook.
"""

import html
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
START_MARKER = "<!-- AUTO-GENERATED:START -->"
END_MARKER = "<!-- AUTO-GENERATED:END -->"


def get_meta(content, name):
    m = re.search(
        rf'<meta\s+name=["\']{name}["\']\s+content=["\'](.*?)["\']\s*/?>',
        content,
        re.IGNORECASE,
    )
    return html.unescape(m.group(1).strip()) if m else ""


def get_title(content):
    m = re.search(r"<title>(.*?)</title>", content, re.IGNORECASE | re.DOTALL)
    if not m:
        return ""
    title = m.group(1).strip()
    # Strip the trailing " — Darius Chan" (or similar em-dash suffix) if present.
    title = re.sub(r"\s*—\s*[^—]+$", "", title)
    return html.unescape(title)


def format_date(iso_date):
    try:
        from datetime import datetime

        return datetime.strptime(iso_date, "%Y-%m-%d").strftime("%B %-d, %Y")
    except (ValueError, TypeError):
        return iso_date or ""


def load_entries(folder):
    entries = []
    if not folder.is_dir():
        return entries
    for f in sorted(folder.glob("*.html")):
        content = f.read_text(encoding="utf-8")
        entries.append(
            {
                "file": f,
                "href": f"{folder.name}/{f.name}",
                "title": get_title(content),
                "date": get_meta(content, "date"),
                "summary": get_meta(content, "summary"),
                "tags": get_meta(content, "tags"),
            }
        )
    # Newest first. Entries without a date sort last.
    entries.sort(key=lambda e: e["date"] or "", reverse=True)
    return entries


def render_blog_list(entries):
    if not entries:
        return '<ul class="post-list">\n        <li>No posts yet.</li>\n      </ul>'
    items = []
    for e in entries:
        items.append(
            f'        <li>\n'
            f'          <span class="date">{format_date(e["date"])}</span>\n'
            f'          <a href="{e["href"]}">{e["title"]}</a>\n'
            f'        </li>'
        )
    return '<ul class="post-list">\n' + "\n".join(items) + "\n      </ul>"


def render_project_list(entries):
    if not entries:
        return '<ul class="project-list">\n        <li>No projects yet.</li>\n      </ul>'
    items = []
    for e in entries:
        summary = f"\n          <p>{e['summary']}</p>" if e["summary"] else ""
        items.append(
            f'        <li>\n'
            f'          <span class="tags">{e["tags"]}</span>\n'
            f'          <a href="{e["href"]}">{e["title"]}</a>{summary}\n'
            f'        </li>'
        )
    return '<ul class="project-list">\n' + "\n".join(items) + "\n      </ul>"


def replace_section(page_path, rendered):
    content = page_path.read_text(encoding="utf-8")
    if START_MARKER not in content or END_MARKER not in content:
        print(f"warning: markers not found in {page_path}, skipping", file=sys.stderr)
        return False
    pattern = re.compile(
        re.escape(START_MARKER) + r".*?" + re.escape(END_MARKER), re.DOTALL
    )
    new_content = pattern.sub(
        f"{START_MARKER}\n      {rendered}\n      {END_MARKER}", content
    )
    if new_content != content:
        page_path.write_text(new_content, encoding="utf-8")
        return True
    return False


def main():
    changed = []

    blog_entries = load_entries(ROOT / "blog")
    if replace_section(ROOT / "blog.html", render_blog_list(blog_entries)):
        changed.append("blog.html")

    project_entries = load_entries(ROOT / "projects")
    if replace_section(ROOT / "projects.html", render_project_list(project_entries)):
        changed.append("projects.html")

    if changed:
        print("Updated: " + ", ".join(changed))
    else:
        print("Already up to date.")


if __name__ == "__main__":
    main()
