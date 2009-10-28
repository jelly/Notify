#!/usr/bin/python
# Simple Todolist Notification, change the todolist="" to your own todo list file
todolist="/home/jelle/todo"
try:
    import pynotify
    if pynotify.init("My Application Name"):
        f = open(todolist, 'r')
        message =  "".join(f.readlines())
        n = pynotify.Notification("Todo List", message)
        n.show()
    else:
        print "there was a problem initializing the pynotify module"
except:
    print "you don't seem to have pynotify installed \n  pacman -S python-notify"
