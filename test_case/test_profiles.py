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


class Utils(object):

    @staticmethod
    def token_putin(email, password):
        global username
        url = 'https://api.realworld.io/api/users/login'
        if email == 'plumrx6@qq.com':
            username = 'plumrx6'
        elif email == 'plumrx13@qq.com':
            username = 'plumrx13'
        else:
            username = 'other_user'
        req_body = {"user": {"email": email, "password": password}}
        resp = requests.post(url, json=req_body)

        resp_token = resp.json()['user']['token']
        with open('../test_data/' + username + '_token.txt', 'w') as f:
            f.write(resp_token)

    @staticmethod
    def token_get(user):
        with open('../test_data/' + user + '_token.txt', 'r') as f:
            token = f.read()
        return token


class TestProfile(unittest.TestCase):
    def setUp(self):
        print('---------test profile start!---------')

    def profile_get(self, user, headers):
        respister_url = 'https://api.realworld.io/api/profiles/' + user

        req_header = headers

        response = requests.get(respister_url, headers=req_header)
        return response

    def test_profile(self):
        user = 'plumrx13'
        token = Utils.token_get(user)
        req_header = {"Authorization": token}
        resp = self.profile_get(user, req_header)

        self.assertEqual(200, resp.status_code, 'profile调用失败')
        self.assertIn('profile', resp.text, '返回报文不包含profile')
        self.assertIn(user, resp.text, '返回报文不包含用户名')

    def tearDown(self):
        print('---------test profile done!---------')


class TestFollow(unittest.TestCase):
    def setUp(self):
        print('---------test start!---------')

    def follow_post(self, followed_user, login_user):
        follow_url = 'https://api.realworld.io/api/profiles/' + followed_user + '/follow'

        token = Utils.token_get(login_user)
        req_header = {"Authorization": 'Token '+token}
        response = requests.post(follow_url, headers=req_header)
        return response

    def test_follow_success(self):
        followed_user = 'plumrx6'
        login_user = 'plumrx13'
        resp = self.follow_post(followed_user, login_user)

        self.assertEqual(200, resp.status_code, 'profile调用失败')
        self.assertIn('profile', resp.text, '返回报文不包含profile')
        self.assertIn(followed_user, resp.text, '返回报文不包含用户名')

    def test_follow_fail(self):
        followed_user = 'plumrx13'
        login_user = 'plumrx6'
        resp = self.follow_post(followed_user, login_user)

        self.assertEqual(401, resp.status_code, 'profile鉴权非失败')
        self.assertIn('status', resp.text, '返回报文不包含status')
        self.assertIn('message', resp.text, '返回报文不包含message')

    def tearDown(self):
        print('-----------test follow done!-------------')
class TestUnfollow(unittest.TestCase):
    def setUp(self):
        print('-----------test unfollow start!---------')

    def unfollow_delete(self, followed_user, login_user):
        unfollow_url = 'https://api.realworld.io/api/profiles/' + followed_user + '/follow'

        token = Utils.token_get(login_user)
        req_header = {"Authorization": 'Token '+token}
        response = requests.delete(unfollow_url, headers=req_header)
        return response

    def test_unfollow_success(self):
        followed_user = 'plumrx6'
        login_user = 'plumrx13'
        resp = self.unfollow_delete(followed_user, login_user)

        self.assertEqual(200, resp.status_code, 'profile调用失败')
        self.assertIn('profile', resp.text, '返回报文不包含profile')
        self.assertIn(followed_user, resp.text, '返回报文不包含用户名')

    def test_follow_fail(self):
        followed_user = 'plumrx13'
        login_user = 'plumrx6'
        resp = self.unfollow_delete(followed_user, login_user)

        self.assertEqual(401, resp.status_code, 'profile鉴权非失败')
        self.assertIn('status', resp.text, '返回报文不包含status')
        self.assertIn('message', resp.text, '返回报文不包含message')
    def tearDown(self):
        print('-----------test unfollow done!------------')


if __name__ == '__main__':
    test_dir = '.'
    suite = unittest.defaultTestLoader.discover(test_dir, pattern='test_*.py')

    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
