import tkinter as tk
from tkinter import *
from PIL import ImageTk, Image
import os

root = tk.Tk()
root.title("Akmentini")
root.geometry("375x667") 

# background img
bg_image = Image.open("background.png")  
bg_image = bg_image.resize((375, 667))  
bg_photo = ImageTk.PhotoImage(bg_image)

# Canvas 
canvas = tk.Canvas(root, width=375, height=667)
canvas.pack(fill="both", expand=True)
canvas.create_image(0, 0, image=bg_photo, anchor="nw")  
title_image = Image.open("Akmentiņi.png")  
title_image = title_image.resize((187, 50))  
title_photo = ImageTk.PhotoImage(title_image)

canvas.create_image(187, 80, image=title_photo, anchor="center")
count = tk.IntVar(value=50)

def increase():
    count.set(count.get() + 1)

def decrease():
    count.set(count.get() - 1)


left_img = Image.open("left.png").resize((50, 50))
left_photo = ImageTk.PhotoImage(left_img)

right_img = Image.open("right.png").resize((50, 50))
right_photo = ImageTk.PhotoImage(right_img)

left_btn = tk.Button(root, image=left_photo, borderwidth=0, command=decrease, bg="black")
right_btn = tk.Button(root, image=right_photo, borderwidth=0, command=increase, bg="black")

canvas.create_window(130, 250, window=left_btn)
canvas.create_window(245, 250, window=right_btn)

label = tk.Label(root, textvariable=count, font=("Arial", 20, "bold"), bg="black", fg="white", width=5)
canvas.create_window(187, 250, window=label)

start_img = Image.open("start.png").resize((150, 50))
start_photo = ImageTk.PhotoImage(start_img)

exit_img = Image.open("exit.png").resize((150, 50))
exit_photo = ImageTk.PhotoImage(exit_img)

def start_game():
    print("Game Started!")

def exit_game():
    root.destroy()

start_btn = tk.Button(root, image=start_photo, borderwidth=0, command=start_game, bg="black")
exit_btn = tk.Button(root, image=exit_photo, borderwidth=0, command=exit_game, bg="black")

canvas.create_window(187, 400, window=start_btn)
canvas.create_window(187, 460, window=exit_btn)

# run
root.mainloop()