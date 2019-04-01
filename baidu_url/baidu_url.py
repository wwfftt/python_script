#!/usr/bin/env python
# coding=utf-8

import requests
import threading
import Queue
import sys
from bs4 import BeautifulSoup as bs
import re


'''
百度url采集脚本
url = https://www.baidu.com/s?wd=python&pn=10
wd(keyword)   pn(page_num)
'''


headers = {'User-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0'}


class Spider(threading.Thread):
	"""docstring for Spider"""
	def __init__(self, queue):
		threading.Thread.__init__(self)
		self._queue = queue

	def run(self):
		while not self._queue.empty():
			url = self._queue.get_nowait()
			try:
				spider(url)
			except Exception,e:
				print e
				pass

def spider(url):
	r = requests.get(url=url, headers=headers)
	soup = bs(r.content,'lxml')
	python_urls = soup.find_all(name='a',attrs={'data-click':re.compile(('.')),'class':None})
	for python_url in python_urls:
		#print python_url['href']
		really_url = requests.get(url=python_url['href'], headers=headers, timeout=8)
		if really_url.status_code == 200:
			url_para = really_url.url
			url_index_tmp = url_para.split('/')
			url_index = url_index_tmp[0] + '//' + url_index_tmp[2]
			print url_para + '\n' + url_index
			f1 = open('out_para.txt','a+')
			f1.write(url_para+'\n')
			f1.close()
			with open('out_index.txt') as f:
				if url_index not in f.read():
					f2 = open('out_index.txt','a+')
					f2.write(url_index+'\n')
					f2.close()


def main(keyword):
	queue = Queue.Queue()
	for i in range(0,20,10):        #修改页数 10为1页
		queue.put('https://www.baidu.com/s?wd=%s&pn=%s'%(keyword,str(i)))

	threads = []
	thread_count = 3

	for i in range(thread_count):
		threads.append(Spider(queue))

	for t in threads:
		t.start()

	for t in threads:
		t.join()

if __name__ == '__main__':

	f1 = open('out_para.txt','w')
	f1.close()
	f2 = open('out_index.txt','w')
	f2.close()

	if len(sys.argv) != 2:
		print "Enter:%s keyword"%(sys.argv[0])
		sys.exit(-1)
	else:
		main(sys.argv[1])


