# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import re
import cfscrape

from scrapy.loader.processors import MapCompose, Join
from scrapy.loader import ItemLoader  # 2
from scrapy.loader.processors import TakeFirst  # 3

from yts.items import YtsItem


class YtscrawlerSpider(CrawlSpider):
    name = "YTSCrawler"
    allowed_domains = ["yts.mx"]

    start_urls = ["https://yts.mx/browse-movies"]

    # Rules for horizontal and vertical crawling
    rules = (
        Rule(LinkExtractor(allow=r"/browse-movies")),
        Rule(
            LinkExtractor(restrict_xpaths='//*[@class="browse-movie-title"]'),
            callback="parsepage",
        ),
    )

    def parsepage(self, res):
        """This function parses a movie page.
        @url https://yts.mx/browse-movies
        @returns items 1
        @scrapes movie_title release_year genre imdb_rating
        @scrapes rating_count criticts audience magnet_link
        """

        try:
            cr = res.css("div.rating-row > span::text").re(r"\d+%")[0]
            au = res.css("div.rating-row > span::text").re(r"\d+%")[1]
        except IndexError:
            cr = None
            au = None

        # Create the loader using the response
        movie_loader = ItemLoader(item=YtsItem(), response=res)

        movie_loader.default_output_processor = TakeFirst()

        # Load fields using XPath expressions
        movie_loader.add_css(
            "movie_title",
            "div.row > div#movie-info.col-xs-10.col-sm-14.col-md-7.col-lg-8.col-lg-offset-1 > div.hidden-xs > h1::text",
            MapCompose(str.strip, str.title),
        )
        movie_loader.add_css(
            "release_year",
            "div.row > div#movie-info.col-xs-10.col-sm-14.col-md-7.col-lg-8.col-lg-offset-1 > div.hidden-xs > h2::text",
        )
        movie_loader.add_xpath(
            "genre", "/html/body/div[4]/div[3]/div[1]/div[4]/div[1]/h2[2]/text()",
        )
        movie_loader.add_css(
            "imdb_rating", 'div.rating-row > span[itemprop="ratingValue"]::text',
        )
        movie_loader.add_css(
            "rating_count", 'div.rating-row > span[itemprop="ratingCount"]::text',
        )
        movie_loader.add_value("criticts", cr)
        movie_loader.add_value("audience", au)
        movie_loader.add_css(
            "magnet_link",
            "div.modal-torrent a.magnet-download.download-torrent.magnet::attr(href)",
        )

        return movie_loader.load_item()
