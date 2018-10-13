from tkinter import *
import time
import Song

tk = Tk()
cvWidth = 500
cvHeight = 700
cv = Canvas(tk, width=cvWidth, height=cvHeight)
tk.title("Recorder Hero")
tk.resizable(False, False)
cv.pack()

startTime = time.time()

#this should be a list of lists of tuples 'representing columns' of finger placement coordinates
fingerPositions = []

#below is dummy test call for now
fingerPositions = Song.getFingerPositions()


def tempDisplay(canvas, fingerPositions, startTime, pixelsMovedPerSec, initialSongOffest):

    #initialize all columns of balls out of bounds of the canvas at positions based on their time
    ballColumnsOnCanvas = []
    for ballColumn in fingerPositions:
        newBallColumn = []
        # - 1 to not index the time
        for i in range(0, len(ballColumn) - 1):
            if (ballColumn[i] != 0):
                ballColSongTime = ballColumn[-1]
                #position balls based on time, the X is based on the time value, ballCoordY is the hardcoded height value
                ballXPos = (cvWidth + 200) + (ballColSongTime*pixelsMovedPerSec)
                print("startPos" + str(ballXPos))
                ball = cv.create_oval(ballXPos, (i * 50) + 150, ballXPos + 25, (i * 50) + 150 + 25,
                                      fill='black')
                newBallColumn.append(ball)
        #append the time of col to end of newBallColumn
        newBallColumn.append(ballColumn[-1])
        ballColumnsOnCanvas.append(newBallColumn)
        print ("columnAdded")

    while(True):
        currentTime = time.time()
        #move all balls one 'movement'
        for ballColumn in ballColumnsOnCanvas:
            print("ballColumn: " + str(ballColumn))
            for ball in ballColumn[0:len(ballColumn) - 1]:
                ballColSongTime = ballColumn[-1]
                print("ballColumnSongTime: " + str(ballColSongTime))
                print("preMove X coord" + str(canvas.coords(ball)[0]))
                #the 0 is for the y movement; temp offset of (cvWidth + 60)
                ballXPos = initialSongOffest + ((ballColSongTime - (currentTime - startTime)) * pixelsMovedPerSec)
                print("ballXPos " + str(ballXPos))
                canvas.move(ball, ballXPos - canvas.coords(ball)[0], 0)
        canvas.update()
        time.sleep(0.01)

        #if the right XCoord of the last column is past the left window boundary end the game
        if (canvas.coords(ballColumnsOnCanvas[-1][0])[2] < 0):
            break
    #closes window
    tk.destroy()


tempDisplay(cv, fingerPositions, startTime, pixelsMovedPerSec=30, initialSongOffest=cvWidth)
tk.mainloop()