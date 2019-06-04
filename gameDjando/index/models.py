# -*- coding: utf-8 -*-
from django.db import models

from elasticsearch_dsl import DocType, Date, Nested, Boolean,\
    analyzer, Completion, Keyword, Text, Integer
from elasticsearch_dsl.analysis import CustomAnalyzer as _CustomAnalyzer
from elasticsearch_dsl.connections import connections

# Create your models here.
# 以下链接elasticsearch
connections.create_connection(hosts=["127.0.0.1"])
class CustomAnalyzer(_CustomAnalyzer):
    def get_analysis_definition(self):
        return {}

ik_analyzer = CustomAnalyzer("ik_max_word", filter=["lowercase"])
class GameType(DocType):
    # suggest字段类型定义为completion
    # string类型：text, keyword两种
    # 　　text类型：会进行分词，抽取词干，建立倒排索引
    # 　　keyword类型：就是一个普通字符串，只能完全匹配才能搜索到
    # 数字类型：long, integer, short, byte, double, float
    # 日期类型：date
    # bool(布尔)
    # 类型：boolean
    # binary(二进制)
    # 类型：binary
    # 复杂类型：object, nested
    # geo(地区)
    # 类型：geo - point, geo - shape
    # 专业类型：ip, competion
    url = Keyword()
    suggest = Completion(analyzer=ik_analyzer)
    # analyzer = "ik_max_word" 是以一种分词方式
    gameName = Text(analyzer="ik_max_word")
    # 动作啥的
    gameType = Keyword()
    # 开发商
    developer = Text(analyzer="ik_max_word")
    # 发行商
    publisher = Text(analyzer="ik_max_word")
    # 发售日期
    publishDate = Keyword()
    gameLanguage = Keyword()
    # 标签 魔幻 穿越啥的
    gameTitle = Text(analyzer="ik_max_word")
    gamePlatform = Keyword()
    # 游戏内容 对应故事背景
    gameContext = Text(analyzer="ik_max_word")

    class Meta:
        index = "test"
        doc_type = "game"
if __name__ == "__main__":
    GameType.init()