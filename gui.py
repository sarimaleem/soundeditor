import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox

# # Create the application window
# window = tk.Tk()

# # Create the user interface
# frame = tk.Frame(window)
# frame.grid(row=1, column=1)

# for i in range(50):
#     label = ttk.Label(frame, text="this would be a file")
#     label.grid(row=i, column=1)



# quit_button = ttk.Button(window, text="Quit")
# quit_button.grid(row=1, column=2)
# quit_button['command'] = window.destroy

# # Start the GUI event loop
# window.mainloop()

root = tk.Tk()
container = ttk.Frame(root)
canvas = tk.Canvas(container)
scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
scrollable_frame = ttk.Frame(canvas)

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")
    )
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

canvas.configure(yscrollcommand=scrollbar.set)

for i in range(50):
    ttk.Label(scrollable_frame, text="Sample scrolling label").pack()

container.pack()
canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

root.mainloop()