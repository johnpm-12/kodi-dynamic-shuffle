#!python2
import random
import heapq

playlistObj = [
    (79, 'sdf0'),
    (3, 'sdf1'),
    (2, 'sdf2'),
    (1, 'sdf3'),
    (0, 'sdf4'),
    (5, 'sdf5'),
    (6, 'sdf6'),
    (7, 'sdf7')
]
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

print(playlistObj)
