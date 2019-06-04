# -*- coding: utf-8 -*-
import scrapy

def getStr(list):
    str = ""
    for each in list:
        str+=each
    return str
class UrltestSpider(scrapy.Spider):
    name = 'urltest'
    allowed_domains = ['www.doyo.cn']
    start_urls = ['http://www.doyo.cn/game/595']

    def parse(self, response):
        gameContext = ""
        gameContext += getStr(response.xpath(
            "//div[@id='page_box']/div[@id='page_left']/div[@id='game_introduction']/div[@class='content']/text()").extract())


        print(gameContext)