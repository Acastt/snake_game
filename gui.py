import tkinter as tk
from tkinter import ttk
import pygame

def set_volume(_):
    volume = volume_slider.get() / 100
    pygame.mixer.music.set_volume(volume)  # Update the music volume

# Initialize Pygame
pygame.init()

# Load your background music file (e.g., 'background_music.mp3')
# pygame.mixer.music.load('Sound/crunch.wav')

root = tk.Tk()
root.title("Volume Slider")

# Create a slider
volume_slider = ttk.Scale(root, from_=0.0, to=1.0, orient='horizontal', command=set_volume)
volume_slider.pack(padx=20, pady=10)

# Start playing the background music (loop indefinitely)
# pygame.mixer.music.play(-1)

root.mainloop()