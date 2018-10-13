from tkinter import *

#4 Test finger positions for now
#NO NEED FOR COORDS ANYMORE, JUST PUT 1 or 0 for if fingering position present in column
#The last tuple is the column's entry time(second)
def getFingerPositions():
    fingerPositions = [[(100, 150), (), (100, 250), (), (1,)], [(200, 150), (), (), (), (9,)]]
    return fingerPositions