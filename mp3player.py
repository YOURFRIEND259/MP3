import pygame as pg
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from pygame import mixer
import math
import time
from threading import Thread


"""
TIMER
"""

def calculate_time(func):
    def inner1(*args, **kwargs):
        begin = time.time()
        func(*args, **kwargs)
        end = time.time()
        print("Total time taken in : ", func.__name__, end - begin)
    return inner1


root = tk.Tk()
songbox = tk.Listbox(root, bg="black", fg="lightgreen", width=60)
songz = {}


class Musicplayer:
    def __init__(self, window) -> None:
        window.geometry('400x300')
        window.title("Music Player")
        window.resizable(0, 0)

        self.play_restart = tk.StringVar()
        self.play_restart.set('Play')
        self.isrepeat = tk.IntVar

        """
        SLIDERS
        """
        volume_slider=ttk.Scale(window, from_=0, to=1,orient=tk.VERTICAL, command=self.volume,length=125,value=0.1)
        volume_slider.place(x=5,y=20)

        """
        BUTTONS
        """
        # repeat_box = tk.Checkbutton(
        #     window, text='repeat', variable=self.isrepeat, onvalue=1, offvalue=0, command=self.repeat)
        # repeat_box.pack()

        back_button = tk.Button(window, text="Back",
                                width=8, font=20, command=self.back)
        back_button.place(x=120, y=240, anchor='center')

        forward_button = tk.Button(window, text="Forward",
                                   font=20, command=self.forward)
        forward_button.place(x=275, y=240, anchor='center')

        load_button = tk.Button(window, text="Load",
                                width=8, font=20, command=self.load)
        load_button.place(x=330, y=280, anchor='center')

        play_button = tk.Button(window, textvariable=self.play_restart,
                                width=8, font=20, command=self.play)
        play_button.place(x=200, y=240, anchor='center')

        stop_button = tk.Button(window, text="Stop",
                                font=160, command=self.stop)
        stop_button.place(x=200, y=280, anchor='center')

        """
        STATEMENTS
        """
        self.playing = False
        self.ispaused = False
        self.SONG_END = pg.USEREVENT + 1
        self.actual_song = 0
        self.playlist = list()

    """
    BUTTON FUNCTIONS
    """
    @calculate_time
    def load(self):
        source = filedialog.askopenfilenames()
        try:
            for i in source:
                song_name = ".".join(i[i.rfind('/')+1:].split(".")[:-1])

                if i in self.playlist:
                    print(f"{song_name} is already on the playlist")
                    continue

                self.playlist.append(i)

                songz[i] = song_name
                print(songz)

                songbox.insert(tk.END, song_name)
                self.play_restart.set("Play")
                directory = self.playlist[self.actual_song]
                mixer.init()
                mixer.music.load(directory)
                mixer.music.set_volume(0.1)
                mixer.music.set_endevent(self.SONG_END)
                self.playing = False
        except:
            print("error")

    def play(self):
        if self.playlist:

            if not self.playing:
                mixer.music.play(1, 0.0)
                self.playing = True
                self.ispaused = False
                self.play_restart.set('Pause')

            elif not self.ispaused and self.playing:
                mixer.music.pause()
                self.ispaused = True
                self.play_restart.set('Resume')
                print("pause", self.ispaused)

            elif self.ispaused and self.playing:
                mixer.music.unpause()
                self.ispaused = False
                self.play_restart.set('Pause')
                print("resume", self.ispaused)

        else:
            print("empty playlist")

    def forward(self):
        try:
            if self.actual_song+2 <= len(self.playlist):
                self.actual_song += 1
            else:
                self.actual_song = 0

            mixer.music.load(self.playlist[self.actual_song])
            print(self.playlist[self.actual_song])
            mixer.music.play()
            self.play_restart.set('Pause')
            self.ispaused = False
            self.playing = True
        except:
            print("there are no songs loaded")

    def back(self):
        try:
            if self.actual_song == 0:
                self.actual_song = len(self.playlist)-1
            else:
                self.actual_song -= 1
            mixer.music.load(self.playlist[self.actual_song])
            mixer.music.play()
            self.play_restart.set('Pause')
            self.ispaused = False
            self.playing = True
        except:
            print("there are no songs loaded")

    def stop(self):
        try:
            mixer.music.stop()
            self.playing = False
            print("stop")
            self.play_restart.set('Play')
        except:
            print("there are no songs loaded")

    def repeat(self):
        # if (self.isrepeat==1):
        #     mixer.music.play(-1)
        pass

    def volume(self,x):
        global volume_slider
        value= float(x)
        mixer.music.set_volume(value)

    def check_music(self):
        """
        Listens to END_MUSIC event and triggers next song to play if current 
        song has finished
        :return: None
        """
        pg.init()
        for event in pg.event.get():
            if event.type == self.SONG_END:
                self.forward()

        

# def checker():
#     while 1:
#         pass
# t1=Thread(target=checker)

"""
PROGRAM'S LOOP
"""
songbox.pack(pady=20, padx=35)

# Musicplayer(root)
# t1.start()
asd=Musicplayer(root)
asd.check_music()
while True:
    asd.check_music()
    root.update()
# root.mainloop()
