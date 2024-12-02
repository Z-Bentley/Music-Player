import os
import pygame
from pygame import mixer
import random
import threading
import time

playlistFolder = 'audio'

# Starting the mixer
mixer.init()
pygame.init()

playlist = [f for f in os.listdir(playlistFolder) if f.endswith('.mp3')]

currentSongIndex = 0
random.shuffle(playlist)

stillPlay = True
userInitatedChange = False

SONG_END = pygame.USEREVENT + 1
mixer.music.set_endevent(SONG_END)

# songLock = threading.Lock()

def playSong(index):
    global currentSongIndex
    global userInitatedChange
    
    currentSongIndex = index
    songPath = os.path.join(playlistFolder, playlist[currentSongIndex])
    mixer.music.load(songPath)
    mixer.music.set_volume(0.5)
    mixer.music.play()
    print()
    print("\nNow playing " + playlist[currentSongIndex])
    userInitatedChange = False

def handleUserInterface():
    global currentSongIndex
    global stillPlay
    global userInitatedChange

    while stillPlay:
        print()
        print("Press 'p' to pause")
        print("Press 'r' to resume")
        print("Press 'v' to set volume")
        print("Press 's' to shuffle")
        print("Press 'n' to to skip to the next song")
        print("Press 'b' to go back to the previous song")
        print("Press 'c' to restart the current song")
        print("Press 'e' to exit")

        ch = input("['p', 'r', 'v', 's', 'n', 'b', 'c', 'e']>>> ")

        # userInitatedChange = True
        if ch in ['s', 'n', 'b', 'c']:
            manageManualChange()

        # Pause
        if ch == 'p':
            mixer.music.pause()
        # Resume
        elif ch == 'r':
            mixer.music.unpause()
        # Change Volume
        elif ch == 'v':
            v = float(input("Enter volume(0 to 10): "))
            v = v / 10
            mixer.music.set_volume(v)
        # Shuffle/Reshuffle
        elif ch == 's':
            mixer.music.stop()
            random.shuffle(playlist)
            playSong(0)
        # Next Song
        elif ch == 'n':
            # userInitatedChange = True
            mixer.music.stop()
            nextIndex = (currentSongIndex  + 1) % len(playlist)
            playSong(nextIndex)
        # Previous Song
        elif ch == 'b':
            # userInitatedChange = True
            mixer.music.stop()
            previousIndex = (currentSongIndex - 1) % len(playlist)
            playSong(previousIndex)
        # Current Song from the Beginning
        elif ch == 'c':
            # userInitatedChange = True
            mixer.music.stop()
            playSong(currentSongIndex)
        # Finished Listening/End Program
        elif ch == 'e':
            mixer.music.stop()
            stillPlay = False
            break

        resetSongEndEvent()

# Allow smooth alteration to the current playing song
def manageManualChange():
    global userInitiatedChange
    userInitiatedChange = True
    mixer.music.set_endevent(0)
    mixer.music.stop()

# after manual changes allows for natural playlist progression
def resetSongEndEvent():
    mixer.music.set_endevent(SONG_END)
    global userInitiatedChange
    userInitiatedChange = False

def playMusic():
    global currentSongIndex
    playSong(currentSongIndex)
    global userInitatedChange  

    # Allow the next song to be played while still able to interact with the UI
    inputThread = threading.Thread(target=handleUserInterface)
    inputThread.daemon = True
    inputThread.start()
    
    while stillPlay:
        for event in pygame.event.get():
            if event.type == SONG_END and not userInitatedChange:
                nextSong = (currentSongIndex + 1) % len(playlist)
                playSong(nextSong)

        time.sleep(1)
    
    mixer.music.stop()
    mixer.quit()
    pygame.quit()

playMusic()