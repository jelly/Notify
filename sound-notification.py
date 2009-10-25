#!/usr/bin/python
# Simple Volume Notification, that shows volume percentage , sound is on/off
try:
    import pynotify
    import commands
    if pynotify.init("My Application Name"):
        message = commands.getoutput("amixer get Master | awk 'NR==5 { print $4,  $6}'")

        n = pynotify.Notification("Master Volume", message)
        n.show()
    else:
        print "there was a problem initializing the pynotify module"
except:
    print "you don't seem to have pynotify installed \n  pacman -S python-notify"
