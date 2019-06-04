# -*- coding: utf-8 -*-
import re

import scrapy
from scrapy.http import Request

from game.items import Game
from game.utils.utils import Utils

class YouminSpider(scrapy.Spider):
    name = 'youmin'
    allowed_domains = ['gamersky.com']
    start_urls = ['http://ku.gamersky.com/release/pc_201904/']

    def parse(self, response):
        for each in response.xpath("//div[@class='center']/div[@class='Mid']/div[@class='Mid_L']/ul[@class='PF']/li[@class='lx1']"):
            game = Utils.getNewGame()
            game["gameName"] = each.xpath("div[@class='PF_1']/div[@class='tit']/a/text()").extract()[0]
            game["url"] = each.xpath("div[@class='PF_1']/div[@class='tit']/a/@href").extract()[0]
            publishDateList = each.xpath("div[@class='PF_1']/div[@class='txt'][1]/text()").extract()
            publishDate = Utils.getStr(publishDateList)
            game["publishDate"] = re.match("发行日期：(.*)","发行日期：2019-04-16").group(1)
            game["gameType"] = Utils.getStr(each.xpath("div[@class='PF_1']/div[@class='txt'][2]/a/text()").extract())
            developer = Utils.getStr(each.xpath("div[@class='PF_1']/div[@class='txt'][3]/text()").extract()[0])
            game["developer"] = re.match("制作发行：(.*)",developer).group(1)
            game["gameContext"] = Utils.getStr(each.xpath("div[@class='PF_1']/div[@class='Intr']/p/text()").extract()[0])
            yield game

        nextPage = response.xpath("//div[@class='center']/div[@class='Mid']/div[@class='Mid_L']/div[@class='MidL_2']/a[@class='ptn'][1]/@href").extract()[0]
        yield Request(url='http://ku.gamersky.com' + nextPage, callback=self.parse)

