import time

from PIL import ImageTk, Image

import keyboard
import note
import audio
import server
import Song
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

def startGame(canvas, song, difficulty, startTime, cvWidth, cvHeight, ballSize, pixelsMovedPerSec, initialSongOffest):
    global pressedFingers

    song_background_image = ImageTk.PhotoImage(image=Image.open('images/' + song.name.replace('_', ' ') + '-500.jpg'))
    canvas.create_image(250, 545, image=song_background_image)


    #initailize noteline
    noteLine = canvas.create_line(cvWidth/5, 0, cvWidth/5, cvHeight, width='25', fill='gray')
    tempLine = canvas.create_line(cvWidth/5, 0, cvWidth/5, cvHeight, fill='black')
    pointDisplay = canvas.create_text(cvWidth - 80, 20, text='Points: 0')
    finalAccuracyDisplay = canvas.create_text(cvWidth - 200, 200, font=('Times New Roman', 36), text='')
    accuracy = 0
    accuracyDisplay = canvas.create_text(cvWidth - 80, 40, text='Accuracy: ' + str(accuracy) + '%')
    songName = str(song.name).replace("_", " ")
    if ("by" in songName):
        leftSongName = songName[:songName.index(" by")]
        rightSongName = songName[songName.index(" by"):]
        songName = leftSongName + '\n' + rightSongName[1:]

    songTitleDisplay = canvas.create_text(cvWidth - 250, cvHeight - 50, font=('Times New Roman', 20), text=songName)
    darkLineBallList = []

    #create dark lineball markers
    for i in range(0, len(pressedFingers)):
        darkLineBall = canvas.create_oval(cvWidth/5 - 12.5, (i * 50) + 150,
                                          cvWidth/5 - 12.5 + ballSize, (i * 50) + 150 + ballSize,
                                          fill='gray')
        darkLineBallList.append(darkLineBall)

    #initialize all columns of balls out of bounds of the canvas at positions based on their time
    ballColumnsOnCanvas = []

    finger_positions = Song.timed_finger_positions_for_song(song, difficulty)
    rest_timings = Song.rest_timings_for_song(song, difficulty)
    cut_short_timings = Song.cut_short_timings_for_song(song, difficulty)

    for ballColumn in finger_positions:
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

    detectIndex = 0
    points = 0
    ammountCorrect = 0
    outsidePressLength = 1
    mistake = True
    soundHasBeenPlayedForColumn = False
    columnPassed = False
    endofNotes = False

    #note movement
    while(True):

        server.check_for_updates()

        currentTime = time.time()
        currentTimecode = (currentTime - startTime)

        #move all balls one 'movement'
        for ballColumn in ballColumnsOnCanvas:
            for ball in ballColumn[0:len(ballColumn) - 1]:
                ballColSongTime = ballColumn[-1]
                #the 0 is for the y movement; temp offset of initialSongOffset Ex:(cvWidth + 60)
                ballTimecode = (ballColSongTime - currentTimecode)
                ballXPos = initialSongOffest + (ballTimecode * pixelsMovedPerSec)

                canvas.move(ball, ballXPos - canvas.coords(ball)[0], 0)

        canvas.update()


        # if this time code is close to a rest, stop playing
        for rest_time in rest_timings:
            if abs(rest_time - (currentTimecode + 0.75)) < 0.4:
                audio.play_note(None)

        time.sleep(0.001)


        # temporary markers for what 'holes' are being pressed
        for lineBall in darkLineBallList:
            # unfill lineballs
            canvas.itemconfig(lineBall, fill='gray')
        for i in range(0, len(pressedFingers)):
            if (pressedFingers[i] == 1):
                # fill selected lineballs as 'selected'
                canvas.itemconfig(darkLineBallList[i], fill='#e8ecf2')


        #after all ball columns have been updated
        #detect if proper notes are pressed in noteLine
        #have negative effect if notes pressed outside

        columnToDetect = ballColumnsOnCanvas[detectIndex]
        colXLeft = canvas.coords(columnToDetect[0])[0]

        # calculate the correct fingering for this column
        correctFingering = [0, 0, 0, 0, 0, 0, 0]
        for ball in columnToDetect[0:len(columnToDetect) - 1]:
            ballY = canvas.coords(ball)[1]

            correctFingerIndex = int((ballY - 150) / 50)
            correctFingering[correctFingerIndex] = 1

        # if this is the ball is at the center, play the sound
        ballCenterX = colXLeft + ballSize / 2
        recorderLineCenterX = 113
        columnDistanceFromRecorderLine = (ballCenterX - recorderLineCenterX)

        if abs(columnDistanceFromRecorderLine) < 10 and not soundHasBeenPlayedForColumn:
            note_to_play = note.note_for_recorder_press_combination(correctFingering)

            should_cut_short = False

            for cut_short_time in cut_short_timings:
                if abs(cut_short_time - (currentTimecode + 0.75)) < 0.2:
                    should_cut_short = True

            audio.play_note(note_to_play, cut_short=should_cut_short)
            soundHasBeenPlayedForColumn = True

            for ball in columnToDetect[0:len(columnToDetect) - 1]:
                canvas.itemconfig(ball, fill='green')
            mistake = False


        if (columnDistanceFromRecorderLine < -10) and not endofNotes:
            columnPassed = True

        if(mistake and columnPassed):
            audio.play_mistake_audio()

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
            points += 10
            canvas.itemconfig(pointDisplay, text="Points: " + str(points))
            columnPassed = False
            soundHasBeenPlayedForColumn = False
            #so it will not go out of bounds and also handles last note case
            if (detectIndex < len(ballColumnsOnCanvas) - 1):
                detectIndex+=1
                mistake = True
                ammountCorrect += 1
                accuracy = (ammountCorrect / len(ballColumnsOnCanvas)) * 100
                canvas.itemconfig(accuracyDisplay, text='Accuracy: ' + str('%.1f'%accuracy) + '%')
            else:
                endofNotes = True
                ammountCorrect += 1
                accuracy = (ammountCorrect / len(ballColumnsOnCanvas)) * 100
                print(accuracy)
                canvas.itemconfig(accuracyDisplay, text='Accuracy: ' + str('%.1f'%accuracy) + '%')
                if (accuracy == 100.0):
                    canvas.itemconfig(finalAccuracyDisplay, text='Accuracy: ' + str('%.1f'%accuracy) + '%' + '\nPerfect Score!')
                elif (accuracy >= 80.0):
                    canvas.itemconfig(finalAccuracyDisplay, text='Accuracy: ' + str('%.1f'%accuracy) + '%' + '\nPretty Good!')
                elif (accuracy >= 70.0):
                    canvas.itemconfig(finalAccuracyDisplay, text='Accuracy: ' + str('%.1f'%accuracy) + '%'+ '\nAlmost There!')
                elif (accuracy < 70.0):
                    print("test")
                    canvas.itemconfig(finalAccuracyDisplay, text='Accuracy: ' + str('%.1f'%accuracy) + '%'+ '\nTry easy next time')

        #if the right XCoord of the last column is past the left window boundary end the game
        if (canvas.coords(ballColumnsOnCanvas[-1][0])[2] < 0):
            break
    #end current song and return back to selection menu
    audio.play_note(None)
    time.sleep(3)
    canvas.delete("all")
