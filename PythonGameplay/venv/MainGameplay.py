from tkinter import *
import time
import datetime

tk = Tk()
cvWidth = 500
cvHeight = 700
cv = Canvas(tk, width=cvWidth, height=cvHeight)
tk.title("Recorder Hero")
tk.resizable(False, False)
cv.pack()

startTime = time.time()

#eventually this will be the tempo fo the song obtained from somewhere else (will be pipelined in from somewhere)
songSpeed = -1
#this should be a list of lists of tuples 'representing columns' of finger placement coordinates
fingerPositions = []
#below is dummty test for now

#4 Test finger positions for now
#initial X position off of the canvas, Y will be hardcoded constant for each ball Ex: (cvWidth + 50, 150)
#The last tuple is the column's entry second
fingerPositions = [[(100, 150), (), (100, 300), (), (1,)], [(200, 150), (), (), (), (9,)]]
#fingerPositions.append([()])


def tempDisplay(canvas, fingerPositions, songSpeed, startTime, pixelsMovedPerSec):

    #initialize all columns of balls out of bounds of the canvas at positions based on their time
    ballColumnsOnCanvas = []
    for ballColumn in fingerPositions:
        newBallColumn = []
        # to not index the time
        for ballCoord in ballColumn[0:len(ballColumn) - 1]:
            if (ballCoord != ()):
                ballColSongTime = ballColumn[-1][0]
                #position balls based on time, the X is based on the time value, ballCoordY is the hardcoded height value
                ballXPos = (cvWidth + 200) + (ballColSongTime*pixelsMovedPerSec)
                print("startPos" + str(ballXPos))
                ball = cv.create_oval(ballXPos, ballCoord[1], ballXPos + 60, ballCoord[1] + 60,
                                      fill='black')
                newBallColumn.append(ball)
        #append the time of col
        newBallColumn.append(ballColumn[-1])
        ballColumnsOnCanvas.append(newBallColumn)
        print ("columnAdded")

    while(True):
        currentTime = time.time()
        #move all balls one 'movement'
        for ballColumn in ballColumnsOnCanvas:
            print("ballColumn: " + str(ballColumn))
            for ball in ballColumn[0:len(ballColumn) - 1]:
                ballColSongTime = ballColumn[-1][0]
                print("ballColumnSongTime: " + str(ballColSongTime))
                #the 0 is for the y movement; 100 is offset
                ballXPos = ((ballColSongTime - (currentTime - startTime)) * pixelsMovedPerSec)
                canvas.move(ball, ballXPos - canvas.coords(ball)[0], 0)
        canvas.update()
        time.sleep(0.01)

        #if the right XCoord of the last column is past the left window boundary end the game
        if (canvas.coords(ballColumnsOnCanvas[-1][0])[2] < 0):
            break
    tk.destroy()


tempDisplay(cv, fingerPositions, songSpeed, startTime, pixelsMovedPerSec=20)
tk.mainloop()