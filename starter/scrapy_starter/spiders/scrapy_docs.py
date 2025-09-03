from urllib.parse import urlsplit

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy_starter.items import ScrapyDocsItem


class ScrapyDocsSpider(CrawlSpider):
    name = "scrapy_docs"
    allowed_domains = ["docs.scrapy.org"]
    start_urls = ["https://docs.scrapy.org/en/latest/"]
    rules = (
        Rule(LinkExtractor(allow=(r"/en/[^#]*")), callback="parse_page", follow=True),
    )

    def parse_page(self, response):
        item = ScrapyDocsItem()
        item["url"] = response.url
        item["title"] = response.css("title::text").get()
        item["html"] = response.text
        parts = urlsplit(response.url).path.split("/")
        if len(parts) > 2:
            item["lang"] = parts[1]
            item["version"] = parts[2]
        item["content_type"] = response.headers.get("content-type", b"").decode()
        item["source"] = "scrapy-docs"
        return item
