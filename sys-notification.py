#!/usr/bin/python
import subprocess
import commands
import time
import os, os.path

# Set your partitions here:
partitions = ['/' ,'/home/jelle' , '/var', '/boot']

# Get the system memory
def get_memory():
    with open('/proc/meminfo', 'r') as fd:
        data = [int(l.split()[1]) for l in fd.readlines()]
    memory =  data[0]  / 1024
    return memory

# Get Free memory
def get_memfree():
    free = 0
    with open('/proc/meminfo', 'r') as fd:
        data = [int(l.split()[1]) for l in fd.readlines()]
    free =  data[1] + data[2] + data[3]
    free = free / 1024
    return free

# Get FreeSpace
def freespace(p):
       s = os.statvfs(p)
       a = (s.f_bsize * s.f_bavail) / 1048576
       a = a / 1024
       return a

# Get Capacity
def diskspace(p):
    s = os.statvfs(p)
    a = (s.f_bsize * s.f_blocks) / 1048576
    a = a / 1024
    return a

# Disk Partitions
def getDisks():
    disks  = ""
    for partition in partitions:
        if partition == '/':
            disks.join("root:  ")
        else:
            disks.join(partition).join(":   ")

        disks += (str(diskspace(partition) - freespace(partition))) 
        disks += "/" 
        disks += str(diskspace(partition)) + " Gb \n"
    return disks

# Get Icon / Theme / Font
def get_theme_name():
        home = os.getenv("HOME")
        file = home + "/.gtkrc-2.0"
        fp = open(file, 'r').read()
        theme = fp.split('\"')[1]
        icon = fp.split('\"')[3]
        font = fp.split('\"')[5]
        themes = "GTK Theme:  " + theme + "\n" + "Icon:  " + icon + "\n" + "Font:  " + font + "\n"
        return themes

# Kernel version
uname = commands.getoutput('uname -r')

# Uptime
uptime = commands.getoutput('uptime')

# Memory
used = get_memory() - get_memfree()

# Updates
updates = commands.getoutput('pacman -Qu | wc -l')


head = "System information"

msg = "Kernel version: " + uname +"\n"
msg += "Uptime: " + str(uptime) + "\n"
msg += "Memory: " + str(used) + " / " + str(get_memory())  + " Mb\n\n"
msg += "Disks" + "\n"
msg += getDisks()
msg += "\n"
msg += str(get_theme_name())
msg += "\n"
msg += "Updates: \n"
msg += "Pacman: " + str(updates) + "\n"

pic="--icon=/home/jelle/archlinux.png"
subprocess.call(['notify-send', pic,head,msg],)
