__author__ = 'Plumrx'

# encoding = utf-8

import json
import requests
import unittest


class Testarticles(unittest.TestCase):
    def setUp(self):
        print('---------test start!---------')

    def test_all_articles(self):
        url = 'https://api.realworld.io/api/articles'
        req_header = {





        }
        response=requests.get(url,headers=req_header)

        print('状态码：'+str(response.status_code))
        print('返回报文：' + response.text)
