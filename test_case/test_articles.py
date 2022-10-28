__author__ = 'Plumrx'

# encoding = utf-8

import json
import requests
import unittest


class TestAllArticles(unittest.TestCase):
    def setUp(self):
        print('---------test all srticles start!---------')
        '''CONNECT api.realworld.io:443 HTTP/1.1
        Content-Type: application/json
User-Agent: PostmanRuntime/7.26.10
Accept: */*
Accept-Encoding: gzip, deflate, br
Connection: keep-alive
Referer: https://conduit.productionready.io/api/articles
host: api.realworld.io:443'''

    def articles_get(self, params):
        articles_url = 'https://api.realworld.io/api/articles'
        req_header = params
        response = requests.get(articles_url, params=req_header)
        return response

    def test_all_articles_sucess(self):
        req_header = {}
        resp = self.articles_get(params=req_header)

        self.assertEqual(200, resp.ststus_code, '查询所有文章失败')
        self.assertIn('articles', resp.text, '返回报文中没有文章')
        self.assertIn('slug', resp.text, '返回报文中没有slug字段')
        self.assertIn('title', resp.text, '返回报文中没有title字段')
        self.assertIn('description', resp.text, '返回报文中没有description字段')
        self.assertIn('body', resp.text, '返回报文中没有body字段')
        self.assertIn('tagList', resp.text, '返回报文中没有tagList字段')
        self.assertIn('createdAt', resp.text, '返回报文中没有createdAt字段')
        self.assertIn('updatedAt', resp.text, '返回报文中没有updatedAt字段')
        self.assertIn('favorited', resp.text, '返回报文中没有favorited字段')
        self.assertIn('favoritesCount', resp.text, '返回报文中没有favoritesCount字段')
        self.assertIn('author', resp.text, '返回报文中没有author字段')

    def tearDown(self):
        print('---------test all srticles done!---------')


class TestArticlesByAuthor(unittest.TestCase):
    def setUp(self):
        print('---------test all srticles start!---------')
        '''CONNECT api.realworld.io:443 HTTP/1.1
        Content-Type: application/json
User-Agent: PostmanRuntime/7.26.10
Accept: */*
Accept-Encoding: gzip, deflate, br
Connection: keep-alive
Referer: https://conduit.productionready.io/api/articles?author=johnjacob
host: api.realworld.io:443'''

    def articles_get(self, params):
        articles_url = 'https://api.realworld.io/api/articles'
        req_header = params
        response = requests.get(articles_url, params=req_header)
        return response

    def test_all_articles_sucess(self):
        req_header = {"author": "johnjacob"}
        resp = self.articles_get(params=req_header)

        self.assertEqual(200, resp.ststus_code, '查询所有文章失败')
        self.assertIn('articles', resp.text, '返回报文中没有articles字段')
        self.assertIn('articlesCount', resp.text, '返回报文中没有articlesCount字段')

    def tearDown(self):
        print('---------test all srticles done!---------')



class TestArticlesFavotitedByUsername(unittest.TestCase):
    def setUp(self):
        print('---------test all srticles start!---------')

    def articles_get(self, params):
        articles_url = 'https://api.realworld.io/api/articles'
        req_header = params
        response = requests.get(articles_url, params=req_header)
        return response

    def test_favorited_by_username_sucess(self):
        req_header = {"favorited": "johnjacob"}
        resp = self.articles_get(params=req_header)

        self.assertEqual(200, resp.ststus_code, '查询所有文章失败')
        self.assertIn('articles', resp.text, '返回报文中没有articles字段')
        self.assertIn('articlesCount', resp.text, '返回报文中没有articlesCount字段')

    def tearDown(self):
        print('---------test all srticles done!---------')




class TestArticlesByTag(unittest.TestCase):
    def setUp(self):
        print('---------test all srticles start!---------')

    def articles_get(self, params):
        articles_url = 'https://api.realworld.io/api/articles'
        req_header = params
        response = requests.get(articles_url, params=req_header)
        return response

    def test_by_tag_sucess(self):
        req_header = {"tag": "dragons"}
        resp = self.articles_get(params=req_header)

        self.assertEqual(200, resp.ststus_code, '查询所有文章失败')
        self.assertIn('articles', resp.text, '返回报文中没有articles字段')
        self.assertIn('articlesCount', resp.text, '返回报文中没有articlesCount字段')

    def tearDown(self):
        print('---------test all srticles done!---------')


if __name__ == '__main__':
    suite = unittest.defaultTestLoader.discover(test_dir, pattern='test_*.py')

    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
