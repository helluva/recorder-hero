from tkinter import *
import time
import Song
import MainGameplay

tk = Tk()
MainGameplay.tk = tk
MainGameplay.bootstrap_input()

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

#this should be a list of lists of tuples 'representing columns' of finger placement coordinates
fingerPositions = []

#below is dummy test call for now
fingerPositions = Song.getFingerPositions()

def createMainMenu():

    titleDisplay = cv.create_text(cvWidth / 2, 100, text='Recorder Hero', font=('Verdana', 36))

    songButton1 = Button(text='Song 1', command=startGame, font=('Verdana', 20))
    songButton1Window = cv.create_window(cvWidth / 2, 250, window=songButton1, width=120)

    songButton2 = Button(text='Song 2', command=startGame, font=('Verdana', 20))
    songButton2Window = cv.create_window(cvWidth / 2, 300, window=songButton2, width=120)

    songButton3 = Button(text='Song 3', command=startGame, font=('Verdana', 20))
    songButton3Window = cv.create_window(cvWidth / 2, 350, window=songButton3, width=120)

    songButton4 = Button(text='Song 4', command=startGame, font=('Verdana', 20))
    songButton4Window = cv.create_window(cvWidth / 2, 400, window=songButton4, width=120)

    songButton5 = Button(text='Song 5', command=startGame, font=('Verdana', 20))
    songButton5Window = cv.create_window(cvWidth / 2, 450, window=songButton5, width=120)


    quitButton = Button(text='Quit', command=tk.destroy, font=('Verdana', 20))
    quitButtonWindow = cv.create_window(cvWidth / 2, 550, window=quitButton, width=120)



def startGame():
    cv.delete("all")
    startTime = time.time()
    MainGameplay.startGame(cv, fingerPositions, startTime, cvWidth, cvHeight, ballSize, pixelsMovedPerSec=70, initialSongOffest=cvWidth)
    createMainMenu()


# def returnToMenu(canvas):
#     time.sleep(3)
#     canvas.delete("all")
#     createMainMenu()

createMainMenu()
tk.mainloop()