from tkinter import *
import time
import Song
import keyboard
from enum import Enum

tk = Tk()



################
# Input handling -- the currently pressed fingers are stored in `pressedFingers`. e.g. [1, 0, 0, 1, 0, 0, 0]
################

class InputMode(Enum):
    # (1) the server that talks to the iOS / macOS recorder app. Primary interaction mode
    IOS_APP = 1
    # (2) the 1-7 keys on the keyboard. Development / debugging mode.
    KEYBOARD = 2

CURRENT_INPUT_MODE = InputMode.KEYBOARD;

def didUpdatePressedFingers(updatedFingers):
    global pressedFingers
    pressedFingers = updatedFingers


if CURRENT_INPUT_MODE is InputMode.IOS_APP:
    pass # todo
elif CURRENT_INPUT_MODE is InputMode.KEYBOARD:
    keyboard.configure_keyboard_listener(tk, didUpdatePressedFingers)



#################
# Tkinter setup #
#################

cvWidth = 500
cvHeight = 700
ballSize = 25
cv = Canvas(tk, width=cvWidth, height=cvHeight)
tk.title("Recorder Hero")
tk.resizable(False, False)
cv.pack()

startTime = time.time()

#this should be a list of lists of tuples 'representing columns' of finger placement coordinates
fingerPositions = []

#below is dummy test call for now
fingerPositions = Song.getFingerPositions()

# The finger positions currently being pressed.
# This is driven by either the iOS app or the keyboard (depending on the current configuration)
pressedFingers = [0, 0, 0, 0, 0, 0, 0]



#################
# Main run loop #
#################

def tempDisplay(canvas, fingerPositions, startTime, pixelsMovedPerSec, initialSongOffest):
    #initailize noteline
    noteLine = cv.create_line(cvWidth/2, 0, cvWidth/2, cvHeight, width='25', fill='gray')
    tempLine = cv.create_line(cvWidth/2, 0, cvWidth/2, cvHeight, fill='black')
    goodNoteBoundL = cvWidth/2 - ballSize
    goodNoteBoundR = cvWidth/2 + ballSize

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
                ball = cv.create_oval(ballXPos, (i * 50) + 150, ballXPos + ballSize, (i * 50) + 150 + ballSize,
                                      fill='black')
                newBallColumn.append(ball)
        #append the time of col to end of newBallColumn
        newBallColumn.append(ballColumn[-1])
        ballColumnsOnCanvas.append(newBallColumn)
        print ("columnAdded")

    #note movement
    while(True):
        currentTime = time.time()
        #move all balls one 'movement'
        for ballColumn in ballColumnsOnCanvas:
            print("ballColumn: " + str(ballColumn))
            for ball in ballColumn[0:len(ballColumn) - 1]:
                ballColSongTime = ballColumn[-1]
                print("ballColumnSongTime: " + str(ballColSongTime))
                print("preMove X coord" + str(canvas.coords(ball)[0]))
                #the 0 is for the y movement; temp offset of initialSongOffset Ex:(cvWidth + 60)
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