#/usr/bin/env python
#coding=utf-8
#进程检测程序
import psutil,demjson,os,time
from subprocess import PIPE
from compiler import *
def getfile(name):
	f = open(name,'r')
	res = f.read()
	f.close()
	return res
testcode = input('请输入题号：')
config = demjson.decode(getfile(testcode+'/config.json'))
print ('测评题为:',config['title'])
if config['IO'] == 'standard IO':
	count = config['datacount']
	if os.path.exists('run.exe'):
		os.remove('run.exe')
	compiling('c++','run.cpp','run.exe')
	if not os.path.exists('run.exe'):
		print('Result:Compile Error')
		print('Total Score:', 0)
		exit(0)
	tot = 0
	for i in range(0,int(count)):
		data = config['configuration'][str(i)]
		infile = getfile(testcode+'/'+data['in'])
		outfile = getfile(testcode+'/'+data['out']).strip()#读取完out文件自动去除空格前缀and后缀
		start = time.clock()
		p = psutil.Popen(['run.exe'], stdout=PIPE, stdin=PIPE)
		p.stdin.write(str(infile+'\r\n').encode('GBK'))
		p.stdin.flush()
		mem = p.memory_info().rss
		out = p.stdout.read().strip()
		end = time.clock()
		ret = p.wait()#wait相当于call的返回值，csdn:https://www.cnblogs.com/zhoug2020/p/5079407.html
		mem = int(mem) / 1024 #放到这里计算是为了防止时间被算的太多，当然也可以分段取时间
		timer = int(data['timelimit'])/1000
		print('data'+str(i)+' time:',end-start,'memory:',mem,'in:',infile,'yourout:',out.decode(),'correctout:',outfile)
		if ret!=0:
			print('Result:Runtime Error')
			continue
		if end-start>timer:
			print('Result:Time Limit Exceeded')
			continue
		if mem >= int(data['memory']):
			print('Result:Memory Limit Exceeded')
			continue
		if out.decode() != outfile:
			print('Result:Wrong Anwser')
			continue
		print('Result:Accepted')
		tot+=int(data['score'])
	print('Total Score:',tot)
