__author__ = 'Plumrx'
# encoding = utf-8
__author__ = 'Plumrx'

# time =
# encoding = utf-8
# file = .py
import unittest
import json
import requests
import time


class TestRespisterCeleb(unittest.TestCase):
    def setUp(self):
        print('---------test start!---------')

    def respister_post(self, email, password, username):
        respister_url = 'https://api.realworld.io/api/users'
        req_header = {}
        req_body = {"user": {"email": 'celeb_' + email, "password": password, "username": 'celeb_' + username}}
        response = requests.post(respister_url, headers=req_header, json=req_body)
        return response

    def test_success(self):
        user = str(int(time.time()) * 1000)
        resp = self.respister_post(user + '@qq.com', 'plumrx', user)
        print('Response内容：' + resp.text)

        self.assertEqual(200, resp.status_code, '注册失败！')
        self.assertIn(user + '@qq.com', resp.text, '响应不包含user')
        self.assertIn(user, resp.text, '响应不包含email')
        self.assertIn('image', resp.text, '响应不包含image')
        self.assertIn('token', resp.text, '响应不包含token')

        # 将注册获取的 token 写入文件中
        resp_token = resp.json()['user']['token']
        print('****************' + resp_token)
        f = open('token.txt', 'a')
        f.write(resp_token + '\n')
        f.close()

    def test_username_repeat(self):
        resp = self.respister_post('plumrx13@qq.com', 'plumrx', 'plumrx13')
        print('Response内容：' + resp.text)

        self.assertEqual(422, resp.status_code, '重复用户名验证失败！')
        self.assertIn('has already been taken', resp.text, '重复用户名验证失败！')

    def test_email_empty(self):
        resp = self.respister_post('', 'plumrx', 'plumrx5')

        self.assertEqual(422, resp.status_code, '空邮箱验证失败！')
        self.assertIn('can\'t be blank', resp.text, '空邮箱验证失败！')

    def tearDown(self):
        print('---------test end!-----------')


class TestProfile(unittest.TestCase):
    def setUp(self):
        print('---------test start!---------')

    def respister_get(self, username):
        respister_url = 'https://api.realworld.io/api/profiles/celeb_' + username

        req_header = {}

        response = requests.get(respister_url, params=req_header)
        return response

    def test_profile(self):
        username = 'plumrx13'
        resp = self.respister_get(username)

        self.assertEqual(200, resp.status_code, 'profile调用失败')
        self.assertIn('profile', resp.text, '返回报文不包含profile')
        self.assertIn('celeb_' + username, resp.text, '返回报文不包含用户名')


class TestFollow(unittest.TestCase):
    def setUp(self):
        print('---------test start!---------')

    def follow_post(self, username, email):
        follow_url = 'https://api.realworld.io/api/profiles/celeb_' + username+'/follow'

        req_header = {}
        req_body = {"user": {"email": email}}
        response = requests.get(follow_url, params=req_header,json=req_body)
        return response

    def test_follow_success(self):
        username = 'plumrx13'
        email='plumrx13@qq.com'
        resp = self.follow_post(username,email)

        self.assertEqual(200, resp.status_code, 'profile调用失败')
        # self.assertIn('profile', resp.text, '返回报文不包含profile')
        # self.assertIn('celeb_' + username, resp.text, '返回报文不包含用户名')

    def test_follow_fail(self):
        username = 'plumrx13'
        email='plumrx13@qq.com'
        resp = self.follow_post(username,email)

        self.assertEqual(401, resp.status_code, 'profile鉴权非失败')
        self.assertIn('status', resp.text, '返回报文不包含status')
        self.assertIn('message' + username, resp.text, '返回报文不包含message')


class TestUnfollow(unittest.TestCase):
    def setUp(self):
        print('---------test start!---------')

    def unfollow_delete(self, username):
        follow_url = 'https://api.realworld.io/api/profiles/celeb_' + username+'/follow'

        req_header = {}

        response = requests.delete(follow_url, params=req_header)
        return response

    def test_unfollow_success(self):
        username = 'plumrx13'

        resp = self.unfollow_delete(username)

        self.assertEqual(200, resp.status_code, 'profile调用失败')
        # self.assertIn('profile', resp.text, '返回报文不包含profile')
        # self.assertIn('celeb_' + username, resp.text, '返回报文不包含用户名')

    def test_unfollow_fail(self):
        username = 'plumrx13'
        email='plumrx13@qq.com'
        resp = self.follow_post(username,email)

        self.assertEqual(401, resp.status_code, 'profile鉴权非失败')
        self.assertIn('status', resp.text, '返回报文不包含status')
        self.assertIn('message' + username, resp.text, '返回报文不包含message')

if __name__ == '__main__':
    test_dir = '.'
    suite = unittest.defaultTestLoader.discover(test_dir, pattern='test_*.py')

    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
