from enum import auto
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from functools import partial
import os
import winsound
import matplotlib.pyplot as plt
from scipy import signal
from scipy.io import wavfile

class SoundEditor:
    def __init__(self) -> None:
        self.window = tk.Tk()
        self.curr_dir = os.getcwd()
        self.create_widgets()
        self.window.mainloop()
    
    def create_widgets(self):
        file_dialog_button = tk.Button(self.window, text="select folder", command=self.get_folder)
        file_dialog_button.grid(row=1, column=1)
        self.list_files()

    
    # function that creates the list of folders in python. super hacky but whatever
    def list_files(self):
        if(hasattr(self, "file_container")):
            self.file_container.destroy()
        
        file_container = ttk.Frame(self.window) 
        tk.Label(file_container, text="file list: ").pack()
        canvas = tk.Canvas(file_container)
        scrollbar = ttk.Scrollbar(file_container, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        file_list = os.listdir(self.curr_dir)
        for filename in file_list:
            if(".wav" in filename):
               # it's hard to pass callback functions with arguments so i need to make this hack
               display_with_file_arg = partial(self.display_wav_file, filename)
               ttk.Button(scrollable_frame, text=filename, command=display_with_file_arg).pack()

        file_container.grid(row=2, column=1)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        self.file_container = file_container
    
    def display_wav_file(self, filename):
        if hasattr(self, "editor_window"):
            self.editor_window.destroy()
        
        self.current_file = filename
        editor_window = tk.Frame(self.window)
        
        #button to play the sound
        play = lambda: winsound.PlaySound(self.curr_dir + "/" + filename, winsound.SND_FILENAME)
        tk.Button(editor_window, text="Play", command=play).pack()

        #display the plot
        sample_rate, data = wavfile.read(self.curr_dir + "/" + filename)
        frequencies, times, spectrogram = signal.spectrogram(data, sample_rate)
        plt.pcolormesh(times, frequencies, spectrogram, shading='auto')
        # plt.imshow(spectrogram)
        plt.ylabel('Frequency [Hz]')
        plt.xlabel('Time [sec]')
        plt.show()

        editor_window.grid(row=2, column=2)
        self.editor_window = editor_window

    def get_folder(self):
        self.curr_dir = filedialog.askdirectory()
        self.list_files()

gui = SoundEditor()

#Create the image display thing