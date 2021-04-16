import scrapy

from scrapy.loader import ItemLoader

from ..items import BnatnItem
from itemloaders.processors import TakeFirst


class BnatnSpider(scrapy.Spider):
	name = 'bnatn'
	start_urls = ['http://www.bna.tn/site/fr/news.php?categorie_news=1&id_article=536']

	def parse(self, response):
		post_links = response.xpath('//div[@class="content_article"]/a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

		next_page = response.xpath('//li[@class="next"]/a/@href').getall()
		yield from response.follow_all(next_page, self.parse)

	def parse_post(self, response):
		title = response.xpath('//h1/span/text()').get()
		description = response.xpath('//div[@class="content_actu"]//text()[normalize-space()]').getall()
		description = [p.strip() for p in description if '{' not in p]
		description = ' '.join(description).strip()
		date = response.xpath('//div[@class="blog-carousel-meta"]/span/text()').get()

		item = ItemLoader(item=BnatnItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
