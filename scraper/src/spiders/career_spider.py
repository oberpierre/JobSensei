from urllib.parse import urlsplit, urlunsplit, urlencode, parse_qs as urlparseqs
import scrapy

class CareerSpider(scrapy.Spider):
    name = "career"

    def start_requests(self):
        urls = [
            "https://www.google.com/about/careers/applications/jobs/results/136914285465871046-software-engineer-machine-learning-bard?q=engineer&hl=en_US&jlo=en_US&location=Zurich,+Switzerland&location=Singapore&sort_by=date",
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def next_page_url(self, url: str) -> str:
        # urlparts: (addressing scheme, network location, path, query, fragment identifier)
        urlparts = urlsplit(url)
        qs = urlparseqs(qs=urlparts[3])
        page = int(qs['page'][0]) if 'page' in qs else 1
        qs['page'] = [str(page + 1)]
        return urlunsplit([
            urlparts[0],
            urlparts[1],
            urlparts[2],
            urlencode(qs, doseq=True),
            urlparts[4]
        ])

    def parse(self, response):
        path = urlsplit(response.url)[2]
        if path.endswith('/jobs/results/'):
            for link in response.css("a[jsname='hSRGPd']"):
                if link.attrib['aria-label'].startswith('Learn more'):
                    yield response.follow(link.attrib['href'], callback=self.parse)

            next_page = response.css("button[jsname='ViaHrd']")
            if 'disabled' not in next_page.attrib:
                yield response.follow(self.next_page_url(response.url), callback=self.parse)
        else:
            for listing in response.css("div[jsname='tIk9qd']"):
                yield {
                    "url": response.url,
                    "content": ' '.join(listing.css("*::text").getall()),
                }
