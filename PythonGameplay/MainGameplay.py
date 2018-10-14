import time
import keyboard
import note
import audio
import server
from enum import Enum

tk = None # dependency-injected from MainMenu


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

    audio.play_note(note.note_for_recorder_press_combination(updatedFingers))

def bootstrap_input():
    if CURRENT_INPUT_MODE is InputMode.IOS_APP:
        server.connect_to_client(didUpdatePressedFingers)
    elif CURRENT_INPUT_MODE is InputMode.KEYBOARD:
        keyboard.configure_keyboard_listener(tk, didUpdatePressedFingers)

# The finger positions currently being pressed.
# This is driven by either the iOS app or the keyboard (depending on the current configuration)
pressedFingers = [0, 0, 0, 0, 0, 0, 0]


#################
# Main run loop #
#################

def startGame(canvas, fingerPositions, startTime, cvWidth, cvHeight, ballSize, pixelsMovedPerSec, initialSongOffest):
    #initailize noteline

    noteLine = canvas.create_line(cvWidth/5, 0, cvWidth/5, cvHeight, width='25', fill='gray')
    tempLine = canvas.create_line(cvWidth/5, 0, cvWidth/5, cvHeight, fill='black')
    goodNoteBoundL = cvWidth/5 - ballSize
    goodNoteBoundR = cvWidth/5 + ballSize
    pointDisplay = canvas.create_text(cvWidth - 80, 20, text='Points: 0')
    darkLineBallList = []

    #create dark lineball markers
    for i in range(0, len(pressedFingers)):
        darkLineBall = canvas.create_oval(goodNoteBoundL + 12, (i * 50) + 150,
                                      goodNoteBoundL + 12 + ballSize, (i * 50) + 150 + ballSize,
                                      fill='gray')
        darkLineBallList.append(darkLineBall)

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
                #print("startPos" + str(ballXPos))
                ball = canvas.create_oval(ballXPos, (i * 50) + 150, ballXPos + ballSize, (i * 50) + 150 + ballSize,
                                      fill='black')
                newBallColumn.append(ball)
        #append the time of col to end of newBallColumn
        newBallColumn.append(ballColumn[-1])
        ballColumnsOnCanvas.append(newBallColumn)
        #print ("columnAdded")

    detectIndex = 0
    points = 0
    outsidePressLength = 1
    mistake = True
    columnPassed = False
    endofNotes = False
    #note movement
    while(True):

        server.check_for_updates()

        currentTime = time.time()
        #move all balls one 'movement'
        for ballColumn in ballColumnsOnCanvas:
            #print("ballColumn: " + str(ballColumn))
            for ball in ballColumn[0:len(ballColumn) - 1]:
                ballColSongTime = ballColumn[-1]
                #print("ballColumnSongTime: " + str(ballColSongTime))
                #print("preMove X coord" + str(canvas.coords(ball)[0]))
                #the 0 is for the y movement; temp offset of initialSongOffset Ex:(cvWidth + 60)
                ballXPos = initialSongOffest + ((ballColSongTime - (currentTime - startTime)) * pixelsMovedPerSec)
                #print("ballXPos " + str(ballXPos))
                canvas.move(ball, ballXPos - canvas.coords(ball)[0], 0)
        canvas.update()

        time.sleep(0.001)


        #after all ball columns have been updated
        #detect if proper notes are pressed in noteLine
        #have negative effect if notes pressed outside

        columnToDetect = ballColumnsOnCanvas[detectIndex]
        #if the left xValue for column or right XValue are within goodNoteLine
        colXLeft = canvas.coords(columnToDetect[0])[0]
        colXRight = canvas.coords(columnToDetect[0])[2]
        if (((colXLeft <= goodNoteBoundR + 15) and colXRight > goodNoteBoundR) or ((colXRight >= goodNoteBoundL - 15) and colXLeft < goodNoteBoundL)):

            correctFingering = [0, 0, 0, 0, 0, 0, 0]
            for ball in columnToDetect[0:len(columnToDetect) - 1]:
                #print(canvas.coords(ball))
                canvas.itemconfig(ball, fill='black')
                ballY = canvas.coords(ball)[1]
                correctFingerIndex = int((ballY - 150)/50)
                correctFingering[correctFingerIndex] = 1

            #temporary markers for what 'holes' are being pressed
            for lineBall in darkLineBallList:
                #unfill lineballs
                canvas.itemconfig(lineBall, fill='gray')
            for i in range(0, len(pressedFingers)):
                if (pressedFingers[i] == 1):
                    #fill selected lineballs as 'selected'
                    canvas.itemconfig(darkLineBallList[i], fill='#e8ecf2')
            # #refill moving ball(s) so that they will be over the lineballs
            # for closeBalls in ballColumnsOnCanvas[detectIndex]:
            #     canvas.itemconfig(closeBalls, fill='black')
            #if at any point the proper fingers were pressed
            if (pressedFingers == correctFingering):
                for ball in columnToDetect[0:len(columnToDetect) - 1]:
                    canvas.itemconfig(ball, fill='green')
                mistake = False




        if (colXRight < goodNoteBoundL - 5 and not endofNotes):
            columnPassed = True

        if(mistake and columnPassed):
            #TODO decrement points
            #points -= 10
            canvas.itemconfig(pointDisplay, text="Points: " + str(points))
            columnPassed = False
            #so it will not go out of bounds and also handles last note case
            if (detectIndex < len(ballColumnsOnCanvas) - 1):
                for ball in columnToDetect[0:len(columnToDetect) - 1]:
                    canvas.itemconfig(ball, fill='red')
                detectIndex+=1
            else:
                #canvas.itemconfig(ball, fill='red')
                endofNotes = True
        elif((not mistake) and columnPassed):
            #TODO increment points
            points += 10
            canvas.itemconfig(pointDisplay, text="Points: " + str(points))
            columnPassed = False
            #so it will not go out of bounds and also handles last note case
            if (detectIndex < len(ballColumnsOnCanvas) - 1):
                detectIndex+=1
                mistake = True
            else:
                endofNotes = True

        #print("Points: " + str(points))

        #if the right XCoord of the last column is past the left window boundary end the game
        if (canvas.coords(ballColumnsOnCanvas[-1][0])[2] < 0):
            break
    #end current song and return back to selection menu
    audio.play_note(None)
    time.sleep(3)
    canvas.delete("all")
    #tk.destroy()
