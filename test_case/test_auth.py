__author__ = 'Plumrx'

# time =
# encoding = utf-8
# file = .py
import unittest
import json
import requests
import time


@classmethod(unittest.skip('no reason'))
class TestRespister(unittest.TestCase):
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
        resp = self.respister_post('plumrx5@qq.com', 'plumrx', 'plumrx5')
        print('Response内容：' + resp.text)

        self.assertEqual(422, resp.status_code, '重复用户名验证失败！')
        self.assertIn('has already been taken', resp.text, '重复用户名验证失败！')

    def test_email_empty(self):
        resp = self.respister_post('', 'plumrx', 'plumrx5')

        self.assertEqual(422, resp.status_code, '空邮箱验证失败！')
        self.assertIn('can\'t be blank', resp.text, '空邮箱验证失败！')

    def tearDown(self):
        print('---------test end!-----------')


class TestLogin(unittest.TestCase):
    def setUp(self):
        print('-------------test login------------')

    def login_post(self, email, password):
        login_url = 'https://api.realworld.io/api/users/login'
        req_header = {}
        req_body = {"user": {"email": email, "password": password}}
        response = requests.post(login_url, params=req_header, json=req_body)
        return response

    def test_login_success(self):
        email = 'plumrx6@qq.com'
        password = 'plumrx'
        resp = self.login_post(email, password)

        self.assertEqual(200, resp.status_code, '登录失败！')
        self.assertIn('email', resp.text, '返回值不包含邮箱')
        self.assertIn(email, resp.text, '返回值邮箱不正确！')
        self.assertIn('image', resp.text, '返回值不包含image')
        self.assertIn('token', resp.text, '返回值不包含token')

    def test_email_wrong(self):
        email = 'plumrx6@qq.com1'
        password = 'plumrx'
        resp = self.login_post(email, password)

        self.assertEqual(403, resp.status_code, '错误邮箱验证失败！')
        self.assertIn('errors', resp.text, '返回值不包含错误码')
        self.assertIn('email or password', resp.text, '返回值不包含错误信息')
        self.assertIn('is invalid', resp.text, '返回值不包含具体错误信息')

    def test_password_empty(self):
        email = 'plumrx6@qq.com'
        password = ''
        resp = self.login_post(email, password)

        self.assertEqual(422, resp.status_code, '空密码验证失败！')
        self.assertIn('errors', resp.text, '返回值不包含错误码')
        self.assertIn('password', resp.text, '返回值不包含错误信息')
        self.assertIn('can\'t be blank', resp.text, '返回值不包含具体错误信息')

    def tearDown(self):
        print('-------------test login done------------')


class TestCurrentUser(unittest.TestCase):
    def setUp(self):
        print('----------current user---------')

    def current_user_get(self, params):
        current_user_url = 'https://api.realworld.io/api/users'
        response = requests.get(current_user_url, params=params)
        return response

    def test_current_user_success(self):
        req_header = {
            "Authorization": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InBsdW1yeDEzQHFxLmNvbSIsInVzZXJuYW1lIjoicGx1bXJ4MTMiLCJpYXQiOjE2NjY5NDk5OTksImV4cCI6MTY3MjEzMzk5OX0.0jGAEDtOi7zFL8ZNfdzSLXfhYq2j9mOqiv3DMj-Vr_s"
        }
        resp = self.current_user_get(params=req_header)

        self.assertEqual(200, resp.status_code, 'current user查询失败')
        self.assertIn('username', resp.text, '返回报文不包含username')

    def test_current_user_success(self):
        req_header = {
            "Authorization": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InBsdW1yeDEzQHFxLmNvbSIsInVzZXJuYW1lIjoicGx1bXJ4MTMiLCJpYXQiOjE2NjY5NDk5OTksImV4cCI6MTY3MjEzMzk5OX0.0jGAEDtOi7zFL8ZNfdzSLXfhYq2j9mOqiv3DMj-Vr_s"
        }
        resp = self.current_user_get(params=req_header)

        self.assertEqual(200, resp.status_code, 'current user查询失败')
        self.assertIn('username', resp.text, '返回报文不包含username')

    def test_no_token(self):
        req_header = {
            "Authorization": ""
        }
        resp = self.current_user_get(params=req_header)

        self.assertEqual(200, resp.status_code, 'current user查询失败')
        self.assertIn('username', resp.text, '返回报文不包含username')

    def test_not_exist_token(self):
        req_header = {
            "Authorization": "this is not exist token"
        }
        resp = self.current_user_get(params=req_header)

        self.assertEqual(401, resp.status_code, '不存在 token 查询失败')
        self.assertIn('"status": "error"', resp.text, '返回报文不包含错误状态')
        self.assertIn("missing authorization credentials", resp.text, '返回报文不包含错误信息')

    def test_expired_token(self):
        req_header = {
            "Authorization": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InBsdW1yeDZAcXEuY29tIiwidXNlcm5hbWUiOiJwbHVtcng2IiwiaWF0IjoxNjY2ODczOTM0LCJleHAiOjE2NzIwNTc5MzR9.rOjHf3uuJsywLq5OB1W0h9Wf3_x1-Eyhy4iKYAwmWZU"
        }
        resp = self.current_user_get(params=req_header)

        self.assertEqual(401, resp.status_code, '不存在 token 查询失败')
        self.assertIn('"status": "error"', resp.text, '返回报文不包含错误状态')
        self.assertIn("missing authorization credentials", resp.text, '返回报文不包含错误信息')
    def test_no_token(self):
        resp = self.current_user_get(params={})

        self.assertEqual(401, resp.status_code, '不存在 token 查询失败')
        self.assertIn('"status": "error"', resp.text, '返回报文不包含错误状态')
        self.assertIn("missing authorization credentials", resp.text, '返回报文不包含错误信息')
    def tearDown(self):
        print('----------current user done---------')

    if __name__ == '__main__':
        test_dir = '.'
        suite = unittest.defaultTestLoader.discover(test_dir, pattern='test_*.py')

        runner = unittest.TextTestRunner(verbosity=2)
        runner.run(suite)
