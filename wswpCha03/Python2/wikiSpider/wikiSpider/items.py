"""
Define here the models for our scraped items
"""
from scrapy import Item, Field

class Article(Item):
    """
    Define the fields for our item here like:
    `name = scrapy.Field()`
    """
    title = Field()
