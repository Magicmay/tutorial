#! /usr/bin/env python3
# -*- coding:utf-8 -*-
from backend.libs.Util import Util

class CSDN2018BlogStar(object):
    index = 'csdn2018blogstar'
    es = Util.get_es()

    @classmethod
    def index_doc(cls,body):
        cls.es.index(index=cls.index, doc_type=cls.index, body=body)

    @classmethod
    def hot_key(cls):
        body = {
          "size": 0,
          "aggs": {
            "term_comment": {
              "terms": {
                "field": "blogstar_comment.Content",
                "size": 1000
              }
            }
          }
        }
        try:
            res = cls.es.search(index=cls.index, doc_type=cls.index, body=body)
        except Exception as e:
            print('查询失败 ', str(e))
            res = None
        return res

    @classmethod
    def match_all(cls):
        body = {
          "query": {
            "match_all": {}
          },
          "size": 1000
        }
        try:
            res = cls.es.search(index=cls.index, doc_type=cls.index, body=body)
        except Exception as e:
            print('查询失败 ', str(e))
            res = None
        return res

    @classmethod
    def count_doc(cls):
        try:
            res = cls.es.count(index=cls.index, doc_type=cls.index,)
        except Exception as e:
            print('查询失败 ', str(e))
            return 0
        return res['count']

    @classmethod
    def stats_aggs(cls,field):
        body = {
          "size": 0,
          "aggs": {
            "stats_"+field: {
              "stats": {
                "field": field
              }
            }
          }
        }
        try:
            res = cls.es.search(index=cls.index, doc_type=cls.index, body=body)
        except Exception as e:
            print('查询失败 ', str(e))
            res = None
        return res

    @classmethod
    def term_aggs(cls,field,size=10):
        body = {
          "size": 0,
          "aggs": {
            "term_"+field: {
              "terms": {
                "field": field,
                "size": size,
                "order": {
                  "_key": "desc"
                }
              }
            }
          }
        }
        try:
            res = cls.es.search(index=cls.index, doc_type=cls.index, body=body)
        except Exception as e:
            print('查询失败 ', str(e))
            res = None
        return res

    @classmethod
    def term_query(cls,field,value):
        body = {
          "query": {
            "bool": {
              "filter": {
                "term": {
                  field: value
                }
              }
            }
          }
        }

        try:
            res = cls.es.search(index=cls.index, doc_type=cls.index, body=body)
        except Exception as e:
            print('查询失败 ', str(e))
            res = None
        return res

    @classmethod
    def username_term_query(cls,field,value):
        body = {
          "query": {
            "bool": {
              "filter": {
                "term": {
                  field: value
                }
              }
            }
          },
          "_source": ["blogstar_comment.UserName"]
        }

        try:
            res = cls.es.search(index=cls.index, doc_type=cls.index, body=body)
        except Exception as e:
            print('查询失败 ', str(e))
            res = None
        return res

    @classmethod
    def stats_agg_year_2018(cls):
        body = {
          "aggs": {
            "term_username": {
              "terms": {
                "field": "blogstar_comment.UserName",
                "size": 10000
              },
              "aggs": {
                "year_2018": {
                  "nested": {
                    "path": "archives"
                  },
                  "aggs": {
                    "prefix_yesr": {
                      "filter": {
                        "prefix": {
                          "archives.year_month": "2018年"
                        }
                      },
                      "aggs": {
                        "sum_article_num": {
                          "sum": {
                            "field": "archives.article_num"
                          }
                        }
                      }
                    }
                  }
                }
              }
            },
            "stats_year_2018":{
              "stats_bucket": {
                "buckets_path": "term_username>year_2018>prefix_yesr>sum_article_num"
              }
            }
          },
          "size": 0
        }

        try:
            res = cls.es.search(index=cls.index, doc_type=cls.index, body=body)
        except Exception as e:
            print('查询失败 ', str(e))
            res = None
        return res