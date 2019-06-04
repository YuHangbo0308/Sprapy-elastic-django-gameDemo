# -*- coding: utf-8 -*-
import re
import time

import scrapy
from scrapy.http import Request
from game.items import Game


def getStr(list):
    if (len(list) > 0):
        return list[0]
    return ""

class A3dmSpider(scrapy.Spider):
    name = '3dm'
    allowed_domains = ['3dmgame.com']
    start_urls = ['https://dl.3dmgame.com/all_all_1_hot/']


    def parse(self, response):
        for each in response.xpath("//div[@class='listwrap']/ul/li"):
            gameurl = each.xpath("div/a/@href").extract()[0]
            # print(gameurl)
            yield Request(url=gameurl,callback=self.analysisGame)
        url = response.xpath("/html/body/div[@class='content']/div[@class='listwrap']/div[@class='pagewrap']/ul[@class='pagination']/li[@class='next']/a/@href").extract()[0]
        yield Request(url=url , callback=self.parse)

    def analysisGame(self, response):
        str = ""
        game = Game()
        game["tag"] = 1
        game["url"] = response.url
        str = response.xpath("/html/body/div[@class='content clear game']/div[@class='gameinfo']/div[@class='name']/h1/text()").extract()[0]
        str = re.match("《(.*)》|(.*)\s", str).group(1)
        game["gameName"] = str

        gameType = response.xpath("/html/body/div[@class='content clear game']/div[@class='gameinfo']/ul[@class='list']/li[1]/span/text()").extract()
        game["gameType"] =getStr(gameType)
        # 开发发行商
        str = response.xpath("/html/body/div[@class='content clear game']/div[@class='gameinfo']/ul[@class='list']/li[2]/span/text()").extract()[0]
        re_result = re.match("(.*)\|(.*)",str)
        game["developer"] = re_result.group(1)
        game["publisher"] = re_result.group(2)
        # 发布日期游戏平台

        publishDateList= response.xpath(
            "/html/body/div[@class='content clear game']/div[@class='gameinfo']/ul[@class='list']/li[3]/span/text()").extract()
        game["publishDate"] = getStr(publishDateList)
        # if len(publishDateList):
        #     game["publishDate"] = publishDateList[0]
        # else:
        #     game["publishDate"] = ""
        gamePlatformList = response.xpath(
            "/html/body/div[@class='content clear game']/div[@class='gameinfo']/ul[@class='list']/li[5]/span/text()").extract()[0]

        game["gamePlatform"] = getStr(gamePlatformList)
        # 游戏标签
        node = response.xpath("/html/body/div[@class='content clear game']/div[@class='gameinfo']/ul[@class='list']/li[7]")
        str = ""
        for each in node.xpath("//i/a"):
            str = str + each.xpath("text()").extract()[0]
            str += " "
        game["gameTitle"] = str

        gameLanguageList = response.xpath("/html/body/div[@class='content clear game']/div[@class='gameinfo']/ul[@class='list']/li[8]/span/text()").extract()[0]
        game["gameLanguage"] = getStr(gamePlatformList)

        gameContext = ""
        for each in response.xpath("/html/body/div[@class='content clear game']/div[@class='Content_L']/div[@class='GmL_1']/p[@style='text-indent:2em;']"):
            contextlist = each.xpath("text()").extract()
            if len(contextlist) != 0:
                gameContext += contextlist[0]

        gameContext = gameContext.replace("\r\n\r\n","")
        game["gameContext"] = gameContext
        # game["gameImg"] = response.xpath("/html/body/div[@class='content clear game']/div[@class='gameinfo']/div[@class='img']/img/@src").extract()[0]
        yield game

