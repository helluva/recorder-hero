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
#default difficulty
songDifficulty = Song.Difficulty.EASY

def createMainMenu():
    radioFrame.pack()

    selectedDifficulty = StringVar()

    rbEasy = Radiobutton(radioFrame, text="Easy", variable=selectedDifficulty, value="E", command=lambda: difficultyChange(Song.Difficulty.EASY))
    rbEasy.grid(row=1, column=1)
    rbEasy.focus_set()

    rbMedium = Radiobutton(radioFrame, text="Medium", variable=selectedDifficulty, value="M", command=lambda: difficultyChange(Song.Difficulty.MEDIUM))
    rbMedium.grid(row=1, column=2)

    rbHard = Radiobutton(radioFrame, text="Hard", variable=selectedDifficulty, value="H", command=lambda: difficultyChange(Song.Difficulty.HARD))
    rbHard.grid(row=1, column=3)


    #titleDisplay = cv.create_text(cvWidth / 2, 100, text='Recorder Hero', font=('Verdana', 36))
    recorderHeroTitleImage = Image.open('recorderHero.jpg')
    print(recorderHeroTitleImage)
    recorderHeroTitleImage = ImageTk.PhotoImage(image=recorderHeroTitleImage, size=100)
    titleDisplay = cv.create_image(cvWidth / 2, 100, image=recorderHeroTitleImage)

    for (index, song) in enumerate(list(Song.Song)):
        songButton = Button(text=song.name.replace('_', ' '), command=lambda song=song: startGameplayForSong(song), font=('Verdana', 16))
        window = cv.create_window(cvWidth / 2, 250 + (50 * index), window=songButton, width=300)

def difficultyChange(newSongDifficulty):
    global songDifficulty
    songDifficulty = newSongDifficulty

def startGameplayForSong(song):
    cv.delete("all")
    radioFrame.pack_forget()
    startTime = time.time()
    print(song)
    print(songDifficulty)
    MainGameplay.startGame(cv, Song.timed_finger_positions_for_song(song, songDifficulty), startTime, cvWidth, cvHeight, ballSize, pixelsMovedPerSec=150, initialSongOffest=cvWidth)
    createMainMenu()

createMainMenu()
tk.mainloop()