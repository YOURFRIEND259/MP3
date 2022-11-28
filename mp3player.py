import pygame as pg
import tkinter as tk
from tkinter import filedialog
from pygame import mixer

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

    def load(self):
        directory=filedialog.askopenfilenames()
        for i in directory:
            self.playlist.append(i)
        for i in directory:
            song_name=i[i.rfind('/')+1:]
            songz[i]=song_name
            print(songz)
            try:
                songbox.insert(tk.END,song_name)
                self.play_restart.set("Play")
            except:
                print("error")

    """
    BUTTON FUNCTIONS
    """
    # global ispaused
    # ispaused=False

    def play(self):
        if self.playlist:
            directory=self.playlist[self.actual_song ]
            mixer.init()
            mixer.music.load(directory)
            mixer.music.set_volume(0.01)
            mixer.music.set_endevent(self.SONG_END)
            mixer.music.play(1, 0.0)
            
            if not self.playing:   
                
                self.playing=True
                # self.ispaused=False
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
        global select
        select=songbox.curselection()
        if select[0]>=len(songz)-1:
            next_song=(list(songz.keys())[0])
            print(next_song)
            select=select[0]+1
        else:
            next_song=(list(songz.keys())[select[0]+1])
            print(next_song)
            select=select[0]+1
        # next_song=songbox.curselection()
        # if next_song[0]>=len(songz)-1:
        #     next_song=next_song[0]+1
        # else:
        #     next_song=next_song[0]-len(songz)-1
        song=songbox.get(next_song)
        mixer.music.load(songz[song])
        print("select",songz[song])
        mixer.music.play()
        self.play_restart.set('Pause')
        self.playing=True
    
    def back(self):
        select=songbox.curselection()
        if select[0]<=0:
            next_song=(list(songz.keys())[select[-1]])
            
            print(next_song)
            select=select[0]-1
        else:
            next_song=(list(songz.keys())[0])
            print(next_song)
            select=select[0]+1
            
        mixer.music.load(songz[next_song])
        print("select",songz[next_song])
        mixer.music.play()
        self.play_restart.set('Pause')
        self.playing=True

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