import scrapy


class ScrapyDocsItem(scrapy.Item):
    url = scrapy.Field()
    title = scrapy.Field()
    html = scrapy.Field()
    content_type = scrapy.Field()
    lang = scrapy.Field()
    version = scrapy.Field()
    sha1 = scrapy.Field()
    fetched_at = scrapy.Field()
    source = scrapy.Field()
    md_path = scrapy.Field()
    pdf_path = scrapy.Field()
