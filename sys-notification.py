#!/usr/bin/python
import subprocess
import commands
import time
import os, os.path

# Set the icon here
pic="--icon=/home/jelle/Afbeeldingen/Logos/archlinux.png"
# Set your partitions here:
partitions = ['/' ,'/home/jelle' , '/var']

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
        str_list = [partition,'  ', str(diskspace(partition)-freespace(partition)),"/",str(diskspace(partition)),'Gb \n']

        disks.join(str_list)
        disks += partition + "  "
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
        themes = "Theme: %s\n Icon: %s\n Font: %s\n" % (theme,icon,font)
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
msg = "Kernel version: %s \n Uptime: %s \n Memory: %s / %s Mb\n\n Disks: (used/total)\n %s  \n %s \n Updates: %s \n" % (uname,str(uptime),str(used),str(get_memory()),getDisks(),get_theme_name(),str(updates))

subprocess.call(['notify-send', pic,head,msg],)
