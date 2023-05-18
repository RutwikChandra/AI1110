import os
import random
import pygame.mixer
import tkinter as tk

# Path to the directory containing the songs
songs_directory = "playlist"

def get_song_names(directory):
    song_names = []
    for filename in os.listdir(directory):
        if filename.endswith(".mp3"):
            song_names.append(os.path.join(directory, filename))
    return song_names

def fisher_yates_shuffle(arr):
    for i in range(len(arr)-1, 0, -1):
        j = random.randint(0, i)
        arr[i], arr[j] = arr[j], arr[i]

# Get the list of song names from the directory
songs = get_song_names(songs_directory)

# Initialize the mixer
pygame.mixer.init()

# Placeholder play_song function
def play_song(song):
    if song not in played_songs:
        pygame.mixer.music.load(song)
        pygame.mixer.music.play()
        update_song_label()
        played_songs.append(song)

# GUI button callbacks
def skip_next():
    pygame.mixer.music.stop()
    playlist_index.set((playlist_index.get() + 1) % len(playlist))
    play_song(playlist[playlist_index.get()])

def stop_music():
    pygame.mixer.music.stop()
    window.destroy()

# Create GUI window
window = tk.Tk()
window.title("Music Player")

# Playlist and index variables
playlist = songs.copy()
fisher_yates_shuffle(playlist)
playlist_index = tk.IntVar()
playlist_index.set(0)

# Song information label
song_label = tk.Label(window, text="Playing song: ")
song_label.pack()

# Next button
next_button = tk.Button(window, text="Next", command=skip_next)
next_button.pack(side=tk.LEFT)

# Stop button
stop_button = tk.Button(window, text="Stop", command=stop_music)
stop_button.pack(side=tk.LEFT)

# Update the song label
def update_song_label():
    current_song = os.path.basename(playlist[playlist_index.get()])
    song_label.config(text="Playing song: " + current_song)

played_songs = []

# Event loop to update the GUI
def update_gui():
    if not pygame.mixer.music.get_busy():
        if len(played_songs) == len(playlist):
            played_songs.clear()  # Clear the played songs list
        playlist_index.set((playlist_index.get() + 1) % len(playlist))
        play_song(playlist[playlist_index.get()])
        update_song_label()
        played_songs.append(playlist[playlist_index.get()])
    window.after(100, update_gui)

# Start playing the first song
play_song(playlist[playlist_index.get()])
update_song_label()

# Start the GUI event loop
window.after(100, update_gui)
window.mainloop()

