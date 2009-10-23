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


    # Libnotify
    artist = getArtist(client)
    album = getAlbum(client)
    size = 128, 128

    # resize image
    image = str(albumart(artist, album))
    im = Image.open(image)
    im.thumbnail(size)
    im.save(image, "png")

#im.resize((80,80))

    pic =  "--icon=" + image 
    head = "Now Playing"
    msg = nowplaying(client)

    # call notify send
    subprocess.call(['notify-send', pic,head,msg])


def getArtist(client):
    # Get Dict with current song info and mpd status
    mpddict = client.currentsong()
    artist  = mpddict['artist']
    return artist

def getAlbum(client):
    # Get Dict with current song info and mpd status
    mpddict = client.currentsong()
    album  = mpddict['album']
    return album

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

def albumart(artist, album):
        # Album Art Part

        home = os.getenv("HOME")
        if artist == "" and album == "":
                if os.path.exists(home + "/.album"):
                        os.remove(home + "/.album")
        else:
                url = "http://www.albumart.org/index.php?srchkey=" + artist + "+" + album + "&itempage=1&newsearch=1&searchindex=Music"
                albumart = urllib.urlopen(url).read()
                image = ""
                for line in albumart.split("\n"):
                        if "http://www.albumart.org/images/zoom-icon.jpg" in line:
                                image = line.partition('src="')[2].partition('"')[0]
                                break
                if image:
                        if os.path.exists("/tmp/imagepath") and os.path.exists(home + "/.album"):
                                imagepath = open("/tmp/imagepath").read()
                                if imagepath == image:
                                        pass
                                else:
                                        urllib.urlretrieve(image, home + "/.album")
                        else:
                                urllib.urlretrieve(image, home + "/.album")
                        open("/tmp/imagepath","w").write(image)
                else:
                        if os.path.exists(home + "/.album"):
                                os.remove(home + "/.album")
        return home + "/.album"





if __name__ == "__main__":
    main()
