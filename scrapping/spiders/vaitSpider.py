import scrapy

# spider for vait.ua web site
from scrapping.items import VaitItem


class vaitSpider(scrapy.Spider):
    name = "vait"
    allowed_domains = ["vait.ua"]
    start_urls = []

    color = ""
    collection = ""
    prod = ""
    minPrice = 0
    maxPrice = 0

    def __init__(self, color=None, collection=None, base=None, prod=None, minprice=None, maxprice=None, *args,
                 **kwargs):
        super(vaitSpider, self).__init__(*args, **kwargs)
        self.setColor(color)
        self.collection = collection
        self.setProd(prod)
        self.setBase(base)
        self.minPrice = minprice
        self.maxPrice = maxprice

    def parse(self, response):
        add_url = "https://www.vait.ua/"
        after_url = "?view_type=list"
        for quote in response.css('div.product').css('div.product_info'):
            product = quote.css('h3 a::attr(href)').extract_first()

            if product is not None:
                product = add_url + product
                yield scrapy.Request(product, callback=self.parseProduct)

        links = response.css('div.pagination a.next_page_link::attr(href)')
        links = links.extract()
        next_page = add_url + links[0] + after_url
        yield scrapy.Request(next_page, callback=self.parse)

    def parseProduct(self, response):
        product = response.css('div.description')
        name = response.xpath('//div[@class="product"]/h1/text()').extract()[0]
        price = product.css('span.price')
        price = price.css('span::text').extract()
        price = "".join(price)
        price = "".join(price.split())
        price = price.replace(".", "", 1)
        price = price.replace(",", ".", 1)
        pricef = self.get_num(price)
        passedPrice = 0
        if (self.minPrice is None or pricef >= float(self.minPrice)) and (
                self.maxPrice is None or pricef <= float(self.maxPrice)):
            passedPrice = 1
        image = response.css('div.product').css('div.image').css('a').css('img').xpath("@src").extract_first()
        if image is None:
            image = "https://pyrellas.gr/images/stories/virtuemart/product/no-photo.jpg"
        item = VaitItem()
        item['name'] = name
        item['url'] = response.url
        item['price'] = price
        item['image'] = image

        datas = []

        for row in response.xpath('//*[@class="features-table"]/tr'):
            field = row.xpath('th[1]//text()').extract_first()
            value = row.xpath('td[1]//text()').extract_first()
            data = (field, value)
            datas.append(data)

        item['data'] = datas
        if passedPrice == 1:
            yield item

    def setColor(self, color):
        if color == "red":
            self.color = "156=Красный/"
        if color == "green":
            self.color = "156=Зеленый/"
        if color == "white":
            self.color = "156=Белый/"
        if color == "yellow":
            self.color = "156=Желтый/"
        if color == "beige":
            self.color = "156=Бежевый/"
        if color == "brown":
            self.color = "156=Коричневый/"
        if color == "orange":
            self.color = "156=Оранжевый/"
        if color == "blue":
            self.color = "156=Синий/"
        if color == "gray":
            self.color = "156=Серый/"
        if color == "violet":
            self.color = "156=Фиолетовый/"
        if color == "black":
            self.color = "156=Черный/"
        if color == "bordo":
            self.color = "156=Бордовый/"
        if color == "light_blue":
            self.color = "156=Голубой/"
        if color == "gold":
            self.color = "156=Золотой/"
        if color == "pink":
            self.color = "156=Розовый/"
        if color == "silver":
            self.color = "156=Серебристый/"
        if color is None:
            self.color = ""

    def setBase(self, base):
        adding_str = ""
        if self.prod == "all":
            adding_str = "filter/" + self.color
        else:
            adding_str = self.prod + ";" + self.color
        if base == "acryl":
            self.start_urls.append("https://www.vait.ua/catalog/akrilovye-emali/" + adding_str + "?view_type=list")
        if base == "alkid":
            self.start_urls.append("https://www.vait.ua/catalog/sinteticheskie-odnokomponentnye-emali/" + adding_str + "?view_type=list")
        if base == "poli":
            self.start_urls.append("https://www.vait.ua/catalog/poliuretanovye-emali/" + adding_str + "?view_type=list")
        if base == "basecov":
            self.start_urls.append("https://www.vait.ua/catalog/bazovye-pokrytiya-metalliki/" + adding_str + "?view_type=list")
        if base is None:
            self.start_urls.append("https://www.vait.ua/catalog/avtoemali/" + adding_str + "?view_type=list")
        if base == "all":
            self.start_urls.append("https://www.vait.ua/catalog/avtoemali/" + adding_str + "?view_type=list")

    def setProd(self, prod):
        if prod == "Mobihel":
            prod = "mobihel-helios"
        if prod == "all":
            self.prod = prod
        else:
            self.prod = "filter/brand=" + str(prod).lower()


    def get_num(self, x):
        return float(''.join(ele for ele in x if ele.isdigit() or ele == '.'))
