import scrapy


# spider for autofarba.com web site
from scrapping.items import AutofarbaItem


class autofarbaSpider(scrapy.Spider):
    name = "autofarba"
    allowed_domains = ["autofarba.com"]
    start_urls = [
        'http://autofarba.com/autofarba/automobil/',
    ]
    color = ""
    collection = ""
    base = ""
    prod = ""
    minPrice = 0
    maxPrice = 0

    def __init__(self, color=None, collection=None, base=None, prod=None, minprice=None, maxprice=None, *args, **kwargs):
        super(autofarbaSpider, self).__init__(*args, **kwargs)
        self.setColor(color)
        self.collection = collection
        self.setBase(base)
        self.setProd(prod)
        self.minPrice = minprice
        self.maxPrice = maxprice

    def parse(self, response):
        for quote in response.css('div.product-block-info'):
            product = quote.css('h3.name a::attr(href)').extract_first()

            if product is not None:
                yield scrapy.Request(product, callback=self.parseProduct)
        links = response.css('div.links a::attr(href)')
        links = links.extract()
        marks = response.css('div.links a::text').extract()
        idx = marks.index(">")
        if idx >= 0:
            next_page = links[idx]
            yield scrapy.Request(next_page, callback=self.parse)

    def parseProduct(self, response):
        name = response.xpath('//div[@class="col-lg-5 col-sm-6"]/h1/text()').extract()[0]
        price = response.css('div.price::text').extract()[0]
        price = "".join(price.split())
        availability = response.css('div.description::text').extract()[3]
        image = response.css('img.product-image-zoom').xpath("@src").extract_first()
        if image is None:
            image = "https://pyrellas.gr/images/stories/virtuemart/product/no-photo.jpg"
        item = AutofarbaItem()
        item['name'] = name
        item['url'] = response.url
        item['price'] = price
        item['availability'] = availability
        item['image'] = image
        datas = []
        product = response.css('table.attribute')
        all = product.xpath('//*[@id="tab-attribute"]/table/tbody/tr[position()>0]/td[position()>0]/text()').extract()
        i = 0
        pricef = self.get_num(price)
        passedPrice = 0
        if (pricef >= float(self.minPrice) or self.minPrice is None) and (pricef <= float(self.maxPrice) or self.maxPrice is None):
            passedPrice = 1
        passedCol = 0
        passedBase = 0
        passedProd = 0
        for fld in all:
            if i % 2 == 0:
                field = fld
            else:
                value = fld
                if field == "Колір фарби" and value == self.color:
                    passedCol = 1
                if field == "Хімічна основа" and value == self.base:
                    passedBase = 1
                if field == "Виробник" and value == self.prod:
                    passedProd = 1
                data = (field, value)
                datas.append(data)
            i = i + 1

        if self.color == "all":
            passedCol = 1
        if self.base == "all":
            passedBase = 1
        if self.prod == "all":
            passedProd = 1
        item['data'] = datas
        if passedCol == 1 and passedBase == 1 and passedProd == 1 and passedPrice == 1:
            yield item

    def setColor(self, color):
        if color == "red":
            self.color = "Червона"
        if color == "green":
            self.color = "Зелена"
        if color == "white":
            self.color = "Біла"
        if color == "yellow":
            self.color = "Жовта"
        if color == "beige":
            self.color = "Бежева"
        if color == "brown":
            self.color = "Коричнева"
        if color == "orange":
            self.color = "Помаранчева"
        if color == "blue":
            self.color = "Синя"
        if color == "gray":
            self.color = "Сіра"
        if color == "violet":
            self.color = "Фіолетова"
        if color == "black":
            self.color = "Чорна"
        if color is None:
            self.color = "all"

    def setBase(self, base):
        if base == "acryl":
            self.base = "Акрилова"
        if base == "alkid":
            self.base = "Алкідна"
        if base is None:
            self.base = "all"
        if base == "all":
            self.base = "all"

    def setProd(self, prod):
        self.prod = prod

    def get_num(self, x):
        return float(''.join(ele for ele in x if ele.isdigit() or ele == '.'))
