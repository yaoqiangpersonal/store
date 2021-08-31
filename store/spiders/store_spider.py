import scrapy


class StoreSpiderSpider(scrapy.Spider):
    name = 'store_spider'
    allowed_domains = ['store.hmv.com']
    proxy = "192.168.1.199:7890"

    def start_requests(self):
        
        for page in range(1,4):
            yield scrapy.Request(
                "https://store.hmv.com/store/promotions/3for_304kultrahd?sort=most_relevant%20desc&quantity=24&view=grid&categories=offers&offers=3%2Bfor%2B%C2%A330%2B4K%2BUltra%2BHD&page=" + str(page),
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
            dic['name'] = id
            dic['price'] = price
            dic['barcode'] = barcode
            dic['details'] = details
            
            yield dic
