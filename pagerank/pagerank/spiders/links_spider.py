import scrapy
from scrapy.http import Response


class LinksSpider(scrapy.Spider):
    name = "links"
    allowed_domains = [
        "soundcloud.com"
    ]
    start_urls = [
        "https://soundcloud.com/visionrecordings"
    ]
    custom_settings = {
        "DEPTH_LIMIT": 3
    }

    def parse(self, response: Response):
        links = response.css("a::attr(href)").getall()

        for i in range(len(links)):
            if not not links[i].startswith("http") or links[i].startswith(("/", "#")):
                links[i] = response.urljoin(links[i])

        yield {
            "parent": response.request.url,
            "children": [link for link in links if "soundcloud" in link]
        }
        for link in links:
            if not link.startswith("http"):
                continue
            yield scrapy.Request(link, callback=self.parse)
