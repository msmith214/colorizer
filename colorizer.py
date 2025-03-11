import tkinter as tk
from tkinter import filedialog as fd
from PIL import Image, ImageTk, ImageDraw
import pathlib
import os

global altered_image
global preview_image 

def update_input_sample(placeholder):
    input_sample.create_rectangle(0, 0, 80, 80, fill="#"+hex(red_scale_1.get())[2:].rjust(2, "0")+hex(green_scale_1.get())[2:].rjust(2, "0")+hex(blue_scale_1.get())[2:].rjust(2, "0"))

def update_output_sample(placeholder):
    output_sample.create_rectangle(0, 0, 80, 80, fill="#"+hex(red_scale_2.get())[2:].rjust(2, "0")+hex(green_scale_2.get())[2:].rjust(2, "0")+hex(blue_scale_2.get())[2:].rjust(2, "0"))

def open_file():
    filepath = fd.askopenfilename(
        initialdir="/",
        title="Choose a file to alter"
    )
    if filepath:
        global altered_image
        altered_image= Image.open(filepath)
        width, height = altered_image.size
        if height > width:
            altered_image = altered_image.resize((int(400*width/height), 400))
        else:
            altered_image = altered_image.resize((400, int(400*height/width)))
        img = ImageTk.PhotoImage(altered_image)
        for child in picture_frame.winfo_children():
                child.destroy()
        display = tk.Label(picture_frame, image=img)
        display.image = img
        display.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

def preview():
    if altered_image:
        global preview_image
        preview_image = Image.new("RGB", size=altered_image.size)
        for i in range(altered_image.size[0]):
            for j in range(altered_image.size[1]):
                red, green, blue = altered_image.getpixel((i,j))
                if red >= red_scale_1.get()-red_scale_3.get() and red <= red_scale_1.get()+red_scale_3.get() and green >= green_scale_1.get()-green_scale_3.get() and green <= green_scale_1.get()+green_scale_3.get() and blue >= blue_scale_1.get()-blue_scale_3.get() and blue <= blue_scale_1.get()+blue_scale_3.get():
                    red_shift = red_scale_1.get() - red
                    green_shift = green_scale_1.get() - green
                    blue_shift = blue_scale_1.get() - blue
                    preview_image.putpixel((i, j), (red_scale_2.get() - red_shift, green_scale_2.get() - green_shift, blue_scale_2.get() - blue_shift))
                    print("Pixel replaced.")
                else:
                    preview_image.putpixel((i, j), (red, green, blue))
                    print("Pixel not replaced.")
        for child in picture_frame.winfo_children():
            child.destroy()
        img = ImageTk.PhotoImage(preview_image)
        display = tk.Label(picture_frame, image=img)
        display.image = img
        display.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

def save_file():
    global preview_image
    preview_image.save(os.path.abspath(__file__).replace("colorizer.py", "")+"altered-image.jpg")

root=tk.Tk()
root.title("Colorizer")

C = tk.Canvas(root, height=540, width=720)
path = pathlib.Path(__file__).parent

input_frame = tk.Frame(root, padx=10, pady=10)
input_frame.place(x=0, y=0)
input_sample = tk.Canvas(input_frame, width=80, height=80)
input_sample.create_rectangle(0, 0, 80, 80, fill="#ffffff")
text_label_1 = tk.Label(input_frame, text="Color you want to remove:", font=("Arial", 16, "bold"), fg="#dddddd", bd=2, height=2, width=25)
text_label_1.pack()
red_scale_1 = tk.Scale(input_frame, from_=0, to=255, orient=tk.HORIZONTAL, showvalue=False, troughcolor="#aa7777", length=200, command=update_input_sample)
red_scale_1.set(255)
red_scale_1.pack()
green_scale_1 = tk.Scale(input_frame, from_=0, to=255, orient=tk.HORIZONTAL, showvalue=False, troughcolor="#77aa77", length=200, command=update_input_sample)
green_scale_1.set(255)
green_scale_1.pack()
blue_scale_1 = tk.Scale(input_frame, from_=0, to=255, orient=tk.HORIZONTAL, showvalue=False, troughcolor="#7777aa", length=200, command=update_input_sample)
blue_scale_1.set(255)
blue_scale_1.pack()
input_sample.pack(pady=20)

output_frame = tk.Frame(root, padx=10, pady=10)
output_frame.place(x=0, y=210)
output_sample = tk.Canvas(output_frame, width=80, height=80)
output_sample.create_rectangle(0, 0, 80, 80, fill="#ffffff")
text_label_2 = tk.Label(output_frame, text="Color you want to insert:", font=("Arial", 16, "bold"), fg="#dddddd", bd=2, height=2, width=25)
text_label_2.pack()
red_scale_2 = tk.Scale(output_frame, from_=0, to=255, orient=tk.HORIZONTAL, showvalue=False, troughcolor="#aa7777", length=200, command=update_output_sample)
red_scale_2.set(255)
red_scale_2.pack()
green_scale_2 = tk.Scale(output_frame, from_=0, to=255, orient=tk.HORIZONTAL, showvalue=False, troughcolor="#77aa77", length=200, command=update_output_sample)
green_scale_2.set(255)
green_scale_2.pack()
blue_scale_2 = tk.Scale(output_frame, from_=0, to=255, orient=tk.HORIZONTAL, showvalue=False, troughcolor="#7777aa", length=200, command=update_output_sample)
blue_scale_2.set(255)
blue_scale_2.pack()
output_sample.pack(pady=20)

threshold_frame = tk.Frame(root, padx=10, pady=10)
threshold_frame.place(x=0, y=420)
text_label_3 = tk.Label(threshold_frame, text="Color threshold:", font=("Arial", 16, "bold"), fg="#dddddd", bd=2, height=2, width=25)
text_label_3.pack()
red_scale_3 = tk.Scale(threshold_frame, from_=0, to=255, orient=tk.HORIZONTAL, showvalue=False, troughcolor="#aa7777", length=200)
red_scale_3.pack()
green_scale_3 = tk.Scale(threshold_frame, from_=0, to=255, orient=tk.HORIZONTAL, showvalue=False, troughcolor="#77aa77", length=200)
green_scale_3.pack()
blue_scale_3 = tk.Scale(threshold_frame, from_=0, to=255, orient=tk.HORIZONTAL, showvalue=False, troughcolor="#7777aa", length=200)
blue_scale_3.pack()

buttons_frame = tk.Frame(root, padx=10, pady=10)
buttons_frame.place(x=300, y=480)
open_button = tk.Button(buttons_frame, text="Select file", command=open_file)
open_button.pack(side=tk.LEFT)
preview_button = tk.Button(buttons_frame, text="Preview changes", command=preview)
preview_button.pack(side=tk.LEFT)
finalize_button = tk.Button(buttons_frame, text="Overwrite file", command=save_file)
finalize_button.pack(side=tk.LEFT)

picture_frame = tk.Frame(root, width=440, height=440)
picture_frame.place(x=270, y=20)


C.pack()
tk.mainloop()