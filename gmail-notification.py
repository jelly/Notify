#!/usr/bin/python
import os,string

#Enter your username and password below within double quotes
# eg. username="username" and password="/path/to/passwdfile"
username="xxxxxxxxxx"
password = "xxxxxxxx"

com="wget -O  - https://"+username+":"+password+"@mail.google.com/mail/feed/atom -q --no-check-certificate" 
temp=os.popen(com)
msg=temp.read()
index=string.find(msg,"<fullcount>")
index2=string.find(msg,"</fullcount>")
msg = (msg[index+11:index2]) + ' new mail(s)'

try:
    import pynotify
    icon = 'file://home/jelle/Projects/Notify/gmail.png'
    if pynotify.init("My Application Name"):
        n = pynotify.Notification("GMail", msg, icon)
        n.show()
    else:
        print "there was a problem initializing the pynotify module"
except:
       print "you don't seem to have pynotify installed"
