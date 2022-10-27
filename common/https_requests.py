import requests


class HttpsRequests(object):
    def __init__(self, url):
        self.url = url
        self.req = requests.session()
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:97.0) Gecko/20100101 Firefox/97.0'}

    def get(self, uri='', params='', data='', headers=None, cookies=None):
        url = self.url + uri
        response = self.req.get(url, params=params, data=data)
        return response


    def post(self, uri='', params='', data='', headers=None, cookies=None):
        url = self.url + uri
        response = self.req.post(url, params=params, data=data, headers=headers, cookies=cookies)
        return response


    # 封装 put 方法，更新资源
    def put(self, uri='', params='', data='', headers=None, cookies=None):
        url = self.url + uri
        response = self.req.put(url, params=params, data=data, headers=headers, cookies=cookies)
        return response


    def delete(self, rui='', params='', data='', headers=None, cookies=None):
        url = self.url + uri
        response = self.req.delete(url, params=params, data=data, headers=headers, cookies=cookies)
        return response