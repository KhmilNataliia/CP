import scrapy

# spider for  shop.mobihel.ua web site
from scrapping.items import VaitItem


class avtomaliarSpider(scrapy.Spider):
    name = "avtomaliar"
    allowed_domains = ["avtomaliar.ua"]
    start_urls = []

    color = ""
    collection = ""
    minPrice = 0
    maxPrice = 0

    def __init__(self, color=None, collection=None, base=None, prod=None, minprice=None, maxprice=None, *args,
                 **kwargs):
        super(avtomaliarSpider, self).__init__(*args, **kwargs)
        self.setColor(color)
        self.collection = collection
        self.setProd(prod)
        self.setBase(base)
        self.minPrice = minprice
        self.maxPrice = maxprice

    def parse(self, response):
        for quote in response.css('div.name'):
            product = quote.css('a::attr(href)').extract_first()

            if product is not None:
                product = product
                yield scrapy.Request(product, callback=self.parseProduct)

        links = response.css('div.links a::attr(href)')
        links = links.extract()
        marks = response.css('div.links a::text').extract()
        idx = marks.index(">")
        if idx >= 0:
            next_page = links[idx]
            yield scrapy.Request(next_page, callback=self.parse)

    def parseProduct(self, response):
        product = response.css('div.product-info')
        name = response.xpath('//div[@class="product-info"]/h1/span/text()').extract_first()
        price = product.css('div.price')
        price = price.css('span::text').extract()
        price = "".join(price)
        price = "".join(price.split())
        pricef = self.get_num(price)
        passedPrice = 0
        if (self.minPrice is None or pricef >= float(self.minPrice)) and (
                self.maxPrice is None or pricef <= float(self.maxPrice)):
            passedPrice = 1
        image = response.css('div.product-info').css('div.share42init::attr(data-image)').extract_first()
        if image is None:
            image = "https://pyrellas.gr/images/stories/virtuemart/product/no-photo.jpg"
        item = VaitItem()
        item['name'] = name
        item['url'] = response.url
        item['price'] = price
        item['image'] = image

        datas = []

        for row in response.xpath('//*[@id="tab-description"]/div[4]/table/tbody/tr'):
            field = row.xpath('td[1]//text()').extract_first()
            value = row.xpath('td[2]//text()').extract_first()
            data = (field, value)
            datas.append(data)

        item['data'] = datas
        if passedPrice == 1:
            yield item

    def setColor(self, color):
        if color == "red":
            self.color = "gruppa-tsveta/krasnyj/"
        if color == "green":
            self.color = "gruppa-tsveta/zelenyj/"
        if color == "white":
            self.color = "gruppa-tsveta/belyj/"
        if color == "yellow":
            self.color = "gruppa-tsveta/zheltyj/"
        if color == "beige":
            self.color = "gruppa-tsveta/bezhevyj/"
        if color == "brown":
            self.color = "gruppa-tsveta/korichnevyj/"
        if color == "orange":
            self.color = "gruppa-tsveta/oranzhevyj/"
        if color == "blue":
            self.color = "gruppa-tsveta/sinij/"
        if color == "gray":
            self.color = "gruppa-tsveta/seryj/"
        if color == "violet":
            self.color = "gruppa-tsveta/fioletovyj/"
        if color == "black":
            self.color = "gruppa-tsveta/chernyj/"
        if color == "light_blue":
            self.color = "gruppa-tsveta/goluboj/"
        if color is None:
            self.color = ""

    def setBase(self, base):
        if base == "acryl":
            self.start_urls.append("https://avtomaliar.ua/1-lakokrasochnye-materialy/avtoemali/akrilovaya-kraska/" + self.prod + self.color)
        if base == "alkid":
            self.start_urls.append("https://avtomaliar.ua/1-lakokrasochnye-materialy/avtoemali/alkidnaya-kraska/" + self.prod + self.color)
        if base == "basecov":
            self.start_urls.append("https://avtomaliar.ua/1-lakokrasochnye-materialy/avtoemali/bazovaya-kraskametallik/" + self.prod + self.color)

    def setProd(self, prod):
        if prod == "all":
            self.prod = ""
        else:
            self.prod = str(prod).lower() + "/"


    def get_num(self, x):
        return float(''.join(ele for ele in x if ele.isdigit() or ele == '.'))

