import pygame as pg
import tkinter as tk
from tkinter import filedialog
from pygame import mixer
import math
import time



"""
TIMER
"""
def calculate_time(func):
     
    # added arguments inside the inner1,
    # if function takes any arguments,
    # can be added like this.
    def inner1(*args, **kwargs):
 
        # storing time before function execution
        begin = time.time()
         
        func(*args, **kwargs)
 
        # storing time after function execution
        end = time.time()
        print("Total time taken in : ", func.__name__, end - begin)
 
    return inner1




root=tk.Tk()
songbox=tk.Listbox(root,bg="black",fg="lightgreen",width=60)
songz={}

class Musicplayer:
    def __init__(self,window) -> None:
        window.geometry('400x300')
        window.title("Music Player")
        window.resizable(0,0)
        

        self.play_restart=tk.StringVar()
        # self.pause_resume=tk.StringVar()
        self.play_restart.set('Play')
        # self.pause_resume.set('Pause')
        self.isrepeat=tk.IntVar


        """
        BUTTONS
        """
        repeat_box=tk.Checkbutton(window, text='repeat',variable=self.isrepeat, onvalue=1, offvalue=0, command=self.repeat)
        repeat_box.pack()

        back_button=tk.Button(window,text="Back", font=20, command=self.back)
        back_button.place(x=200,y=250, anchor='center')

        forward_button=tk.Button(window,text="Forward", font=20, command=self.forward)
        forward_button.place(x=100,y=250, anchor='center')

        load_button=tk.Button(window,text="Load",width=10, font=20, command=self.load)
        load_button.place(x=300,y=250, anchor='center')

        play_button=tk.Button(window,textvariable=self.play_restart,width=10, font=20, command=self.play)
        play_button.place(x=50,y=250, anchor='center')


        stop_button=tk.Button(window,text="Stop", font=160, command=self.stop)
        stop_button.place(x=150,y=250, anchor='center')


        """
        STATEMENTS
        """
        self.playing=False
        self.ispaused=False
        self.SONG_END = pg.USEREVENT + 1
        self.actual_song = 0
        self.playlist=list()

    @calculate_time
    def load(self):
        source=filedialog.askopenfilenames()
        for i in source:
            self.playlist.append(i)
        for i in source:
            song_name=i[i.rfind('/')+1:]
            songz[i]=song_name
            print(songz)
            try:
                songbox.insert(tk.END,song_name)
                self.play_restart.set("Play")
                directory=self.playlist[self.actual_song ]
                mixer.init()
                mixer.music.load(directory)
                mixer.music.set_volume(0.01)
                mixer.music.set_endevent(self.SONG_END)
            except:
                print("error")

    """
    BUTTON FUNCTIONS
    """
    # global ispaused
    # ispaused=False

    def play(self):
        if self.playlist:
    
            if not self.playing:   
                mixer.music.play(1, 0.0)
                self.playing=True
                self.ispaused=False
                self.play_restart.set('Pause')
                print("gra")

            elif not self.ispaused and self.playing:
                mixer.music.pause()
                print("pauza")
                self.ispaused=True
                self.play_restart.set('Resume')
                print("pause",self.ispaused)

            elif self.ispaused and self.playing:
                mixer.music.unpause()
                print("po pauzie?????????")
                self.ispaused=False
                self.play_restart.set('Pause')
                print("resume",self.ispaused)
            
            # self.playing_state = False
            # self.play_restart.set('Restart')
            # self.pause_resume.set('Pause')
        else:
            print("empty playlist")
    

    def forward(self):
        if self.actual_song+2<=len(self.playlist):
            self.actual_song+=1

        else:
            self.actual_song= 0
        mixer.music.load(self.playlist[self.actual_song])
        mixer.music.play()
        self.play_restart.set('Pause')
    
    def back(self):
        if self.actual_song==0:
            self.actual_song=len(self.playlist)-1
        else:
            self.actual_song-=1
        mixer.music.load(self.playlist[self.actual_song])
        mixer.music.play()
        self.play_restart.set('Pause')

    def stop(self):
        mixer.music.stop()
        self.playing=False
        print("stop")
        self.play_restart.set('Play')
        
    # def pause(self):
    #     if not self.ispaused:
    #         mixer.music.pause()
    #         self.ispaused=True
    #         self.pause_resume.set("Resume")
    #     else:
    #         mixer.music.unpause()
    #         self.ispaused=False
    #         self.pause_resume.set("Pause")

    def repeat(self):
        # if (self.isrepeat==1):
        #     mixer.music.play(-1)
        pass
    
    
"""
PROGRAM'S LOOP
"""
songbox.pack(pady=20)
Musicplayer(root)
root.mainloop()