# Import necessary libraries
import tkinter as tk
from tkinter import *
import tkinter.messagebox as mbox
from tkinter import ttk, filedialog
from PIL import ImageTk, Image
import cv2
import os
import numpy as np
import time

# Create the main window
window = Tk()
window.geometry("1000x700")
window.title("Image Encryption and Decryption")
window.configure(bg='light green')
time.sleep(1)

# Define global variables
global count, eimg, con, bright, frp, tname, panelA, panelB
count = 0
con = 1
bright = 0
panelA = None
panelB = None
frp = []
tname = []

# Utility functions
def getpath(path):
    """Get the directory path of the selected image."""
    a = path.split(r'/')
    fname = a[-1]
    location = path[:-len(fname)]
    return location

def getfoldername(path):
    """Get the folder name from which the image is selected."""
    a = path.split(r'/')
    return a[-1]

def getfilename(path):
    """Get the file name of the selected image."""
    a = path.split(r'/')
    fname = a[-1]
    return fname.split('.')[0]

def openfilename():
    """Open the file dialog to select an image."""
    return filedialog.askopenfilename(title='Open')

# Image handling functions
def open_img():
    """Open and display the selected image."""
    global x, panelA, panelB, count, eimg, location, filename
    count = 0
    x = openfilename()
    
    # Open the image using PIL
    img = Image.open(x)
    
    # Resize the image to fit within the Tkinter window (e.g., 300x300 pixels)
    img = img.resize((300, 300), Image.ANTIALIAS)
    
    # Convert the image to a Tkinter-compatible PhotoImage object
    eimg = img
    img = ImageTk.PhotoImage(img)
    
    location = getpath(x)
    filename = getfilename(x)
    
    if panelA is None or panelB is None:
        panelA = Label(image=img)
        panelA.image = img
        panelA.pack(side="left", padx=10, pady=10)
        
        panelB = Label(image=img)
        panelB.image = img
        panelB.pack(side="right", padx=10, pady=10)
    else:
        panelA.configure(image=img)
        panelB.configure(image=img)
        panelA.image = img
        panelB.image = img


def en_fun():
    """Encrypt the selected image."""
    global x, encrypted_image, key
    input_image = cv2.imread(x, 0)
    x1, y = input_image.shape
    input_image = input_image.astype(float) / 255.0
    
    mu, sigma = 0, 0.1
    key = np.random.normal(mu, sigma, (x1, y)) + np.finfo(float).eps
    encrypted_image = input_image / key
    
    cv2.imwrite('encrypted_image.jpg', encrypted_image * 255)
    
    imge = Image.open('encrypted_image.jpg')
    imge = ImageTk.PhotoImage(imge)
    panelB.configure(image=imge)
    panelB.image = imge
    
    mbox.showinfo("Encrypt Status", "Image Encrypted successfully.")

def de_fun():
    """Decrypt the encrypted image."""
    global encrypted_image, key
    output_image = encrypted_image * key
    output_image *= 255.0
    
    cv2.imwrite('output_image.jpg', output_image)
    
    imgd = Image.open('output_image.jpg')
    imgd = ImageTk.PhotoImage(imgd)
    panelB.configure(image=imgd)
    panelB.image = imgd
    
    mbox.showinfo("Decrypt Status", "Image decrypted successfully.")

def reset():
    """Reset the image to its original state."""
    global x, eimg, count
    image = cv2.imread(x)[:, :, ::-1]
    count = 6
    image = Image.fromarray(image)
    eimg = image
    image = ImageTk.PhotoImage(image)
    panelB.configure(image=image)
    panelB.image = image
    
    mbox.showinfo("Success", "Image reset to original format!")

def save_img():
    """Save the encrypted/decrypted image."""
    global eimg
    filename = filedialog.asksaveasfile(mode='w', defaultextension=".jpg")
    if not filename:
        return
    eimg.save(filename)
    mbox.showinfo("Success", "Encrypted Image Saved Successfully!")

def exit_win():
    """Exit the application."""
    if mbox.askokcancel("Exit", "Do you want to exit?"):
        window.destroy()

# UI Elements
start1 = tk.Label(text="Image Encryption\nand\nDecryption", font=("Arial", 25), bg='light green', fg="black")
start1.place(x=350, y=10)

start2 = tk.Label(text="Original\nImage", font=("Arial", 25), bg='light green', fg="black")
start2.place(x=100, y=270)

start3 = tk.Label(text="Encrypted\nDecrypted\nImage", font=("Arial", 25), bg='light green', fg="black")
start3.place(x=700, y=230)

chooseb = Button(window, text="Choose", command=open_img, font=("Arial", 15), bg="black", fg="pink", borderwidth=3, relief="raised")
chooseb.place(x=30, y=20)

saveb = Button(window, text="Save", command=save_img, font=("Arial", 15), bg="black", fg="pink", borderwidth=3, relief="raised")
saveb.place(x=170, y=20)

enb = Button(window, text="Encrypt", command=en_fun, font=("Arial", 15), bg="black", fg="pink", borderwidth=3, relief="raised")
enb.place(x=150, y=620)

deb = Button(window, text="Decrypt", command=de_fun, font=("Arial", 15), bg="pink", fg="black", borderwidth=3, relief="raised")
deb.place(x=450, y=620)

resetb = Button(window, text="Reset", command=reset, font=("Arial", 15), bg="black", fg="pink", borderwidth=3, relief="raised")
resetb.place(x=800, y=620)

exitb = Button(window, text="EXIT", command=exit_win, font=("Arial", 15), bg="red", fg="white", borderwidth=3, relief="raised")
exitb.place(x=880, y=20)

# Handle window close event
window.protocol("WM_DELETE_WINDOW", exit_win)

# Run the application
window.mainloop()
