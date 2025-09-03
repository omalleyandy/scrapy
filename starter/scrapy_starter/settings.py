from __future__ import annotations

BOT_NAME = "scrapy_starter"

SPIDER_MODULES = ["scrapy_starter.spiders"]
NEWSPIDER_MODULE = "scrapy_starter.spiders"

ROBOTSTXT_OBEY = True
DOWNLOAD_DELAY = 0.5
CONCURRENT_REQUESTS_PER_DOMAIN = 8

ITEM_PIPELINES = {"scrapy_starter.pipelines.MarkdownPipeline": 300}

AUTOTHROTTLE_ENABLED = True
HTTPCACHE_ENABLED = True
