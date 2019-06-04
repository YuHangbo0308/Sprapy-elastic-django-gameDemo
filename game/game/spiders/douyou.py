# -*- coding: utf-8 -*-
import re
import scrapy
from scrapy.http import Request
from game.items import Game

def getStr(list):
    str = ""
    for each in list:
        str += each
    return str

def getNewGame():
    game = Game()
    game["url"] = ""
    game["developer"]= ""
    game["gameContext"]= ""
    game["gameLanguage"]= ""
    game["gameName"]= ""
    game["gamePlatform"]= ""
    game["gameTitle"]= ""
    game["gameType"]= ""
    game["publishDate"]= ""
    game["publisher"]= ""
    game["tag"] = 2
    return game

class DouyouSpider(scrapy.Spider):
    name = 'douyou'
    allowed_domains = ['doyo.cn']
    start_urls = ['http://www.doyo.cn/wangluo/list']

    def parse(self, response):
        # yield Request(url='http://www.doyo.cn/wangluo/list', callback=self.wangyou)

        yield Request(url='http://www.doyo.cn/danji/list/3', callback=self.danji)
        # for each in response.xpath("//div[@id='list_game']/div[@class='list']/a"):
        #     gameurl = each.xpath("@href").extract()[0]
        #     # print(gameurl)
        #     yield Request(url='http://www.doyo.cn'+gameurl, callback=self.analysisGame)
        # nextpage = response.xpath("//div[@id='wrapper']/div[@id='p_right']/div[@id='list_game']/div[@class='change_page']/a[@class='next']/@href").extract()[0]
        # yield Request(url='http://www.doyo.cn'+nextpage, callback=self.parse)

    def wangyou(self, response):
        for each in response.xpath("//div[@id='list_game']/div[@class='list']/a"):
            gameurl = each.xpath("@href").extract()[0]
            # print(gameurl)
            yield Request(url='http://www.doyo.cn'+gameurl, callback=self.analysisWangyou)
        nextpage = response.xpath("//div[@id='wrapper']/div[@id='p_right']/div[@id='list_game']/div[@class='change_page']/a[@class='next']/@href").extract()[0]
        yield Request(url='http://www.doyo.cn'+nextpage, callback=self.wangyou)

    def analysisWangyou(self, response):
        str = ""
        game = getNewGame()
        game["url"] = response.url

        game["gameName"] = response.xpath("//div[@id='game_info']/div[@class='m wangluo_m']/h1/text()").extract()[0]

        gameTypeList = response.xpath("//div[@id='game_info']/div[@class='m wangluo_m']/div[@class='info']/div[1]/a/text()").extract()
        game["gameType"] = getStr(gameTypeList)
        gameTitleList = response.xpath("//div[@id='game_info']/div[@class='m wangluo_m']/div[@class='info']/div[2]/a/text()").extract()
        game["gameTitle"] = getStr(gameTitleList)
        developerList = response.xpath("//div[@id='game_info']/div[@class='m wangluo_m']/div[@class='info']/div[5]/a/text()").extract()
        game["developer"] = getStr(developerList)
        publisherList = response.xpath("//div[@id='game_info']/div[@class='m wangluo_m']/div[@class='info']/div[6]/a/text()").extract()
        game["publisher"] = getStr(publisherList)

        gameContext = ""
        gameContext = getStr(response.xpath(
                "//div[@id='page_box']/div[@id='page_left']/div[@id='game_introduction']/div[@class='content']/text()").extract())
        for each in response.xpath(
                "//div[@id='page_box']/div[@id='page_left']/div[@id='game_introduction']/div[@class='content']/p"):
            contextlist = each.xpath("text()").extract()
            for str in contextlist:
                gameContext += str
        for each in response.xpath(
                "//div[@id='page_box']/div[@id='page_left']/div[@id='game_introduction']/div[@class='content']/span"):
            contextlist = each.xpath("text()").extract()
            for str in contextlist:
                gameContext += str

        gameContext = gameContext.replace("\r\n", "")
        game["gameContext"] = gameContext
        # game["gameContext"] = response.xpath("//div[@id='page_box']/div[@id='page_left']/div[@id='game_introduction']/div[@class='content']/p/text()").extract()[0]
        yield game

    def danji(self, response):
            for each in response.xpath("//div[@id='list_game']/div[@class='list']/a"):
                gameurl = each.xpath("@href").extract()[0]
                # print(gameurl)
                yield Request(url='http://www.doyo.cn' + gameurl, callback=self.analysisDanji)

            nextpage = response.xpath(
                "//div[@id='wrapper']/div[@id='p_right']/div[@id='list_game']/div[@class='change_page']/a[@class='next']/@href").extract()[
                0]
            yield Request(url='http://www.doyo.cn' + nextpage, callback=self.danji)

    def analysisDanji(self, response):
            str = ""
            game = getNewGame()
            game["url"] = response.url

            game["gameName"] = response.xpath("//div[@id='game_info']/div[@class='m danji_m']/h1/text()").extract()[0]

            gameTypeList = response.xpath(
                "//div[@id='game_info']/div[@class='m danji_m']/div[@class='info']/div[4]/a/text()").extract()
            game["gameType"] = getStr(gameTypeList)

            gameTitleList = response.xpath(
                "//div[@id='game_info']/div[@class='m danji_m']/div[@class='info']/div[@class='b']/a")
            gameTitle = ""
            if(len(gameTitleList) >0):
                for each in gameTitleList:
                    gameTitle += getStr(each.xpath("text()").extract())

            game["gameTitle"] = gameTitle

            developerList = response.xpath(
                "//div[@id='game_info']/div[@class='m danji_m']/div[@class='info']/div[5]/a/text()").extract()
            game["developer"] = getStr(developerList)

            publishDateList = response.xpath(
                "//div[@id='game_info']/div[@class='m danji_m']/div[@class='info']/div[6]/span/a/text()").extract()
            game["publishDate"] = getStr(publishDateList)

            gameContext = ""
            gameContext += getStr(response.xpath(
                "//div[@id='page_box']/div[@id='page_left']/div[@id='game_introduction']/div[@class='content']/text()").extract())
            for each in response.xpath(
                    "//div[@id='page_box']/div[@id='page_left']/div[@id='game_introduction']/div[@class='content']/p"):
                contextlist = each.xpath("text()").extract()
                if len(contextlist) != 0:
                    gameContext += contextlist[0]
            for each in response.xpath(
                    "//div[@id='page_box']/div[@id='page_left']/div[@id='game_introduction']/div[@class='content']/span"):
                contextlist = each.xpath("text()").extract()
                if len(contextlist) != 0:
                    gameContext += contextlist[0]

            gameContext = gameContext.replace("\r\n", "")
            game["gameContext"] = gameContext
            # game["gameContext"] = response.xpath("//div[@id='page_box']/div[@id='page_left']/div[@id='game_introduction']/div[@class='content']/p/text()").extract()[0]
            yield game
