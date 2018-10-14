import os
from tkinter import *
from PIL import ImageTk, Image
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
cvHeightOffsetForRadioFrameArea = 50
ballSize = 25

cv = Canvas(tk, width=cvWidth, height=cvHeight - cvHeightOffsetForRadioFrameArea)
tk.title("Recorder Hero")
cv.pack()
radioFrame = Frame(tk)
recorderHeroTitleImage = ImageTk.PhotoImage(image=Image.open('images/recorderHero-500.jpg'))

# place the window in the middle of the screen
x = (tk.winfo_screenwidth() / 2) - (cvWidth/2)
y = (tk.winfo_screenheight() / 2) - (cvHeight/2)
tk.geometry('%dx%d+%d+%d' % (cvWidth, cvHeight, x, y - 25))

#default difficulty
songDifficulty = Song.Difficulty.EASY
songDifficulty_radioVariable = StringVar(value=songDifficulty.name)


def createMainMenu():
    global songDifficulty_radioVariable

    rbEasy = Radiobutton(radioFrame,
        text="Easy\n\n", variable=songDifficulty_radioVariable, value="EASY",
        font=('Times New Roman', 15),
        command=lambda: difficultyChange(Song.Difficulty.EASY))

    rbMedium = Radiobutton(radioFrame,
        text="Medium\n\n", variable=songDifficulty_radioVariable, value="MEDIUM",
        font=('Times New Roman', 15),
        command=lambda: difficultyChange(Song.Difficulty.MEDIUM))

    rbHard = Radiobutton(radioFrame,
        text="Hard\n\n", variable=songDifficulty_radioVariable, value="HARD",
        font=('Times New Roman', 15),
        command=lambda: difficultyChange(Song.Difficulty.HARD))

    rbEasy.grid(row=1, column=1)
    rbMedium.grid(row=1, column=2)
    rbHard.grid(row=1, column=3)
    radioFrame.pack()

    global recorderHeroTitleImage
    cv.create_image(250, 155, image=recorderHeroTitleImage)

    for (index, song) in enumerate(list(Song.Song)):
        songButton = Button(text=song.name.replace('_', ' '), command=lambda song=song: startGameplayForSong(song), font=('Times New Roman', 15))
        window = cv.create_window(cvWidth / 2, 350 + (50 * index), window=songButton, width=300)

def difficultyChange(newSongDifficulty):
    global songDifficulty, songDifficulty_radioVariable
    songDifficulty = newSongDifficulty
    songDifficulty_radioVariable.set(newSongDifficulty.name)
    print(songDifficulty_radioVariable.get())

def startGameplayForSong(song):
    global cv
    cv.destroy()
    cv = Canvas(tk, width=cvWidth, height=cvHeight)
    cv.pack()

    radioFrame.pack_forget()
    startTime = time.time()
    MainGameplay.startGame(cv, song, songDifficulty, startTime, cvWidth, cvHeight, ballSize, pixelsMovedPerSec=150, initialSongOffest=0)

    # after the gameplay is over, set up the menu again
    cv.destroy()
    cv = Canvas(tk, width=cvWidth, height=cvHeight - cvHeightOffsetForRadioFrameArea)
    cv.pack()
    createMainMenu()

createMainMenu()

os.system('''/usr/bin/osascript -e 'tell app "Finder" to set frontmost of process "Python" to true' ''')
tk.mainloop()