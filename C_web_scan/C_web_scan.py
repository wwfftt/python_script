#!/usr/bin/env python
# encoding=utf-8


#C段WEB扫描工具

import requests
import threading
import Queue
import sys
from IPy import IP
import user_agent_list
from requests.packages import urllib3
import re

headers = user_agent_list.get_user_agent()

class WebScan(threading.Thread):
	"""docstring for Spider"""
	def __init__(self, queue):
		threading.Thread.__init__(self)
		self._queue = queue

	def run(self):
		while not self._queue.empty():
			url = self._queue.get()
			#print url
			spider(url)

def spider(url):
	try:
		urllib3.disable_warnings()  #取消访问https时的warning信息
		r = requests.get(url=url, headers=headers, timeout=6, verify=False)   #verify=False 访问https
  		if r.status_code == 200:
  			print '[*]Web Service Found!%s'%url
  			f = open('result.txt','a+')
  			f.write(url+'\n')
  			f.close()
	except Exception as e:
		pass
  	
def web_scan(ip):
	queue = Queue.Queue()
	ips = IP(ip, make_net=True)

	req_mtd = ['http://']

	port = ['80', '8080']

	for re in req_mtd:
		for ip in ips:
			for p in port:
				queue.put(str(re)+str(ip)+':'+str(p))

	return queue

def main(ip):

	f = open('result.txt','w')
	f.close()

	queue = web_scan(ip)

	threads = []
	thread_count = 100

	for i in range(thread_count):
		threads.append(WebScan(queue))

	for t in threads:
		t.start()

	for t in threads:
		t.join()

if __name__ == '__main__':
	# with open('nmap.xml') as f:
	# 	ips = re.findall('<address addr="(.*?)" addrtype',f.read())

	# 	main(ips)
	if len(sys.argv) != 2:
		print '%s:xxx.xxx.xxx.xxx/24'%sys.argv[0]
		exit(1)
	else:
		main(sys.argv[1])
		exit(1)