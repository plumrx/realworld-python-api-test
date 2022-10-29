__author__ = 'Plumrx'

import time

# encoding = utf-8
import requests
import unittest


class TestCreateArtcles(unittest.TestCase):
    def setUp(self):
        print('---------test all create articles start!---------')

    def create_articles_post(self, header, body):
        articles_url = 'https://api.realworld.io/api/articles'
        req_header = header
        req_body = body
        response = requests.post(articles_url,headers=req_header, json=req_body)
        return response

    def test_create_articles_success(self):
        req_header = {"Host": "api.realworld.io",
                      "Authorization": "Token eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InBsdW1yeDZAcXEuY29tIiwidXNlcm5hbWUiOiJwbHVtcng2IiwiaWF0IjoxNjY2ODczOTM0LCJleHAiOjE2NzIwNTc5MzR9.rOjHf3uuJsywLq5OB1W0h9Wf3_x1-Eyhy4iKYAwmWZU"}
        title = str(time.time())
        req_body = {"article": {"title": title, "description": "Ever wonder how?", "body": "Very carefully.",
                                "tagList": ["training", "dragons"]}}
        resp = self.create_articles_post(req_header, req_body)

        print(resp.text)
        self.assertEqual(200, resp.status_code, '创建文章失败')
        self.assertIn('article', resp.text, '返回报文中没有article字段')
        self.assertIn(title, resp.text, '返回报文中没有title字段')

    def test_title_existed(self):
        req_header = {"Host": "api.realworld.io",
                      "Authorization": "Token eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InBsdW1yeDEzQHFxLmNvbSIsInVzZXJuYW1lIjoicGx1bXJ4MTMiLCJpYXQiOjE2NjY5NjU4NzcsImV4cCI6MTY3MjE0OTg3N30.NOUJDf0NO0pQl5bakKKUlryX7FNQp4X66NxlnrzXEE8"}
        req_body = {"article": {"title": "How to train your dragon", "description": "Ever wonder how?",
                                "body": "Very carefully.", "tagList": ["training", "dragons"]}}
        resp = self.create_articles_post(req_header, req_body)

        self.assertEqual(422, resp.status_code, '重复title文章发布异常')
        self.assertIn('errors', resp.text, '返回报文中没有errors字段')
        self.assertIn('title', resp.text, '返回报文中没有title字段')
        self.assertIn('must be unique', resp.text, '返回报文中没有错误信息字段')

    def test_token_expired(self):
        req_header = {"Host": "api.realworld.io",
                      "Authorization": "Token eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InBsdW1yeDZAcXEuY29tIiwidXNlcm5hbWUiOiJwbHVtcng2IiwiaWF0IjoxNjY2ODczOTM0LCJleHAiOjE2NzIwNTc5MzR9.rOjHf3uuJsywLq5OB1W0h9Wf3_x1-Eyhy4iKYAwmWZU"}
        req_body = {"article": {"title": "How to train your dragon", "description": "Ever wonder how?",
                                "body": "Very carefully.", "tagList": ["training", "dragons"]}}
        resp = self.create_articles_post(req_header, req_body)

        self.assertNotEqual('401', resp.status_code, '该接口对于token无有效期验证')
        self.assertIn('error', resp.text, '返回报文中没有errors字段')
        self.assertIn('missing authorization credentials', resp.text, '返回报文中没有错误信息字段')

    def tearDown(self):
        print('---------test create articles done!---------')

    if __name__ == '__main__':
        test_dir = '.'
        suite = unittest.defaultTestLoader.discover(test_dir, pattern='test_*.py')

        runner = unittest.TextTestRunner(verbosity=2)
        runner.run(suite)
