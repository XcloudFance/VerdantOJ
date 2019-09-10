#/usr/bin/env python
#-*- coding = utf-8 -*-

import psutil,demjson,os,time
from subprocess import PIPE
from compiler import *
def getfile(name):
	f = open(name,'r',encoding='utf-8')
	res = f.read()
	f.close()
	return res
testcode = input('input titlenum:')
config = demjson.decode(getfile(testcode+'/config.json'))
mem = 0
timer = 0
end = 0
print ('title : ',config['title'])
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
		outfile = getfile(testcode+'/'+data['out']).replace('\n',' ').strip()
		start = time.clock()
		try:
                        p = psutil.Popen(['run.exe'], stdout=PIPE, stdin=PIPE)
                        p.stdin.write(str(infile+'\r\n').encode('utf-8'))
                        p.stdin.flush()
                        mem = p.memory_info().vms
                        out = p.stdout.read().decode().replace('\n',' ').strip()
                        end = time.clock()
                        ret = p.wait()
                        mem = int(mem) / 1024 /1024#
                        timer = int(data['timelimit'])/1000
                        
		except:ret=1;
		print('data'+str(i)+' time:',end-start,'memory:',mem)
		if ret!=0:
			print('Result:Runtime Error')
			continue
		if end-start>timer:
			print('Result:Time Limit Exceeded')
			continue
		if mem >= int(data['memory']):
			print('Result:Memory Limit Exceeded')
			continue
		if out != outfile:
			print('Result:Wrong Anwser')
			continue
		print('Result:Accepted')
		tot+=int(data['score'])
elif config['IO'] == 'File IO':
	count = config['datacount']
	filename = config['ioname']
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
                outfile = getfile(testcode+'/'+data['out']).replace('\n',' ').strip()
                fs = open(filename+'.in','w+')
                fs.write(infile)
                fs.close()
                start = time.clock()
                #try:
                p = psutil.Popen('run.exe',shell=True)
                yourout = getfile(filename+'.out').strip()
                
                mem = p.memory_info().vms
                end = time.clock()
                ret = p.wait()
                mem = int(mem) / 1024 /1024
                timer = int(data['timelimit'])/1000
                        
                #except:ret=1
                print('data'+str(i)+' time:',end-start,'memory:',mem)#'in:',infile,'yourout:',out.decode(),'correctout:',outfile)
                if ret!=0:
                        print('Result:Runtime Error')
                        continue
                if end-start>timer:
                        print('Result:Time Limit Exceeded')
                        continue
                if mem >= int(data['memory']):
                        print('Result:Memory Limit Exceeded')
                        continue
                if yourout != outfile:
                        print('Result:Wrong Anwser')
                        continue
                print('Result:Accepted')
                tot+=int(data['score'])
	print('Total Score:',tot)
