from sqlalchemy import create_engine, Column, Table, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (
    Integer, SmallInteger, String, Date, DateTime, Float, Boolean, Text, LargeBinary)

from scrapy.utils.project import get_project_settings

DeclarativeBase = declarative_base()


def db_connect():
    """
    Performs database connection using database settings from settings.py.
    Returns sqlalchemy engine instance
    """
    return create_engine(get_project_settings().get("CONNECTION_STRING"))


def create_table(queries):
    DeclarativeBase.metadata.create_all(queries)


class queryDB(DeclarativeBase):
    __tablename__ = "queries"

    id = Column(Integer, primary_key=True)
    name = Column('name', String(300))
    url = Column('url', String(300))
    price = Column('price', String(300))
    image = Column('image', String(300))
    availability = Column('availability', String(300))
    query = Column('query', String(300))


class dataDB(DeclarativeBase):
    __tablename__ = "data"

    id = Column(Integer, primary_key=True)
    param = Column('param', String(300))
    value = Column('value', String(300))
    query = Column('query', String(300))
    prod = Column('prod', Integer)
