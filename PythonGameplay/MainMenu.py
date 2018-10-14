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
ballSize = 25
cv = Canvas(tk, width=cvWidth, height=cvHeight)
tk.title("Recorder Hero")
cv.pack()
radioFrame = Frame(tk)
recorderHeroTitleImage = ImageTk.PhotoImage(image=Image.open('recorderHero-500.jpg'))

#default difficulty
songDifficulty = Song.Difficulty.EASY
songDifficulty_radioVariable = StringVar(value=songDifficulty.name)


def createMainMenu():
    global songDifficulty_radioVariable
    radioFrame.pack()

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
    cv.delete("all")
    radioFrame.pack_forget()
    startTime = time.time()
    MainGameplay.startGame(cv, song, songDifficulty, startTime, cvWidth, cvHeight, ballSize, pixelsMovedPerSec=150, initialSongOffest=0)
    createMainMenu()

createMainMenu()
tk.mainloop()