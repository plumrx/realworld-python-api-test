__author__ = 'Plumrx'

# time =
# encoding = utf-8
# file = .py
import unittest
import json
import requests
import time


class Testrespister(unittest.TestCase):
    def setUp(self):
        print('---------test start!---------')

    def respister_post(self, email, password, username):
        respister_url = 'https://api.realworld.io/api/users'
        req_header = {}
        req_body = {"user": {"email": email, "password": password, "username": username}}
        response = requests.post(respister_url, headers=req_header, json=req_body)
        return response

    def test_success(self):
        user = str(int(time.time()) * 1000)
        resp = self.respister_post(user + '@qq.com', 'plumrx', user)
        print('Response内容：' + resp.text)

        self.assertEqual(200, resp.status_code, '注册失败！')
        self.assertIn(user + '@qq.com', resp.text, '响应不包含用户名')
        self.assertIn(user, resp.text, '响应不包含邮箱')

        # 将注册获取的 token 写入文件中
        resp_token=resp.json()['user']['token']
        print('****************'+resp_token)
        f = open('token.txt', 'a')
        f.write(resp_token+'\n')
        f.close()

        
    @unittest.skip('no reason')
    def test_username_repeat(self):
        resp = self.respister_post('plumrx5@qq.com', 'plumrx', 'plumrx5')
        print('Response内容：' + resp.text)

        self.assertEqual(422, resp.status_code, '重复用户名验证失败！')
        self.assertIn('has already been taken', resp.text, '重复用户名验证失败！')

    @unittest.skip('no reason')
    def test_email_empty(self):
        resp = self.respister_post('', 'plumrx', 'plumrx5')

        self.assertEqual(422, resp.status_code, '空邮箱验证失败！')
        self.assertIn('can\'t be blank', resp.text, '空邮箱验证失败！')

    # def test_(self):
    # def test_(self):

    # def test_

    def tearDown(self):
        print('---------test end!-----------')


if __name__ == '__main__':
    test_dir = '.'
    suite = unittest.defaultTestLoader.discover(test_dir, pattern='test_*.py')

    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
