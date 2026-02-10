"""Example scraper for crawling the ArcGIS sitemap."""

import argparse
import json
from collections.abc import Iterator
from pathlib import Path

import requests
from lxml import etree, html

SITEMAP_INDEX_URL = "https://pro.arcgis.com/sitemap_index.xml"


def fetch_xml(url: str) -> etree._Element:
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return etree.fromstring(response.content)


def parse_sitemap(url: str) -> dict[str, object]:
    root = fetch_xml(url)
    ns = root.tag.split("}")[0].strip("{")
    urls: list[str] = [loc.text for loc in root.findall(".//{*}loc") if loc.text]
    sm_type = root.tag.split("}", 1)[1] if "}" in root.tag else root.tag
    selectors = {
        "loc_xpath": f".//{{{ns}}}loc",
    }
    return {"type": sm_type, "namespace": ns, "urls": urls, "selectors": selectors}


def scrape_page(url: str) -> dict[str, object]:
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    doc = html.fromstring(response.content)
    metadata = {
        meta.get("name") or meta.get("property"): meta.get("content")
        for meta in doc.xpath("//meta[@name or @property]")
        if meta.get("content")
    }
    text = " ".join(t.strip() for t in doc.xpath("//body//text()") if t.strip())
    code_examples = [pre.text_content() for pre in doc.xpath("//pre|//code")]
    images = doc.xpath("//img/@src")
    return {
        "url": url,
        "metadata": metadata,
        "text": text,
        "code_examples": code_examples,
        "images": images,
    }


def crawl(
    limit_per_sitemap: int = 5, limit_pages: int = 10
) -> Iterator[dict[str, object]]:
    index = parse_sitemap(SITEMAP_INDEX_URL)
    count = 0
    for sm_url in index["urls"][:limit_per_sitemap]:
        sm = parse_sitemap(sm_url)
        for page_url in sm["urls"][:limit_pages]:
            yield scrape_page(page_url)
            count += 1
            if count >= limit_pages:
                return


def items_to_markdown(items: list[dict[str, object]]) -> str:
    """Return markdown representing the scraped items."""
    lines: list[str] = []
    for i, item in enumerate(items, start=1):
        lines.append(f"# Page {i}: {item['url']}")

        metadata = item.get("metadata") or {}
        if metadata:
            lines.append("## Metadata")
            for k, v in metadata.items():
                lines.append(f"- **{k}**: {v}")

        text = item.get("text")
        if text:
            lines.append("## Text")
            lines.append(text)

        code_examples = item.get("code_examples") or []
        if code_examples:
            lines.append("## Code Examples")
            for code in code_examples:
                lines.append("```")
                lines.append(code.strip())
                lines.append("```")

        images = item.get("images") or []
        if images:
            lines.append("## Images")
            lines.extend(f"![image]({img})" for img in images)

        lines.append("")

    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, help="markdown output file")
    parser.add_argument("--limit-per-sitemap", type=int, default=5)
    parser.add_argument("--limit-pages", type=int, default=10)
    args = parser.parse_args()

    items = list(crawl(args.limit_per_sitemap, args.limit_pages))
    if args.output:
        args.output.write_text(items_to_markdown(items), encoding="utf-8")
    else:
        print(json.dumps(items, indent=2))


if __name__ == "__main__":
    main()
