import psutil
def compiling(lang,name,filename):
	if lang =='c++':
		psutil.Popen('g++ '+name+' -o '+filename+" -O2",shell=True).wait()
	if lang =='c':
		psutil.Popen('gcc '+name+' -o '+filename,shell=True).wait()
	if lang == 'golang':
		psutil.Popen('go build ' + name + ' -o ' + filename , shell=True).wait()