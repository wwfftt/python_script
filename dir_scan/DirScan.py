#!/usr/bin/env python
# encoding=utf-8

import requests
import threading
import Queue
import sys
import user_agent_list
from optparse import OptionParser

headers = user_agent_list.get_user_agent()

class DirScanMain:
	def __init__(self, options):
		self.url = options.url
		self.exp = options.exp
		self.count = options.count

	class DirScan(threading.Thread):
		"""docstring for Spider"""
		def __init__(self, queue, total):
			threading.Thread.__init__(self)
			self._queue = queue
			self._total = total

		def run(self):
			while not self._queue.empty():
				url = self._queue.get()
				self.spider(url)  

		def spider(self, url):
			threading.Thread(target=self.msg).start()
			try:
				r = requests.get(url=url,headers=headers,timeout=6)
				if r.status_code == 200:
					sys.stdout.write('\r'+'[*]%s\t\t\n'%(url))
			except Exception as e:
				pass
				
		#msg 用于计算queue里的数据以及如何表示出来
		def msg(self):
			per = 100-float(self._queue.qsize())/float(self._total)*100
			msg = '%s Finish|%s All| Scan in %1.f %s'%(self._total-self._queue.qsize(), self._total, per, '%')
			sys.stdout.write('\r'+'[#]'+msg)


	def main(self):
		queue = Queue.Queue()

		f = open('./dics/%s.txt'%self.exp,'r')
		for i in f:
			queue.put(self.url+i.rstrip('\n'))

		total = queue.qsize()

		threads = []
		thread_count = self.count

		for i in range(thread_count):
			threads.append(self.DirScan(queue,total))

		for t in threads:
			t.start()

		for t in threads:
			t.join()

if __name__ == '__main__':
	print '''
	 ______  _________ _______       _______  _______  _______  _       
(  __  \ \__   __/(  ____ )     (  ____ \(  ____ \(  ___  )( (    /|
| (  \  )   ) (   | (    )|     | (    \/| (    \/| (   ) ||  \  ( |
| |   ) |   | |   | (____)|     | (_____ | |      | (___) ||   \ | |
| |   | |   | |   |     __)     (_____  )| |      |  ___  || (\ \) |
| |   ) |   | |   | (\ (              ) || |      | (   ) || | \   |
| (__/  )___) (___| ) \ \__     /\____) || (____/\| )   ( || )  \  |
(______/ \_______/|/   \__/_____\_______)(_______/|/     \||/    )_)
                          (_____)  
	'''
	parser = OptionParser()
	parser.add_option("-u", "--url", dest="url", help="target url for scan")
	parser.add_option("-e", "--exp", dest="exp", help="target url exp")
	parser.add_option("-t", "--thread", default=10, type="int", dest="count", help="scan thread_count")

	(options, args) = parser.parse_args()

	if options.url and options.exp:
		d = DirScanMain(options)
		d.main()
		sys.exit(1)
	else:
		parser.print_help()
		sys.exit(1)