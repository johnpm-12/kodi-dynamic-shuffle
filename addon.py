# walks a dir for files
# generates a list of tuples with values of last time each file was played (initially never = unix time 0)
# list is randomly sorted and then heapify'd to get the oldest played file first
# then any slices of the list with all the same last time played get randomly sorted in place
# instead of popping to play the next file, just go through the list
# this makes it semi sorted by order of last played time, but still sufficiently shuffled by the shuffle, heapify, and sliced shuffles
# when a file ends playback, update it's last played time and write it to the json file

import heapq
import json
import random
import time
import os

import xbmc
import xbmcaddon
import xbmcgui


class myPlayer(xbmc.Player):
    def __init__(self):
        xbmc.Player.__init__(self)
        self.stopped = False
        self.cwd = xbmcaddon.Addon().getAddonInfo('path').decode('utf-8')
        with open(self.cwd + '\\playlistdir.txt') as playlistDirFile:
            playlistDirPath = playlistDirFile.readline().decode('utf-8').strip()
        with open(self.cwd + '\\playlist.json') as playlistFile:
            self.playlistDict = json.load(playlistFile)
        playlistObj = []
        for root, _, files in os.walk(playlistDirPath):
            for filename in files:
                filepath = root + '\\' + filename
                if filepath in self.playlistDict:
                    playlistObj.append((self.playlistDict[filepath], filepath))
                else:
                    playlistObj.append((0, filepath))
        random.shuffle(playlistObj)
        heapq.heapify(playlistObj)
        lastTime = 0
        lastIndex = 0
        for index in xrange(len(playlistObj)):
            if playlistObj[index][0] != lastTime:
                startList = playlistObj[:lastIndex]
                shuffleList = playlistObj[lastIndex:index]
                endList = playlistObj[index:]
                random.shuffle(shuffleList)
                playlistObj = startList + shuffleList + endList
                lastTime = playlistObj[index][0]
                lastIndex = index
        startList = playlistObj[:lastIndex]
        shuffleList = playlistObj[lastIndex:]
        random.shuffle(shuffleList)
        playlistObj = startList + shuffleList
        playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        playlist.clear()
        for item in playlistObj:
            fname = item[1].rsplit('\\', 1)[1]
            listitem = xbmcgui.ListItem(fname)
            listitem.setInfo('video', {'Title': fname})
            playlist.add(item[1], listitem=listitem)
        self.play(playlist)

    def onPlayBackStarted(self):
        self.currentFilePath = self.getPlayingFile()

    def onPlayBackEnded(self):
        self.playlistDict[self.currentFilePath] = time.time()
        with open(self.cwd + '\\playlist.json', 'w') as playlistFile:
            json.dump(self.playlistDict, playlistFile)

    def onPlayBackStopped(self):
        self.stopped = True


busyDialog = xbmcgui.DialogBusy()
busyDialog.create()
player = myPlayer()
busyDialog.close()
del busyDialog
while not player.stopped:
    xbmc.sleep(500)
del player
