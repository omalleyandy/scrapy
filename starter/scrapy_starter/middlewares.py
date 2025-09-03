from __future__ import annotations


class ScrapyStarterSpiderMiddleware:
    @classmethod
    def from_crawler(cls, crawler):
        return cls()

    def process_spider_input(self, response, spider):  # type: ignore[unused-argument]
        return None


class ScrapyStarterDownloaderMiddleware:
    @classmethod
    def from_crawler(cls, crawler):
        return cls()

    def process_request(self, request, spider):  # type: ignore[unused-argument]
        return None
