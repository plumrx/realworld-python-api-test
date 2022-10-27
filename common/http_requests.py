__author__ = 'Plumrx'

# time =
# encoding = utf-8
# file = .py
import requests


class HttpRequests(object):

	def __init__(self, url):
		self.url = url
		self.req = requests.Session()
		self.header = {
			'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:97.0) Gecko/20100101 Firefox/97.0'}

	# 封装自己的 get 请求，获取资源
	def get(self, uri='', params='', data='', headers=None, cookie=None):
		url = self.url + uri
		respose = self.req.get(url, params=params, data=data, headers=headers, cookie=cookie)

	# 封装 post 方法，创建资源
	def post(self,uri='',params='',data='',headers=None,cookies=None):
		url = self.url + uri
		response = self.req.post(url,params=params,data=data,headers=headers,cookies=cookies)
		return response

	# 封装 put 方法，更新资源
	def put(self,uri='',params='',data='',headers=None,cookies=None):
		url=self.url+uri
		response = self.req.put(url,params=params,data=data,headers=headers,cookies=cookies)
		return response

	def delete(self,rui='',params='',data='',headers=None,cookies=None):
		url=self.url+uri
		response = self.req.delete(url,params=params,data=data,headers=headers,cookies=cookies)
		return response