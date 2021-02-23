import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst
from datetime import datetime
from baumannbanquiers.items import Article


class BaumannbanquiersSpider(scrapy.Spider):
    name = 'baumannbanquiers'
    start_urls = ['https://www.baumann-banquiers.ch/de/publikationen/blog/archiv.php']

    def parse(self, response):
        links = response.xpath('//div[@class="col-12 col-md-8"]//a[@class="btn btn-primary"]/@href').getall()
        yield from response.follow_all(links, self.parse_article)

    def parse_article(self, response):
        if 'pdf' in response.url:
            return

        item = ItemLoader(Article())
        item.default_output_processor = TakeFirst()

        title = response.xpath('//h1/text()').get()
        if title:
            title = title.strip()

        date = response.xpath('//div[@class="col-10"]/text()').get()
        if date:
            date = date.strip()

        content = response.xpath('//div[@class="col-12 col-md-8"]//text()').getall()
        content = [text for text in content if text.strip()]
        content = "\n".join(content[1:]).strip()

        item.add_value('title', title)
        item.add_value('date', date)
        item.add_value('link', response.url)
        item.add_value('content', content)

        return item.load_item()
