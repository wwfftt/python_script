#!/usr/bin/env python
# encoding=utf-8

import exrex
import sys

'''
一个暴力破解的字典方式
输入一个host: http://www.mode.study.com/
用户名就可能为mode,study 密码就类似mode@123,study123
'''

black_list = ['www','com','http','cn','org','edu'] #写的不太全

def host_para(host):
	#将host变成我们想要的格式
	if '://' in host:
		host = host.split('://')[1]

	if '/' in host:
		host = host.replace('/','')

	return host

def dic_creat(host):
	#取出有用的东西,如mode,study,生成字典
	#将核心的生成规律，写入配置文件，方便使用
	f_rule = open('rule.ini','r')
	for i in f_rule:
		if '#' != i[0]:
			rule = i

	f1_pass = open('dictionary.txt','w')
	f1_pass.close()

	dics = host.split('.')
	for dic_name in dics:
		if dic_name not in black_list:
			f_pass = open('pass_0.txt','r')
			for dic_pass in f_pass:
				dictionary = list(exrex.generate(rule.format(dic_name=dic_name,dic_pass=dic_pass.strip('\n'))))

				for dic in dictionary:
					if len(dic) > 6:   #根据需要修改密码长度
						f1_pass = open('dictionary.txt','a')
						f1_pass.write(dic+'\n')
						f1_pass.close()

	if f1_pass != '':
		print 'successful! Write in dictionary.txt'

def main(host):
	dic_creat(host_para(host))

if __name__ == '__main__':
	if len(sys.argv) != 2:
		print '%s www.xxx.com'%sys.argv[0]
	else:
		main(sys.argv[1])