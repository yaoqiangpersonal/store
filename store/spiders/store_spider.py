import scrapy


class StoreSpiderSpider(scrapy.Spider):
    name = 'store_spider'
    allowed_domains = ['store.hmv.com']
    proxy = "192.168.1.199:7890"

    def start_requests(self):
        
        for page in range(1,14):
            yield scrapy.Request(
                "https://store.hmv.com/store/film-tv/4k-ultra-hd-blu-ray-2-for-%c2%a330?sc_src=email_10684133&sc_lid=572380522&sc_uid=JJvo3RLLwB&sc_llid=36424&sc_eh=0dbf10fb4ec5d1ca1&utm_source=emarsys&utm_medium=Email&utm_campaign=Visual%3A+2+for+%C2%A330+4K+Ultra+HD%3A+Visual+07%2F04-2022-04-07+20%3A30%3A00-Newsletter&page=" + str(page),
                                meta={"proxy": self.proxy},
                                callback=self.parse
                                )

    def parse(self, response):

        if(response.url.find('page') > 0):

            yield from response.follow_all(response.css('.prod__img-link::attr(href)'), meta={"proxy": self.proxy})

        else:

            url = response.url
            id = url[url.rfind("/")+1:-1]
            
            price = response.css('.prod-info__price::text').get().replace('\r\n','').strip()
            barcode = response.css('.prod-info__sku span::text').get()
            details = response.css('.table-responsive td::text').getall()
            dic = dict()
            dic['url'] = url
            dic['name'] = id
            dic['price'] = price
            dic['barcode'] = barcode
            dic['details'] = details
            
            yield dic
