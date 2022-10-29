__author__ = 'Plumrx'

import time

# encoding = utf-8
import requests
import unittest


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


class TestCreateArtcles(unittest.TestCase):
    def setUp(self):
        print('---------test all create articles start!---------')

    def create_articles_post(self, header, body):
        articles_url = 'https://api.realworld.io/api/articles'
        req_header = header
        req_body = body
        response = requests.post(articles_url, headers=req_header, json=req_body)
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


class TestFeed(unittest.TestCase):
    def setUp(self):
        print('-----------test feed start!---------')

    def feed_get(self, login_user):
        unfollow_url = 'https://api.realworld.io/api/articles/'

        token = Utils.token_get(login_user)
        req_header = {"Authorization": 'Token ' + token}
        response = requests.get(unfollow_url, headers=req_header)
        return response

    def test_feed_success(self):
        login_user = 'plumrx13'
        resp = self.feed_get(login_user)
        print(resp.text)

        self.assertEqual(200, resp.status_code, 'feed调用失败')
        self.assertIn('articles', resp.text, '返回报文不包含articles')

    def test_follow_fail(self):
        login_user = 'plumrx6'
        resp = self.feed_get(login_user)
        print(resp.text)

        self.assertEqual(401, resp.status_code, '调用失败')
        self.assertIn('error', resp.text, '返回报文不包含error')

    def tearDown(self):
        print('-----------test feed done!------------')


class TestAllArticlesWithAuth(unittest.TestCase):
    def setUp(self):
        print('-----------test all articles with auth start!---------')

    def articles_with_auth_get(self, login_user):
        articles_url = 'https://api.realworld.io/api/articles/'

        token = Utils.token_get(login_user)
        req_header = {"Authorization": 'Token ' + token}
        response = requests.get(articles_url, headers=req_header)
        return response

    def test_articles_with_auth_success(self):
        login_user = 'plumrx13'
        resp = self.articles_with_auth_get(login_user)
        print(resp.text)

        self.assertEqual(200, resp.status_code, 'feed调用失败')
        self.assertIn('articles', resp.text, '返回报文不包含articles')

    def test_articles_with_auth_fail(self):
        login_user = 'plumrx6'
        resp = self.articles_with_auth_get(login_user)
        print(resp.text)

        self.assertEqual(401, resp.status_code, '调用失败')
        self.assertIn('error', resp.text, '返回报文不包含error')

    def tearDown(self):
        print('-----------test unfollow done!------------')


class TestArticlesBySlug(unittest.TestCase):
    def setUp(self):
        print('-----------test single article by slug start!---------')

    def articles_by_slug_get(self, login_user, slug):
        articles_url = 'https://api.realworld.io/api/articles/' + slug

        token = Utils.token_get(login_user)
        req_header = {"Authorization": 'Token ' + token}
        response = requests.get(articles_url, headers=req_header)
        return response

    def test_articles_by_slug_success(self):
        login_user = 'plumrx13'
        slug = "How-to-train-your-dragon1-110392"

        resp = self.articles_by_slug_get(login_user, slug)

        self.assertEqual(200, resp.status_code, 'articles by slug调用失败')
        self.assertIn('article', resp.text, '返回报文不包含article')
        self.assertIn(slug, resp.text, '返回报文不包含上送slug')

    def test_articles_by_slug_fail(self):
        login_user = 'plumrx6'
        slug = "How-to-train-your-dragon1-110392"

        resp = self.articles_by_slug_get(login_user, slug)

        self.assertEqual(401, resp.status_code, 'articles by slug调用失败')
        self.assertIn('error', resp.text, '返回报文无error')

    def tearDown(self):
        print('-----------test single article by slug done!------------')


class TestArticlesByTag(unittest.TestCase):
    def setUp(self):
        print('-----------test single article by tag start!---------')

    def articles_by_tag_get(self, login_user, tag):
        articles_url = 'https://api.realworld.io/api/articles?tag=' + tag

        token = Utils.token_get(login_user)
        req_header = {"Authorization": 'Token ' + token}
        response = requests.get(articles_url, headers=req_header)
        return response

    def test_articles_by_tag_success(self):
        login_user = 'plumrx13'
        tag = 'dragons'

        resp = self.articles_by_tag_get(login_user, tag)

        self.assertEqual(200, resp.status_code, 'articles by slug调用失败')
        self.assertIn('article', resp.text, '返回报文不包含article')
        self.assertIn(tag, resp.text, '返回报文不包含上送slug')

    def test_articles_by_tag_fail(self):
        login_user = 'plumrx6'
        tag = 'dragons'
        resp = self.articles_by_tag_get(login_user, tag)

        self.assertEqual(401, resp.status_code, 'articles by slug调用失败')
        self.assertIn('error', resp.text, '返回报文无error')

    def tearDown(self):
        print('-----------test single article by tag done!------------')


class TestUpdateArticle(unittest.TestCase):
    def setUp(self):
        print('-----------test update article start!---------')

    def update_article_put(self, login_user, slug):
        articles_url = 'https://api.realworld.io/api/articles/' + slug

        token = Utils.token_get(login_user)
        req_header = {"Authorization": 'Token ' + token}
        req_body = {"article": {"body": "With two hands"}}
        response = requests.get(articles_url, headers=req_header, json=req_body)
        return response

    def test_update_article_success(self):
        login_user = 'plumrx13'
        slug = "How-to-train-your-dragon1-110392"

        resp = self.update_article_put(login_user, slug)

        self.assertEqual(200, resp.status_code, 'articles by slug调用失败')
        self.assertIn('article', resp.text, '返回报文不包含article')
        self.assertIn(slug, resp.text, '返回报文不包含上送slug')

    def test_update_article_fail(self):
        login_user = 'plumrx6'
        slug = "How-to-train-your-dragon1-110392"

        resp = self.update_article_put(login_user, slug)

        self.assertEqual(401, resp.status_code, 'articles by slug调用失败')
        self.assertIn('error', resp.text, '返回报文无error')

    def tearDown(self):
        print('-----------test single article by tag done!------------')


class TestFavoriteArticle(unittest.TestCase):
    def setUp(self):
        print('-----------test favorite article start!---------')

    def update_article_put(self, login_user, slug):
        articles_url = 'https://api.realworld.io/api/articles/' + slug + '/favorite'

        token = Utils.token_get(login_user)
        req_header = {"Authorization": 'Token ' + token}

        response = requests.post(articles_url, headers=req_header)
        return response

    def test_favorite_article_success(self):
        login_user = 'plumrx13'
        slug = "How-to-train-your-dragon1-110392"

        resp = self.update_article_put(login_user, slug)

        self.assertEqual(200, resp.status_code, 'articles by slug调用失败')
        self.assertIn('article', resp.text, '返回报文不包含article')
        self.assertIn(slug, resp.text, '返回报文不包含上送slug')

    def test_favorite_article_fail(self):
        login_user = 'plumrx6'
        slug = "How-to-train-your-dragon1-110392"

        resp = self.update_article_put(login_user, slug)

        self.assertEqual(401, resp.status_code, 'articles by slug调用失败')
        self.assertIn('error', resp.text, '返回报文无error')

    def tearDown(self):
        print('-----------test single article by tag done!------------')


class TestFavoriteArticleByUsername(unittest.TestCase):
    def setUp(self):
        print('-----------test favorite article by username start!---------')

    def favorite_article_by_username_get(self, login_user):
        articles_url = 'https://api.realworld.io/api/articles/?favorite=' + login_user

        token = Utils.token_get(login_user)
        req_header = {"Authorization": 'Token ' + token}

        response = requests.post(articles_url, headers=req_header)
        return response

    def test_favorite_article_by_name_success(self):
        login_user = 'plumrx13'

        resp = self.favorite_article_by_username_get(login_user)

        self.assertEqual(200, resp.status_code, 'articles by slug调用失败')
        self.assertIn('article', resp.text, '返回报文不包含article')

    def test_favorite_article_by_name_fail(self):
        login_user = 'plumrx6'

        resp = self.favorite_article_by_username_get(login_user)

        self.assertEqual(401, resp.status_code, 'articles by slug调用失败')
        self.assertIn('error', resp.text, '返回报文无error')

    def tearDown(self):
        print('-----------test favorite article by username done!------------')


class TestUnfavoriteArticle(unittest.TestCase):
    def setUp(self):
        print('-----------test unfavorite article start!---------')

    def unfavorite_article_delete(self, login_user, slug):
        articles_url = 'https://api.realworld.io/api/articles/' + slug + '/favorite'

        token = Utils.token_get(login_user)
        req_header = {"Authorization": 'Token ' + token}

        response = requests.delete(articles_url, headers=req_header)
        return response

    def test_unfavorite_article_success(self):
        login_user = 'plumrx13'
        slug = "How-to-train-your-dragon1-110392"

        resp = self.unfavorite_article_delete(login_user, slug)

        self.assertEqual(200, resp.status_code, 'articles by slug调用失败')
        self.assertIn('article', resp.text, '返回报文不包含article')

    def test_favorite_article_by_name_fail(self):
        login_user = 'plumrx6'
        slug = "How-to-train-your-dragon1-110392"

        resp = self.unfavorite_article_delete(login_user, slug)

        self.assertEqual(401, resp.status_code, 'articles by slug调用失败')
        self.assertIn('error', resp.text, '返回报文无error')

    def tearDown(self):
        print('-----------test favorite article by username done!------------')


class TestCreateCommentForArticle(unittest.TestCase):
    def setUp(self):
        print('-----------test create comment for article start!---------')

    def comment_article_post(self, login_user, slug, comment):
        articles_url = 'https://api.realworld.io/api/articles/' + slug + '/comments'

        token = Utils.token_get(login_user)
        req_header = {"Authorization": 'Token ' + token}
        req_body = {"comment": {"body": comment}}

        response = requests.post(articles_url, headers=req_header, json=req_body)
        return response

    def test_comment_article_success(self):
        login_user = 'plumrx13'
        slug = "How-to-train-your-dragon1-110392"
        comment = 'This is a good article.'

        resp = self.comment_article_post(login_user, slug, comment)
        print(resp.text)

        self.assertEqual(200, resp.status_code, 'articles by slug调用失败')
        self.assertIn('article', resp.text, '返回报文不包含article')

    def test_comment_article_fail(self):
        login_user = 'plumrx6'
        slug = "How-to-train-your-dragon1-110392"
        comment = 'This is a good article.'

        resp = self.comment_article_post(login_user, slug, comment)

        self.assertEqual(401, resp.status_code, 'articles by slug调用失败')
        self.assertIn('error', resp.text, '返回报文无error')

    def tearDown(self):
        print('-----------test favorite article by username done!------------')


class TestAllCommentForArticle(unittest.TestCase):
    def setUp(self):
        print('-----------test all comment for article start!---------')

    def all_comment_get(self, login_user, slug):
        articles_url = 'https://api.realworld.io/api/articles/' + slug + '/comments'

        token = Utils.token_get(login_user)
        req_header = {"Authorization": 'Token ' + token}

        response = requests.get(articles_url, headers=req_header)
        return response

    def test_comment_article_success(self):
        login_user = 'plumrx13'
        slug = "How-to-train-your-dragon1-110392"

        resp = self.all_comment_get(login_user, slug)

        self.assertEqual(200, resp.status_code, 'articles by slug调用失败')
        self.assertIn('article', resp.text, '返回报文不包含article')

    def test_comment_article_fail(self):
        login_user = 'plumrx6'
        slug = "How-to-train-your-dragon1-110392"

        resp = self.all_comment_get(login_user, slug)

        self.assertEqual(401, resp.status_code, 'articles by slug调用失败')
        self.assertIn('error', resp.text, '返回报文无error')

    def tearDown(self):
        print('-----------all favorite article by username done!------------')


class TestDeleteCommentForArticle(unittest.TestCase):
    def setUp(self):
        print('-----------test delete comment for article start!---------')

    def delete_comment_get(self, login_user, slug, commentid):
        articles_url = 'https://api.realworld.io/api/articles/' + slug + '/comments' + commentid

        token = Utils.token_get(login_user)
        req_header = {"Authorization": 'Token ' + token}

        response = requests.delete(articles_url, headers=req_header)
        return response

    def test_delete_comment_article_success(self):
        login_user = 'plumrx13'
        slug = "How-to-train-your-dragon1-110392"
        commentid = '34794'

        resp = self.all_comment_get(login_user, slug, commentid)

        self.assertEqual(200, resp.status_code, 'articles by slug调用失败')
        self.assertIn('article', resp.text, '返回报文不包含article')

    def test_delete_comment_article_fail(self):
        login_user = 'plumrx13'
        slug = "How-to-train-your-dragon1-110392"
        commentid = '34794'

        resp = self.all_comment_get(login_user, slug, commentid)

        self.assertEqual(404, resp.status_code, 'articles by slug调用失败')


    def tearDown(self):
        print('-----------all favorite article by username done!------------')


class TestDeleteArticle(unittest.TestCase):
    def setUp(self):
        print('-----------test delete article start!---------')

    def article_delete(self, login_user, slug):
        articles_url = 'https://api.realworld.io/api/articles/' + slug

        token = Utils.token_get(login_user)
        req_header = {"Authorization": 'Token ' + token}

        response = requests.get(articles_url, headers=req_header)
        return response

    def test_delete_article_success(self):
        login_user = 'plumrx13'
        slug = "How-to-train-your-dragon1-110392"

        resp = self.article_delete(login_user, slug)

        self.assertEqual(200, resp.status_code, 'delete articles调用失败')
        self.assertIn('article', resp.text, '返回报文不包含article')

    def test_delete_comment_article_fail(self):
        login_user = 'plumrx6'
        slug = "How-to-train-your-dragon1-110392"

        resp = self.all_comment_get(login_user, slug)

        self.assertEqual(401, resp.status_code, 'articles by slug调用失败')


    def tearDown(self):
        print('-----------all delete article done!------------')


if __name__ == '__main__':
    test_dir = '.'
    suite = unittest.defaultTestLoader.discover(test_dir, pattern='test_*.py')

    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
