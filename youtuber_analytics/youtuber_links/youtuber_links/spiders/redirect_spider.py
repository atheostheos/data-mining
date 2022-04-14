import scrapy


class RedirectSpider(scrapy.Spider):
    name = "redirect"

    custom_settings = {
        "DEPTH_LIMIT": 30
    }

    def start_requests(self):
        with open("..//statistics/links") as f:
            links = f.read().splitlines()
        for link in links:
            yield scrapy.Request(link,
                                 callback=self.parse)

    def parse(self, response):
        if response.status in [301, 302] and 'Location' in response.headers:
            yield scrapy.Request(
                response.urljoin(response.headers['Location']),
                callback=self.parse)
        yield {
            "end_url": response.url
        }
