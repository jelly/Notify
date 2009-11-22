#!/usr/bin/python
# Battery Notification, that shows the output of acpi -b
try:
    import pynotify
    import commands
    if pynotify.init("My Application Name"):
        message = commands.getoutput("acpi -b")

        n = pynotify.Notification("Battery", message)
        n.show()
    else:
        print "there was a problem initializing the pynotify module"
except:
    print "you don't seem to have pynotify installed \n  pacman -S python-notify"
