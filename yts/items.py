# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose


class YtsItem(scrapy.Item):
    # define the fields for your item here like:
    movie_title = scrapy.Field()
    release_year = scrapy.Field()
    genre = scrapy.Field()
    imdb_rating = scrapy.Field()
    rating_count = scrapy.Field()
    criticts = scrapy.Field()
    audience = scrapy.Field()
    magnet_link = scrapy.Field()
