# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


from sqlalchemy.orm import sessionmaker
from scrapping.models import queryDB, dataDB, db_connect, create_table

from scrapy.conf import settings
from scrapy.exceptions import DropItem


class AutofarbaPipeline(object):
    db = None

    def __init__(self):
        """
                Initializes database connection and sessionmaker.
                Creates deals table.
                """
        engine = db_connect()
        create_table(engine)
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        """Save deals in the database.

                This method is called for every item pipeline component.
                """
        session = self.Session()
        querydb = queryDB()
        querydb.query = spider.collection
        querydb.url = item['url']
        querydb.name = item['name']
        querydb.price = item['price']
        querydb.image = item['image']
        #querydb.availability = item['availability']

        datadb = []
        for data in item['data']:
            dt = dataDB()
            dt.param = data[0]
            dt.value = data[1]
            dt.query = spider.collection
            datadb.append(dt)

        try:
            session.add(querydb)
            session.commit()
            f = session.query(queryDB).filter_by(query=querydb.query).all()
            id = f[len(f) - 1].id
            for d in datadb:
                d.prod = id
                session.add(d)
                session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

        return item
