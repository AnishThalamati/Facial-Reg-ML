import tkinter as tk
from tkinter import *
from tkinter.filedialog import *
from PIL import ImageTk, Image
import cv2
import time


def select_file(window):
    file_name = tk.filedialog.askopenfilename(master=window,
                                        initialdir="/Users/anisht/testimages",
                                          title="Select image to match")
    return file_name


def capture_file(file_path) :
    camera = cv2.VideoCapture(0)
    time.sleep(5)
    return_value, image = camera.read()
    cv2.imwrite(file_path, image)
    camera.release()
