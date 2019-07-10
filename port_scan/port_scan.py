#!/usr/bin/env python
# coding=utf-8

import optparse
import time
#import nmap
from time import sleep
from threading import *
from socket import *

#tgtPorts = ['21', '22', '25', '80', '90', '139', '443', '445', '8080', '1521']
tgtPorts = []
for i in range(1000):
	tgtPorts.append(str(i))

# 利用nmap进行扫描   (未实现)
# def nmapScan(tgtHost,tgtPort):
# 	nmScan = nmap.PortScanner()    #创建PortScanner类对象
# 	nmScan.scan(tgtHost,tgtPort)
# 	state = nmScan[tgtHost]['tcp'][int(tgtPort)]['state']
# 	print "[*] " + tgtHost + "tcp/" + tgtHost + " " +state

def connScan(tgtHost,tgtPort):
	try:
		connSkt = socket(AF_INET,SOCK_STREAM)       #ipv4,tcp连接
		connSkt.connect((tgtHost,tgtPort))
		connSkt.send('ViolentPython\r\n')
		results = connSkt.recv(100)
		#screenLock.acquire()
		print "\n[+]Port %d is open"%tgtPort
		print '[+] ' + str(results)
		connSkt.close()
	except Exception as e:
		#print "[-]Port %d is not open"%tgtPort
		pass
	

def portScan(tgtHost):
	try:
		tgtIP = gethostbyname(tgtHost)        #将域名解析为ip地址
	except Exception as e:
		print "[-] Can't connect %s: Unknown host"%tgtHost
	try:
		tgtName = gethostbyaddr(tgtIP)
		print "\n[+] Scan Results for: " + tgtName[0]
	except Exception as e:
		print "\n[+] Scan Results for: " + tgtIP
	setdefaulttimeout(1)
	for tgtPort in tgtPorts:
		t = Thread(target=connScan, args=(tgtHost,int(tgtPort)))
		t.start()
		sleep(0.01)
		#nmapScan(tgtHost,tgtPort)
		#connScan(tgtHost,int(tgtPort))

def main():
	parser = optparse.OptionParser('usage %prog -o <target host>')
	parser.add_option('-o', dest='tgtHost', help='target host')
	#parser.add_option('-p', dest='tgtPort', type='int', help='target port')
	(options, args) = parser.parse_args()

	tgtHost = options.tgtHost
	#tgtPort = options.tgtPort
	if tgtHost == None:
		print parser.usage
		exit(0)
	portScan(tgtHost)

if __name__ == '__main__':
	main()