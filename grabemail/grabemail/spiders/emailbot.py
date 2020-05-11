import scrapy
import re
from ..items import GrabemailItem

class EmailbotSpider(scrapy.Spider):
    name = 'emailbot'

    #allowed_domains = ["localhost"]

    start_urls = [
        'https://detailed.com/50/'
    ]
    i = 0


    def parse(self, response):
        items = GrabemailItem()

        urls = response.css("a::attr(href)").extract()
        reobj = re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,6}\b", re.IGNORECASE)
        emailList = re.findall(reobj, response.css("html")[0].extract())

        items['emailList'] = emailList

        for url in urls:
            print(str(self.i) + " urls checked")
            if self.i>200:
                break
            if url.startswith("mailto") or \
                    url.startswith("http://account") or \
                    url.startswith("https://account") or\
                    url.startswith("http://accounts") or \
                    url.startswith("https://accounts"):
                continue
            yield response.follow(url, callback=self.parse)
            self.i +=1

        yield items