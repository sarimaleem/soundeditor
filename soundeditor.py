import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from functools import partial
import os
import winsound
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure
from scipy import signal
from scipy.io import wavfile
import numpy as np

window_types = [
    'boxcar',
    'triang',
    'blackman',
    'hamming',
    'hann',
    'bartlett',
    'flattop',
    'parzen',
    'bohman',
    'blackmanharris',
    'nuttall',
    'barthann'
]


class SoundEditor:
    def __init__(self) -> None:
        self.window = tk.Tk()
        # TODO remove this in production
        self.curr_dir = os.getcwd() + "/wavfiles"
        self.start_trim = tk.DoubleVar()
        self.end_trim = tk.DoubleVar()
        self.segment_length = tk.DoubleVar()
        self.overlap = tk.DoubleVar()
        self.window_type = tk.StringVar()
        self.window_type.set(window_types[0])
        self.create_widgets()
        self.window.mainloop()

    def create_widgets(self):
        file_dialog_button = tk.Button(
            self.window, text="select folder", command=self.get_folder)
        file_dialog_button.grid(row=1, column=1)
        self.list_files()

    # function that creates the list of folders in python. super hacky but whatever

    def list_files(self):
        if(hasattr(self, "file_container")):
            self.file_container.destroy()

        file_container = ttk.Frame(self.window)
        tk.Label(file_container, text="file list: ").pack()
        canvas = tk.Canvas(file_container)
        scrollbar = ttk.Scrollbar(
            file_container, orient="vertical", command=canvas.yview)
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
                display_with_file_arg = partial(
                    self.display_wav_file, filename)
                tk.Button(scrollable_frame, text=filename,
                          command=display_with_file_arg, width=30).pack()

        file_container.grid(row=2, column=1)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        self.file_container = file_container

    def display_wav_file(self, filename):
        if hasattr(self, "editor_window"):
            self.editor_window.destroy()

        self.current_file = filename
        editor_window = tk.Frame(self.window)
        self.editor_window = editor_window

        # button to play the sound
        def play(): return winsound.PlaySound(
            self.curr_dir + "/" + filename, winsound.SND_FILENAME)
        tk.Button(editor_window, text="Play", command=play).pack()

        sample_rate, data = wavfile.read(self.curr_dir + "/" + filename)
        self.sample_rate = sample_rate
        self.data = data

        # add a slider for the stuff and other stfft options
        tk.Label(editor_window, text="start cut off (seconds)").pack()
        tk.Scale(editor_window, from_=0,
                 to=data.size/sample_rate, variable=self.start_trim, length=500, resolution=0.01, orient=tk.HORIZONTAL).pack()

        tk.Label(editor_window, text="end cut off (seconds)").pack()
        tk.Scale(editor_window, from_=0,
                 to=data.size/sample_rate, variable=self.end_trim, length=500, resolution=0.01, orient=tk.HORIZONTAL).pack()

        tk.Label(editor_window, text="window type").pack()
        tk.OptionMenu(editor_window, self.window_type, *window_types).pack()
        
        tk.Label(editor_window, text="segment length (seconds)").pack()
        tk.Scale(editor_window, from_=0,
                 to=1, variable=self.segment_length, length=500, resolution=0.01, orient=tk.HORIZONTAL).pack()
        
        tk.Label(editor_window, text="overlap (% of segment length)").pack()
        tk.Scale(editor_window, from_=0,
                 to=100, variable=self.overlap, length=500, resolution=1, orient=tk.HORIZONTAL).pack()


        tk.Button(editor_window, text="create graph",
                  command=self.create_graph_editor).pack()
        editor_window.grid(row=2, column=2)

    def create_graph_editor(self):
        if(hasattr(self, "graph_fig")):
            self.graph_fig.destroy()

        graph_fig = tk.Frame(self.window)
        frequencies, times, spectrogram = signal.spectrogram(
            self.data, self.sample_rate, window=self.window_type.get(), nperseg=int(self.segment_length.get() * self.sample_rate), noverlap=int(self.segment_length.get() * self.sample_rate * self.overlap.get() // 100))
        fig = Figure(figsize=(7, 7), dpi=100)
        fig.suptitle(self.current_file)
        ax1 = fig.add_subplot(211)
        ax1.pcolormesh(times, frequencies, spectrogram, shading='auto')
        ax1.set_ylabel('Frequency [Hz]')
        ax2 = fig.add_subplot(212)
        ax2.plot(np.linspace(0, times[-1], self.data.size), self.data)
        ax2.set_ylabel('raw data (amplitude i think?)')
        ax2.set_xlabel('Time [sec]')
        canvas = FigureCanvasTkAgg(fig, master=graph_fig)
        canvas.draw()
        canvas.get_tk_widget().pack()
        toolbar = NavigationToolbar2Tk(canvas, graph_fig)
        toolbar.update()
        canvas.get_tk_widget().pack()
        graph_fig.grid(row=2, column=3)
        self.graph_fig = graph_fig

    def get_folder(self):
        self.curr_dir = filedialog.askdirectory()
        self.list_files()


gui = SoundEditor()

# Create the image display thing
