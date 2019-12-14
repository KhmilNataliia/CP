import subprocess
from sqlalchemy.orm import sessionmaker
from scrapping.models import queryDB, dataDB, db_connect, create_table


class search_utils():
    Items = []

    def connect(self):
        engine = db_connect()
        create_table(engine)
        self.Session = sessionmaker(bind=engine)

    def get_item(self, _id):
        item = None
        for i in self.Items:
            if i['_id'] == _id:
                item = i
        return item

    def get_items(self, collection):
        engine = db_connect()
        create_table(engine)
        Session = sessionmaker(bind=engine)
        session = Session()
        items = session.query(queryDB).filter_by(query=collection).all()
        for item in items:
            it = dict()
            it["_id"] = str(item.id)
            it["name"] = item.name
            it["price"] = item.price
            it["url"] = item.url
            it["image"] = item.image
            datas = session.query(dataDB).filter_by(prod=item.id).all()
            dt = []
            for data in datas:
                d = [data.param, data.value]
                dt.append(d)
            it["data"] = dt
            self.Items.append(it)

    def search(self, collection, color, prod, base, min_price, max_price):
        self.Items = []
        params = ' -a color=' + color + ' -a collection=' + collection + ' -a prod=' + prod + ' -a base=' + base + \
                 ' -a minprice=' + str(min_price) + ' -a maxprice=' + str(max_price)
        if ((prod == "Colomix" or prod == "Dalux" or prod == "all") and (
                color != "bordo" and color != "light_blue" and color != "gold"
                and color != "pink" and color != "silver") and (base != "poli" and base != "basecov")):
            subprocess.check_output('scrapy crawl autofarba' + params)
        if base is not None:
             subprocess.check_output('scrapy crawl avtomaliar' + params)
        subprocess.check_output('scrapy crawl vait' + params)

        self.get_items(self, collection)
        return self.Items
