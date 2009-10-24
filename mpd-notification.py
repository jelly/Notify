#!/usr/bin/python
# Dependency:  python-mpd
# Optional: pil for resizing

import sys
from mpd import (MPDClient, CommandError)
from socket import error as SocketError
import subprocess
import urllib
import os
import Image

HOST = 'localhost'
PORT = '6600'
PASSWORD =False


CON_ID = {'host':HOST, 'port':PORT}
##  

## Some functions
def mpdConnect(client, con_id):
    """
    Simple wrapper to connect MPD.
    """
    try:
        client.connect(**con_id)
    except SocketError:
        return False
    return True

def mpdAuth(client, secret):
    """
    Authenticate
    """
    try:
        client.password(secret)
    except CommandError:
        return False
    return True
##

def main():
    ## MPD object instance
    client = MPDClient()
    if not mpdConnect(client, CON_ID):
        print 'fail to connect MPD server.'
        sys.exit(1)

    # Auth if password is set non False
    if PASSWORD:
        if mpdAuth(client, PASSWORD):
            print 'Pass auth!'
        else:
            print 'Error trying to pass auth.'
            client.disconnect()
            sys.exit(2)

    # Libnotify message
    head = "Now Playing"
    msg = nowplaying(client)
    albumartwork = albumart(client)

    # Image size
    size = 128, 128
    
    # pre: album art is fetched
    # post: display album art 
    # else: display noalbum art
    if os.path.isfile('/home/jelle/.album'):
        # resize image
        im = Image.open(albumartwork)
        im.thumbnail(size)
        im.save(albumartwork, "png")
        pic = '--icon=%(picture)s' %  {'picture': albumartwork}

        # call notify send
        subprocess.call(['notify-send', pic,head,msg])
    else:
        subprocess.call(['notify-send', head,msg])

# Get Now Playing info
def nowplaying(client):

    # Get Dict with current song info and mpd status
    mpddict = client.currentsong()
    mpdstatus = client.status()

    # Get Random / repeat mode
    if int(mpdstatus['random']) == 0:
        mpddict['random']  = "off"
    else:
        mpddict['random'] = "on"

    if int(mpdstatus['repeat']) == 0:
        mpddict['repeat'] = "off"
    else:
        mpddict['repeat'] = "on"

    # Get the mpd status ( playing / pause)
    mpddict['state'] = mpdstatus['state']

    # Time
    time = mpdstatus['time']
    played = int(time.split(':')[0])
    length = int(time.split(':')[1]) 
    mpddict['played'] = '{0}:{1}'.format(*divmod(played, 60))
    mpddict['length'] = '{0}:{1}'.format(*divmod(length, 60))

    # Concatenate all info in one string
    mpdinfo = '{artist} - {title}\n Album:  {album}\n State:  [ {state} ]  {played} / {length}\n Repeat:  {repeat}  Random:  {random}\n'.format(**mpddict)

    return mpdinfo

def albumart(client):
        # Album Art Part
        mpddict = client.currentsong()

        file =  os.getenv("HOME") + '/.album'
        if mpddict['artist'] == "" and mpddict['album'] == "":
                if os.path.exists(file):
                        os.remove(file)
        else:
                url = 'http://www.albumart.org/index.php?srchkey={artist}+{album}&itempage=1&newsearch=1&searchindex=Music'.format(**mpddict)
                albumart = urllib.urlopen(url).read()
                image = ""
                for line in albumart.split("\n"):
                        if "http://www.albumart.org/images/zoom-icon.jpg" in line:
                                image = line.partition('src="')[2].partition('"')[0]
                                break
                if image:
                        if os.path.exists("/tmp/imagepath") and os.path.exists(file):
                                imagepath = open("/tmp/imagepath").read()
                                if imagepath == image:
                                        pass
                                else:
                                        urllib.urlretrieve(image, file)
                        else:
                                urllib.urlretrieve(image, file)
                        open("/tmp/imagepath","w").write(image)
                else:
                        if os.path.exists(file):
                                os.remove(file)
        return file





if __name__ == "__main__":
    main()
