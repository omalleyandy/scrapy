"""Item pipelines for the starter project."""

import hashlib
import re
from datetime import datetime
from pathlib import Path

import lxml.html


class MarkdownPipeline:
    """Convert HTML to Markdown and store it on disk."""

    def process_item(self, item, spider):  # type: ignore[override]
        html = item.get("html")
        if not html:
            return item

        item["sha1"] = hashlib.sha1(html.encode("utf-8")).hexdigest()  # noqa: S324
        root = lxml.html.fromstring(html)
        markdown = root.text_content()

        lang = item.get("lang", "en")
        version = item.get("version", "latest")
        slug = _slugify(item.get("title") or item["url"])  # type: ignore[arg-type]

        out_dir = Path("out") / "md" / lang / version
        out_dir.mkdir(parents=True, exist_ok=True)
        out_path = out_dir / f"{slug}.md"
        out_path.write_text(markdown, encoding="utf-8")

        item["md_path"] = str(out_path)
        item["fetched_at"] = datetime.utcnow().isoformat()
        item.pop("html", None)
        return item


def _slugify(value: str) -> str:
    value = value.lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-")
