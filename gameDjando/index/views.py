# -*- coding: utf-8 -*-
import json
from django.shortcuts import render
from django.http import HttpResponse
from elasticsearch import Elasticsearch
from datetime import datetime
# Create your views here.
from index.models import GameType
import redis
# Create your views here.
client = Elasticsearch(hosts=["127.0.0.1"])
redis_cli = redis.StrictRedis()
def index(request):
    return render(request,'index.html')


def getIndex(request):
    topn_search_encoding = redis_cli.zrevrangebyscore("search_keywords_set", "+inf", "-inf", start=0, num=5)
    topn_search = []
    for search_word in topn_search_encoding:
        topn_search.append(search_word.decode())
    return render(request, 'index.html', {"topn_search":topn_search})



def search(request):
    # 获取搜索关键字
    key_words = request.GET.get("q", "")

    # 热门搜索,存到redis中的中文再输出是ascii编码形式，需要解码才能显示为中文
    redis_cli.zincrby("search_keywords_set", 1, key_words)
    topn_search_encoding = redis_cli.zrevrangebyscore("search_keywords_set", "+inf", "-inf", start=0, num=5)
    topn_search = []
    for search_word in topn_search_encoding:
        topn_search.append(search_word.decode())


    page = request.GET.get("p", "1")
    try:
        page = int(page)
    except:
        page = 1
    # 每个网站爬取数据量
    threedm_count = redis_cli.get("threedm_count")  # redis_cli.get("jobbole_count")
    douyou_count = redis_cli.get("douyou_count")
    youmin_count = redis_cli.get("youmin_count")
    start_time = datetime.now()
    # 根据关键字查找
    response = client.search(
        index="test",
        body={
            "query": {
                "multi_match": {
                    "query": key_words,
                    "fields": ["gameName", "gameContext", "gameTitle"]
                }
            },
            "from": (page - 1) * 10,
            "size": 10,
            # 对关键字进行高光标红处理
            "highlight": {
                "pre_tags": ['<span class="keyWord">'],
                "post_tags": ['</span>'],
                "fields": {
                    "gameName": {},
                    "gameContext": {}
                }
            }
        }
    )

    end_time = datetime.now()
    last_seconds = (end_time - start_time).total_seconds()
    total_nums = response["hits"]["total"]
    if (page % 10) > 0:
        page_nums = int(total_nums / 10) + 1
    else:
        page_nums = int(total_nums / 10)
    hit_list = []
    for hit in response["hits"]["hits"]:
        # print(hit)
        hit_dict = {}
        if "gameName" in hit["highlight"]:
            hit_dict["gameName"] = "".join(hit["highlight"]["gameName"])
        else:
            hit_dict["gameName"] = hit["_source"]["gameName"]
        if "gameContext" in hit["highlight"]:
            hit_dict["gameContext"] = "".join(hit["highlight"]["gameContext"])[:500]
        else:
            hit_dict["gameContext"] = hit["_source"]["gameContext"][:500]

        # hit_dict["create_date"] = hit["_source"]["create_date"]
        hit_dict["url"] = hit["_source"]["url"]
        hit_dict["score"] = hit["_score"]

        hit_list.append(hit_dict)

    return render(request, "result.html", {"page": page,
                                           "all_hits": hit_list,
                                           "key_words": key_words,
                                           "total_nums": total_nums,
                                           "page_nums": page_nums,
                                           "last_seconds": last_seconds,
                                           "threedm_count": int(threedm_count),
                                           "douyou_count":int(douyou_count),
                                           "youmin_count":int(youmin_count),
                                           "topn_search":topn_search
                                           })


def getSuggest(request):
    key_words = request.GET.get('s', '')
    re_datas = []
    if key_words:
        s = GameType.search()
        s = s.suggest('my_suggest', key_words, completion={
            "field": "suggest", "fuzzy": {
                "fuzziness": 2
            },
            "size": 10
        })
        suggestions = s.execute().suggest.my_suggest
        for match in suggestions[0].options:
            source = match._source
            re_datas.append(source["gameName"])
        # print(re_datas)
    return HttpResponse(json.dumps(re_datas), content_type="application/json")
