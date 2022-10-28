__author__ = 'Plumrx'
# encoding = utf-8

import json
import requests
import unittest

class TestAllTags(unittest.TestCase):
    def setUp(self):
        print('---------test all tags start!---------')

    def tags_get(self, params):
        articles_url = 'https://api.realworld.io/api/tags'
        req_header = params
        response = requests.get(articles_url, params=req_header)
        return response

    def test_all_tags_sucess(self):
        req_header = {"author": "johnjacob"}
        resp = self.tags_get(params=req_header)

        self.assertEqual(200, resp.ststus_code, '查询所有文章失败')
        self.assertIn('tags', resp.text, '返回报文中没有tags字段')


    def tearDown(self):
        print('---------test all tags done!---------')





    if __name__ == '__main__':
        test_dir = '.'
        suite = unittest.defaultTestLoader.discover(test_dir, pattern='test_*.py')

        runner = unittest.TextTestRunner(verbosity=2)
        runner.run(suite)