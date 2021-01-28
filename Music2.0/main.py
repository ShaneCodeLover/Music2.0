"""
Simple Music player App

# prerequisites
1.. Python 3 basic knowledge
2..Little-Bit of tkinter knowledge
3.. Little bit of patience;
4.. Willingness to built cool and fun staff :) :)

Little bit of advance scripting, and many more
Have some, bugs try to fix it
This app is always on update
Can be add many features as you want
Crazy  fun and cool staff 
Followings are the required modules needed
"""
# Required Modules
import tkinter as tk
# os module for directory
import os
# pickle file for storing data
import pickle
from tkinter import ttk
from tkinter import messagebox
from tkinter import *
from tkinter.ttk import *
from tkinter import filedialog
# pip install pygame
import pygame
#for roundoff value (increment +1)
from math import ceil
# for delay 
from time import sleep
# for images
from tkinter import PhotoImage
# for music, length in seconds
from mutagen.mp3 import MP3  # pip install mutagen


# Initialize the mixer 
pygame.mixer.init()
# os.system('cls')

# Hell_yeah class All mains are here
class Hell_Yeah(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master= master
        # Initializing the master window
        self.config(bg='black')
        # Packing whole window
        self.pack()
        # event listener for pause the song just press space-bar on keyboard
        root.bind('<space>', self.pause_song)
        # event listener for previous song left arrow
        root.bind('<Left>', self.prev_song)
        # event listener for next song right arrow
        root.bind('<Right>', self.next_song)
        # event listener for playall functions
        root.bind('<Up>', self.playall)
        # for down
        root.bind('<Down>', self.loops2)
        # using pickle file
        if os.path.exists('songs.pickle'):
            with open('songs.pickle', 'rb') as f:
                self.playlist = pickle.load(f)
        else:
            self.playlist=[]

        # making some global variables for classes
        self.current = 0 
        self.paused =True
        self.played = False
        self.loop2 = False
        self.shuffled = False
        self.confirm = False

        # Calling all gui components
        self.create_frames()
        self.track_widgets()
        self.control_widgets()
        self.tracklist_widget()
        self.below()
        self.tracklist['text'] = f'Playlist- {str(len(self.playlist))}'

    # For moving text very below
    def below(self):
        def shift():
            x1,y1,x2,y2 = self.canvas2.bbox("marquee")
            if(x2<0 or y1<0): #reset the coordinates
                x1 = self.canvas2.winfo_width()
                y1 = 20
                self.canvas2.coords("marquee",x1,y1)
            else:
                self.canvas2.move("marquee", -20, 0)
            self.canvas2.after(1000//self.fps,shift)
                ############# Main program ###############
        self.canvas2=tk.Canvas(root,bg='black')
        self.canvas2.pack(fill="both", expand=1)
        if self.paused == True:
            self.text5="(::)Advanced Music player with cool features(::)"
        else:
            self.text5="(::)Advanced Music player with cool features(::)"
        self.text3=self.canvas2.create_text(0,-2000,text=self.text5,font=('Consolas',14,'bold italic'),fill='white',tags=("marquee",),anchor='w')
        x1,y1,x2,y2 = self.canvas2.bbox("marquee")
        width = 620
        height = 1
        self.canvas2['width']=width
        self.canvas2['height']=height
        self.fps=2   #Change the fps to make the animation faster/slower
        shift()
    
    # Creating all frames probably there are 3 frames
    def create_frames(self):
        # Main window or track frame or a frame for image and animation as well as Label
        self.track= tk.LabelFrame(self, text='Songs list', font=("times new roman" , 15, 'italic'), bd=4, fg='red', bg='black', relief=tk.GROOVE)
        self.track.config(height=360, width=500)
        self.track.grid(row=0, column=0, padx=10, pady=10)

        # Frames for Songslist :   Here all the songs will be there
        self.tracklist= tk.LabelFrame(self, text='Playlist - ', font=("times new roman" , 15, 'italic'), bd=5, fg='red', bg='black', relief=tk.GROOVE)
        self.tracklist.config(height=400, width=190)
        self.tracklist.grid(row=0, column=2, padx=10,rowspan=2)

        # Frames for control menu:  here all required controls and progressbar will be there
        self.controls= tk.LabelFrame(self, font=("times new roman" , 25, 'italic'), bd=2, fg='white', bg='black', relief=tk.GROOVE)
        self.controls.config(height=80, width=580)
        self.controls.grid(row=1, column=0, padx=10, pady=10)
        self.volume = tk.DoubleVar()

        # volume bar or volume slider
        self.slider = ttk.Scale(self, from_=10, cursor='hand2', to = 0, orient=tk.VERTICAL, variable=self.volume, command=self.change_volume,length=480)
        self.slider.set(8)
        self.slider.grid(row=0, column=1, rowspan=2, pady=10)

    def  track_widgets(self):
        # initialising the main canvas for track
        self.canvas = tk.Label(self.track)
        self.canvas.configure(width=520,height=350)
        self.canvas.grid(row=0, column=0, columnspan=2)
        # defaault image for caanvas which will be changed during the song 
        self.canvas['image'] = img

        # Label for appearing all the songs
        self.songtrack = tk.Label(self.track, font=("times new roman", 15, "italic"), bg="black", fg="dark blue", text="Advanced Music player")
        self.songtrack.config(width=45, height=1)
        self.songtrack.grid(row=1, column=0)


    # All control widgets like play pause next previous , progressbar etc.
    def control_widgets(self):
        # Initial button for loading the songs
        self.loadSongs = tk.Button(self.controls, bg='black', fg='white', font=('consolas',17,'italic'), text="Load-Song", command=self.retreive_songs)
        self.loadSongs.config(height=1)
        self.loadSongs.grid(row=0, column=0, padx=5)

        # setting the loop button as per Button orderss
        self.loop = tk.Button(self.controls,border=1, bg='black', image=loop, command=self.loops2,cursor="hand2", activebackground="black")
        self.loop.config(height=45, width=48)
        self.loop.grid(row=0, column=1,pady=2, padx=2)

        # Previous Button: playing the previous song
        self.previous = tk.Button(self.controls, image=prev, bg='black',command=self.prev_song,cursor="hand2", activebackground="black")
        self.previous.config(height=45, width=48)
        self.previous.grid(row=0, column=2,pady=2, padx=2)

        # For playing the songs
        # Main function
        self.play = tk.Button(self.controls, image=play, bg='black', border=1, command=self.pause_song, cursor="hand2", activebackground="black")
        self.play.config(height=45, width=48)
        self.play.grid(row=0, column=3,pady=2, padx=2)
        

        # For next songs: i.e for playing the next song
        self.next_ = tk.Button(self.controls, image=next_, command=self.next_song,bg='black', border=1,  cursor="hand2", activebackground="black")
        self.next_.config(height=45, width=48)
        self.next_.grid(row=0, column=4,pady=2, padx=1)

        # Shuffle or playall Buttons: For playing all songs in ascending order
        self.shuffle = tk.Button(self.controls,  image=shuffle, command=self.playall,bg='black', border=2,  cursor="hand2", activebackground="black")
        self.shuffle.config(height=45, width=120)
        self.shuffle.grid(row=0, column=5, pady=2, padx=2)

        # Setting the value of volume var
        
        
        # progressbar: showing how much song been played
        self.progress_bar = Progressbar(self.controls, style="red.Horizontal.TProgressbar", mode='determinate', orient=tk.HORIZONTAL, length=530)
        self.progress_bar.grid(row=1, columnspan=7)

    #  tracklist widgets
    def tracklist_widget(self):
        # scroll bar for tracklist
        self.scrollbar = tk.Scrollbar(self.tracklist, orient=tk.VERTICAL)
        self.scrollbar.grid(row=0, column=1, sticky='ns', rowspan=5)

        self.scrollbar2 = tk.Scrollbar(self.tracklist, orient=tk.HORIZONTAL)
        self.scrollbar2.grid(row=5, column=0, sticky='ew', columnspan=3)
        
        
        # List of all the songs
        self.list = tk.Listbox(self.tracklist, cursor='hand2', bg='black', fg='blue', font=('times new roman', 12, "italic"), selectmode=tk.SINGLE, yscrollcommand=self.scrollbar.set, selectbackground='sky blue')
        # calling the enumerate_ function for the purpose of adding the song
        self.enumerate_()
        self.list.config(height=22)
        # Binding the list with double click
        self.list.bind('<Double-1>', self.song)
        # Binding the list return function or say Enter
        self.list.bind('<Return>', self.song)
        # Configuring the scrollbar
        self.scrollbar.config(command=self.list.yview)
        self.scrollbar2.config(command=self.list.xview)
        self.list.grid(row=0, column=0, rowspan=5)

    # Retreeiving the songs from the files
    def retreive_songs(self):
        # blank list
        self.songlist = []
        # calling askdirectory
        # or opening the filedialogue
        directory = filedialog.askdirectory()
        for roots, dirs, files in os.walk(directory):
            for file in files:
                if os.path.splitext(file)[1]=='.mp3':
                    path = (roots + '/' + file).replace('\\','/')
                    self.songlist.append(path)

        # Dumping all the songs in pickle file
        with open('songs.pickle', 'wb') as f:
            pickle.dump(self.songlist, f)
        self.playlist = self.songlist
        # using text function of tracklist
        self.tracklist['text'] = f'Playlist- {str(len(self.playlist))}'
        self.list.delete(0, tk.END)
        # Enumerate the songs
        self.enumerate_()

    # enumerateing the function
    def enumerate_(self):
        # appending all the values to self.list
        for index, song in enumerate(self.playlist):
            self.list.insert(index, os.path.basename(song))
        
    # Main function for songs
    def song(self, event=None):
        #  unpacking the previous vanvas2
        try:
            self.canvas2.pack_forget()
        except:
            pass
        self.paused = False
        try:
            if event is not None:
                self.current = self.list.curselection()[0]
                for i in range(len(self.playlist)):
                    self.list.itemconfig(i, bg='black')
            pygame.mixer.music.load(self.playlist[self.current])
            self.songtrack['text'] = os.path.basename(self.playlist[self.current])
            self.g = f"----Now playing-{os.path.basename(self.playlist[self.current])}----"
            if self.paused == False:
                def shift():
                    x1,y1,x2,y2 = self.canvas2.bbox("marquee")
                    if(x2<0 or y1<0): #reset the coordinates
                        x1 = self.canvas2.winfo_width()
                        y1 = 20
                        self.canvas2.coords("marquee",x1,y1)
                    else:
                        self.canvas2.move("marquee", -20, 0)
                    self.canvas2.after(1000//self.fps,shift)
                ############# Main program ###############
                self.canvas2=tk.Canvas(root,bg='black')
                self.canvas2.pack(fill="both", expand=1)
                self.text5=self.g
                self.text3=self.canvas2.create_text(0,-2000,text=self.text5,font=('Consolas',14,'bold italic'),fill='white',tags=("marquee",),anchor='w')
                x1,y1,x2,y2 = self.canvas2.bbox("marquee")
                width = 620
                height = 1
                self.canvas2['width']=width
                self.canvas2['height']=height
                self.fps=2   #Change the fps to make the animation faster/slower
                shift()
            else:
                pass
        except:
            messagebox.showerror('error', "Please select the playlist")
        self.song2 = MP3(self.playlist[self.current])
        self.songlength = self.song2.info.length
        self.play['image']= pause
        self.played = True
        try:
            self.canvas.grid_forget()
        except:
            pass
        self.canvas = tk.Label(self.track)
        self.canvas.configure(width=520,height=350)
        self.canvas.grid(row=0,column=0, columnspan=2)
        if self.paused == False:
            self.l = AnimatedGIF(self.canvas, "12.gif")
            self.l.pack()
        else:
            self.canvas['image'] = img
        self.list.activate(self.current)
        self.list.itemconfigure(self.current, bg='sky blue')
        self.progress_bar['value'] = 0
        self.progress_bar['maximum'] = ceil(self.songlength)
        self.x = 0
        pygame.mixer.music.play()
        try:
            for i in range(self.x, ceil(self.songlength)):
                sleep(1)
                self.x = self.x + 1
                self.progress_bar['value'] += 1
                self.progress_bar.update()
                if self.x == ceil(self.songlength) or self.x > ceil(self.songlength):
                    break
                if not self.paused:
                    continue
                else:
                    break
        except:
            pass
        if self.shuffled == True:
            if self.current == 0:
                self.current+=1
            elif self.current > 0 and self.current < len(self.playlist) - 1:
                self.current +=1
            elif self.current == len(self.playlist) - 1:
                self.current = 0
            self.song()
        else:
            pass
        if self.loop2 == True:
            self.song()
        else:
            pass
        try:
            self.canvas.grid_forget()
        except:
            pass
        self.canvas = tk.Label(self.track)
        self.canvas.configure(width=520,height=350)
        self.canvas.grid(row=0,column=0, columnspan=2)
        self.canvas['image'] = img

    # Main function for pause and unpause
    def pause_song(self, event=None):
        # changing canvas picture i.e animation to music picture
        if not self.paused:
            self.paused = True
            try:
                self.canvas2.pack_forget()
            except:
                pass
            def shift():
                x1,y1,x2,y2 = self.canvas2.bbox("marquee")
                if(x2<0 or y1<0): #reset the coordinates
                    x1 = self.canvas2.winfo_width()
                    y1 = 20
                    self.canvas2.coords("marquee",x1,y1)
                else:
                    self.canvas2.move("marquee", -20, 0)
                self.canvas2.after(1000//self.fps,shift)
                    ############# Main program ###############
            self.canvas2=tk.Canvas(root,bg='black')
            self.canvas2.pack(fill="both", expand=1)
            self.text5="(::)Song Paused click play button or press spacebar on your keyboard to resume(::)"
            self.text3=self.canvas2.create_text(0,-2000,text=self.text5,font=('Consolas',14,'bold italic'),fill='white',tags=("marquee",),anchor='w')
            x1,y1,x2,y2 = self.canvas2.bbox("marquee")
            width = 620
            height = 1
            self.canvas2['width']=width
            self.canvas2['height']=height
            self.fps=2  #Change the fps to make the animation faster/slower
            shift()
            try:
                self.canvas.grid_forget()
            except:
                pass
            self.canvas = tk.Label(self.track)
            self.canvas.configure(width=520,height=350)
            self.canvas.grid(row=0,column=0, columnspan=2)
            if self.paused == False:
                self.l = AnimatedGIF(self.canvas, "12.gif")
                self.l.pack()
            else:
                self.canvas['image'] = img
            if self.shuffled == True:
                self.shuffled = False
            pygame.mixer.music.pause()
            self.play['image'] = play
            self.progress_bar['value'] = self.x
            self.progress_bar.update()
        else:
            # making song resume i.e calling unpause function as well as changing canvas picture
            if self.played == False:
                self.song()
            self.paused = False
            if self.confirm == True:
                self.shuffled = True
            try:
                self.canvas.grid_forget()
            except:
                pass
            try:
                self.canvas2.pack_forget()
            except:
                pass
            if self.paused == False:
                def shift():
                    x1,y1,x2,y2 = self.canvas2.bbox("marquee")
                    if(x2<0 or y1<0): #reset the coordinates
                        x1 = self.canvas2.winfo_width()
                        y1 = 20
                        self.canvas2.coords("marquee",x1,y1)
                    else:
                        self.canvas2.move("marquee", -20, 0)
                    self.canvas2.after(1000//self.fps,shift)
                ############# Main program ###############
                self.canvas2=tk.Canvas(root,bg='black')
                self.canvas2.pack(fill="both", expand=1)
                self.text5=self.g
                self.text3=self.canvas2.create_text(0,-2000,text=self.text5,font=('Consolas',14,'bold italic'),fill='white',tags=("marquee",),anchor='w')
                x1,y1,x2,y2 = self.canvas2.bbox("marquee")
                width = 620
                height = 1
                self.canvas2['width']=width
                self.canvas2['height']=height
                self.fps=2   #Change the fps to make the animation faster/slower
                shift()
            else:
                pass
            self.canvas = tk.Label(self.track)
            self.canvas.configure(width=520,height=350)
            self.canvas.grid(row=0,column=0, columnspan=2)
            self.l = AnimatedGIF(self.canvas, "12.gif")
            self.l.pack()
            pygame.mixer.music.unpause()
            self.play['image'] = pause
            # Resuming the progressbar
            try:
                for i in range(self.x, ceil(self.songlength)):
                    sleep(1)
                    self.x = self.x + 1
                    self.progress_bar['value'] += 1
                    self.progress_bar.update()
                    if self.x == ceil(self.songlength) or self.x > ceil(self.songlength):
                        break
                    if not self.paused:
                        continue
                    else:
                        break
            except:
                pass
            if self.shuffled == True:
                if self.current == 0:
                    self.current+=1
                elif self.current > 0 and self.current < len(self.playlist) - 1:
                    self.current +=1
                elif self.current == len(self.playlist) - 1:
                    self.current = 0
                self.song()
            else:
                pass
            if self.loop2 == True:
                self.song()
            else:
                pass
            try:
                self.canvas.grid_forget()
            except:
                pass
            # Making the previous canvas image
            self.canvas = tk.Label(self.track)
            self.canvas.configure(width=520,height=350)
            self.canvas.grid(row=0,column=0, columnspan=2)
            self.canvas['image'] = img

    # for playing the previous song
    def prev_song(self, event=None):
        if self.current > 0:
            self.current -= 1
        else:
            self.current = 0
        self.list.itemconfigure(self.current + 1, bg='white')
        self.song()

    # for playing the next song
    def next_song(self, event=None):
        if self.current < len(self.playlist) - 1:
            self.current += 1
        else:
            self.current = 0
        self.list.itemconfigure(self.current + 1, bg='white')
        self.song()

    # for playing all the song from up to down
    def playall(self, event=None):
        if self.shuffled == False:
            self.shuffled = True
            self.confirm = True
            self.shuffle['image'] = shuffle2
        elif self.shuffled == True:
            self.shuffled = False
            self.confirm = False
            self.shuffle['image'] = shuffle

    # For  looping the song or making repeating all songs
    def loops2(self, event=None):
        if self.loop2 == False:
            self.loop2 = True
            self.loop['image'] = loop2
        elif self.loop2 == True:
            self.loop2 = False
            self.loop['image'] = loop

        self.song()
    
    # For changing the volumes
    def change_volume(self, event=None):
        self.v = self.volume.get()
        pygame.mixer.music.set_volume(self.v/10)
        
# requirements of animations
# import tkinter
from tkinter import PhotoImage
# ttk
from tkinter.ttk import Label
# pip install pillow
from PIL import Image, ImageTk

# class for playing the animation
class AnimatedGIF(Label, object):
    def __init__(self, master, path, forever=True):
        self._master = master
        self._loc = 0
        self._forever = forever

        self._is_running = False

        im = Image.open(path)
        self._frames = []
        i = 0
        try:
            while True:
                photoframe = ImageTk.PhotoImage(im.copy().convert('RGBA'))
                self._frames.append(photoframe)

                i += 1
                im.seek(i)
        except EOFError: pass
        
        self._last_index = len(self._frames) - 1

        try:
            self._delay = im.info['duration']
        except:
            self._delay = 10

        self._callback_id = None

        super(AnimatedGIF, self).__init__(master, image=self._frames[0])

    def start_animation(self, frame=None):
        if self._is_running: return

        if frame is not None:
            self._loc = 0
            self.configure(image=self._frames[frame])

        self._master.after(self._delay, self._animate_GIF)
        self._is_running = True

    def stop_animation(self):
        if not self._is_running: return

        if self._callback_id is not None:
            self.after_cancel(self._callback_id)
            self._callback_id = None

        self._is_running = False

    def _animate_GIF(self):
        self._loc += 1
        self.configure(image=self._frames[self._loc])

        if self._loc == self._last_index:
            if self._forever:
                self._loc = 0
                self._callback_id = self._master.after(self._delay, self._animate_GIF)
            else:
                self._callback_id = None
                self._is_running = False
        else:
            self._callback_id = self._master.after(self._delay, self._animate_GIF)

    def pack(self, start_animation=True, **kwargs):
        if start_animation:
            self.start_animation()

        super(AnimatedGIF, self).pack(**kwargs)

    def grid(self, start_animation=True, **kwargs):
        if start_animation:
            self.start_animation()

        super(AnimatedGIF, self).grid(**kwargs)
        
    def place(self, start_animation=True, **kwargs):
        if start_animation:
            self.start_animation()

        super(AnimatedGIF, self).place(**kwargs)
        
    def pack_forget(self, **kwargs):
        self.stop_animation()

        super(AnimatedGIF, self).pack_forget(**kwargs)

    def grid_forget(self, **kwargs):
        self.stop_animation()

        super(AnimatedGIF, self).grid_forget(**kwargs)
        
    def place_forget(self, **kwargs):
        self.stop_animation()

        super(AnimatedGIF, self).place_forget(**kwargs)

    
root = tk.Tk()
root.title("MP")
root.config(bg="black")
root.geometry('790x577')
root.iconbitmap('M.ico')
root.resizable(0,0)

# Here import the PIL pip install pillow
from PIL import ImageTk, Image
image = Image.open('music.jpg')
image = image.resize((524,354), Image.ANTIALIAS)
img = ImageTk.PhotoImage(image)


image = Image.open('pause.png')
image = image.resize((45,46), Image.ANTIALIAS)
pause = ImageTk.PhotoImage(image)

image = Image.open('previous.png')
image = image.resize((45,46), Image.ANTIALIAS)
prev = ImageTk.PhotoImage(image)

image2 = Image.open('play.png')
image2 = image2.resize((45,46), Image.ANTIALIAS)
play = ImageTk.PhotoImage(image2)


image2 = Image.open('shuffle.png')
image2 = image2.resize((45,46), Image.ANTIALIAS)
shuffle = ImageTk.PhotoImage(image2)

image2 = Image.open('shuffle2.png')
image2 = image2.resize((45,46), Image.ANTIALIAS)
shuffle2 = ImageTk.PhotoImage(image2)


image = Image.open('next.png')
image = image.resize((45,46), Image.ANTIALIAS)
next_ = ImageTk.PhotoImage(image)


image = Image.open('loop.jpg')
image = image.resize((45,46), Image.ANTIALIAS)
loop = ImageTk.PhotoImage(image)

image = Image.open('loop2.png')
image = image.resize((45,46), Image.ANTIALIAS)
loop2 = ImageTk.PhotoImage(image)

window = Hell_Yeah(master=root)
window.mainloop()




# Just a small idea please try to fix bugs and modify it
