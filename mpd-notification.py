#!/usr/bin/python
# Dependency:  python-mpd
# Optional: pil for resizing

import sys
from mpd import (MPDClient, CommandError)
from socket import error as SocketError
import subprocess
import urllib
import os
import sys

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

    # Notify 
    head = "Now Playing"

    # With Albumart
    if len(sys.argv) == 1:
        
        msg = nowplaying(client)
        try:
             # import lib for resizing albumart
            import Image

            # Image size
            size = 128, 128

            # Get albumart
            albumartwork = albumart(client)

            # pre: album art is fetched
            # post: display album art 
            # else: display noalbum art
            if os.path.isfile('/home/jelle/.album'):
                # resize image
                im = Image.open(albumartwork)
                im.thumbnail(size)
                im.save(albumartwork, "png")
                pic = '--icon=%(picture)s' %  {'picture': albumartwork}
                subprocess.call(['notify-send', pic,head,msg])
            else:
                subprocess.call(['notify-send', head,msg])
        except:
            print "You don't seem to have pil installed \n  pacman -S pil"

    # Without Albumart 
    elif len(sys.argv) == 2 and sys.argv[1] == "--noalbumart":
        msg = nowplaying(client)
        subprocess.call(['notify-send', head,msg])
        
    else:
        print "unkown option: \n  use '--noalbumart' if you don't want to show albumart else \n  just run it without arguments \n  mpd-notify: version: 0.2"



    


def resizeablum():
    try:
        # import lib for resizing albumart
        import Image

        # Image size
        size = 128, 128

        # Get albumart
        albumartwork = albumart(client)

        # pre: album art is fetched
        # post: display album art 
        # else: display noalbum art
        if os.path.isfile('/home/jelle/.album'):
            # resize image
            im = Image.open(albumartwork)
            im.thumbnail(size)
            im.save(albumartwork, "png")
            pic = '--icon=%(picture)s' %  {'picture': albumartwork}
        else:
            pic = ''
    except:
        print "you don't seem to have pil installed"

        
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

# Pre: there is an mpd connection
# Post: download album art and return the file location
def albumart(client):
        # Get current song dict
        mpddict = client.currentsong()

        # Set image location
        file =  os.getenv("HOME") + '/.album'

        # If artist and album exists , retreive albumart 
        # Else do nothing
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
