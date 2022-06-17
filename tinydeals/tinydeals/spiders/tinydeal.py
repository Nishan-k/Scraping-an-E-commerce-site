from operator import ne
import scrapy


class TinydealSpider(scrapy.Spider):
    name = 'tinydeal'
    allowed_domains = ['web.archive.org']
    start_urls = ['https://web.archive.org/web/20190225123327/https://www.tinydeal.com/specials.html']

    def parse(self, response):
        products = response.xpath("//ul[@class='productlisting-ul']/div")
        for product in products:
            name = product.xpath("normalize-space(.//li/a/text())").get()
            new_price = product.xpath(".//li/div[2]/span[1]/text()").get()
            old_price = product.xpath(".//li/div[2]/span[2]/text()").get()


            yield {
                "Name": name.replace("\u00a0",""),
                "New Price": new_price,
                "Old Price": old_price
            }
        
        next_page = response.xpath("//a[@class='nextPage']/@href").get()
        if next_page:
            yield scrapy.Request(url = next_page, callback=self.parse)
