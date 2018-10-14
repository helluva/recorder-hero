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
#tk.resizable(False, False)
cv.pack()

def createMainMenu():

    titleDisplay = cv.create_text(cvWidth / 2, 100, text='Recorder Hero', font=('Verdana', 36))

    for (index, song) in enumerate(list(Song.Song)):
        songButton = Button(text='test', command=lambda song=song: startGameplayForSong(song), font=('Verdana', 16))
        window = cv.create_window(cvWidth / 2, 250 + (50 * index), window=songButton, width=300)



def startGameplayForSong(song):
    cv.delete("all")
    startTime = time.time()
    MainGameplay.startGame(cv, Song.timed_finger_positions_for_song(song, Song.Difficulty.MEDIUM), startTime, cvWidth, cvHeight, ballSize, pixelsMovedPerSec=150, initialSongOffest=cvWidth)
    createMainMenu()


# def returnToMenu(canvas):
#     time.sleep(3)
#     canvas.delete("all")
#     createMainMenu()

createMainMenu()
tk.mainloop()