# -*- coding: utf-8 -*-
import urllib2  
response = urllib2.urlopen('http://www.findspace.name/adds/hosts2')
new_content = response.read()
path = "c:\windows\system32\drivers\etc\hosts"
msg = "The hosts have added!"
def re_host(list):
    w = open(path,'w+')
    for i in range(len(list)):
        w.write(list[i])
    w.close()
f = open(path,'r')
host_list = f.readlines()
line_num = len(host_list)
begin = '#+BEGIN\n'
for i in range(line_num):
    if host_list[i] == begin:
        del host_list[i:line_num]
        msg = "The hosts have changed!"
        break
host_list.append(new_content)
re_host(host_list)
print msg
