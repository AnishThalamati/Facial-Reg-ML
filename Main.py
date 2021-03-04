from tkinter import *
import os
import tkinter as tk
from tkinter import *
from tkinter import simpledialog
import boto3
from functools import partial
import ttkthemes
import ttkwidgets
import boto3
from ImageMatcher.Imageutils import *
from ImageMatcher.awsutils import *
from ImageMatcher.awsImageMatcher import *
import calendar
import time

from tkinter import messagebox

# Designing window for registration

def register():
    global register_screen
    register_screen = Toplevel(main_screen)
    register_screen.title("Register")
    register_screen.geometry("512x512")

    global username
    global password
    global username_entry
    global password_entry
    username = StringVar()
    password = StringVar()

    Label(register_screen, text="Please enter details below", bg="blue").pack()
    Label(register_screen, text="").pack()
    username_lable = Label(register_screen, text="Username * ")
    username_lable.pack()
    username_entry = Entry(register_screen, textvariable=username)
    username_entry.pack()
    password_lable = Label(register_screen, text="Password * ")
    password_lable.pack()
    password_entry = Entry(register_screen, textvariable=password, show='*')
    password_entry.pack()
    Label(register_screen, text="").pack()
    Button(register_screen, text="Register", width=10, height=2, bg="Gray", command=register_user).pack()


# Designing window for login

def login():
    global login_screen
    login_screen = Toplevel(main_screen)
    login_screen.title("Login")
    login_screen.geometry("512x512")
    Label(login_screen, text="Please enter details below to login").pack()
    Label(login_screen, text="").pack()

    global username_verify
    global password_verify

    username_verify = StringVar()
    password_verify = StringVar()

    global username_login_entry
    global password_login_entry

    Label(login_screen, text="Username * ").pack()
    username_login_entry = Entry(login_screen, textvariable=username_verify)
    username_login_entry.pack()
    Label(login_screen, text="").pack()
    Label(login_screen, text="Password * ").pack()
    password_login_entry = Entry(login_screen, textvariable=password_verify, show='*')
    password_login_entry.pack()
    Label(login_screen, text="").pack()
    Button(login_screen, text="Login", width=10, height=1, command=login_verify).pack()


# Implementing event on register button

def register_user():
    username_info = username.get()
    password_info = password.get()

    file = open(username_info, "w")
    file.write(username_info + "\n")
    file.write(password_info)
    file.close()

    username_entry.delete(0, END)
    password_entry.delete(0, END)

    Label(register_screen, text="Registration Success", fg="green", font=("Times", 11)).pack()


# Implementing event on login button

def login_verify():
    username1 = username_verify.get()
    password1 = password_verify.get()
    username_login_entry.delete(0, END)
    password_login_entry.delete(0, END)

    list_of_files = os.listdir()
    if username1 in list_of_files:
        file1 = open(username1, "r")
        verify = file1.read().splitlines()
        if password1 in verify:
            login_sucess()

        else:
            password_not_recognised()

    else:
        user_not_found()


# Designing popup for login success

def login_sucess():
    global login_success_screen
    login_success_screen = Toplevel(login_screen)
    login_success_screen.title("Success")
    login_success_screen.geometry("512x512")
    Label(login_success_screen, text="Login Success").pack()
    Button(login_success_screen, text="OK", command=delete_login_success).pack()






# Designing popup for login invalid password

def password_not_recognised():
    global password_not_recog_screen
    password_not_recog_screen = Toplevel(login_screen)
    password_not_recog_screen.title("Success")
    password_not_recog_screen.geometry("512x512")
    Label(password_not_recog_screen, text="Invalid Password ").pack()
    Button(password_not_recog_screen, text="OK", command=delete_password_not_recognised).pack()


# Designing popup for user not found

def user_not_found():
    global user_not_found_screen
    user_not_found_screen = Toplevel(login_screen)
    user_not_found_screen.title("Success")
    user_not_found_screen.geometry("512x512")
    Label(user_not_found_screen, text="User Not Found").pack()
    Button(user_not_found_screen, text="OK", command=delete_user_not_found_screen).pack()


# Deleting popups


def delete_login_success():
    login_success_screen.destroy()
    login_screen.destroy()
    main_screen.destroy()



    def get_thumbnail(path):
        size = 256, 256
        t_img = Image.open(path)
        t_img.thumbnail(size)
        return t_img

    # This creates the main window of an application
    master = Tk()
    LOCAL_NO_MATCH_FILE = "/Users/anisht/testimages/No_Match_2.jpg"
    LOCAL_DEFAULT_SOURCE_FILE = "/Users/anisht/testimages/Source_Image_3.jpg"
    LOCAL_DEFAULT_TARGET_FILE = "/Users/anisht/testimages/Target_Image_3.jpg"

    master.title("Stranger Scan Home page")
    # root.configure(background='grey')
    master.geometry("512x512")

    # Setup image widgets
    imageFrame = Frame(master)
    # Set Default images
    current_image = ImageTk.PhotoImage(get_thumbnail(LOCAL_DEFAULT_SOURCE_FILE))
    matched_image = ImageTk.PhotoImage(get_thumbnail(LOCAL_DEFAULT_TARGET_FILE))

    current_label = tk.Label(imageFrame, image=current_image)
    # The Pack geometry manager packs widgets in rows or columns.
    current_label.pack(side="left", fill="both", expand="yes", ipadx=20, ipady=20)

    matched_label = tk.Label(imageFrame, image=matched_image)
    matched_label.pack(side="left", fill="both", expand="yes", ipadx=20, ipady=20)
    imageFrame.pack()

    new_img = current_image

    def update_image(wdgt, filename):
        # update image widgets
        global new_img
        new_img = ImageTk.PhotoImage(get_thumbnail(filename))
        wdgt.image = new_img
        wdgt.configure(image=new_img)

    def compare_update_image(filename):
        # get current image list from s3
        current_image_list = s3_get_image_list()
        # Upload file to S3
        s3_target_name = os.path.basename(filename)
        print(s3_target_name)
        s3_upload_file_name = s3_upload_file(filename, s3_target_name)
        s3_matched_file = compare_faces(current_image_list, s3_upload_file_name)
        local_matched_file = LOCAL_NO_MATCH_FILE
        if s3_matched_file != "":
            local_matched_file = s3_download_file(s3_matched_file, '/tmp/matched_image.jpg')
        update_image(matched_label, local_matched_file)

    def check_file_match():
        # get file name from user
        filename = select_file(master)
        update_image(current_label, filename)
        compare_update_image(filename)

    def check_camera_match():
        filename = "/tmp/captured_image-" + str(time.time_ns()) + ".jpg"
        print("Captured filename:", filename)
        capture_file(filename)
        update_image(current_label, filename)
        compare_update_image(filename)

    def upload_file():
        filename = select_file(master)
        print("Called Upload file")
        print(filename)
        s3_target_name = os.path.basename(filename)
        name = s3_upload_file(filename, s3_target_name)
        print("Upload to s3:", name)

    actionsFrame = Frame(master)

    match_file_button = tk.Button(master=actionsFrame, text="Match Image File", command=check_file_match)
    match_file_button.pack(fill=X, pady=15, ipady=15)

    match_camera_button = tk.Button(master=actionsFrame, text="Match Camera Image", command=check_camera_match)
    match_camera_button.pack(fill=X, pady=15, ipady=15)
    actionsFrame.pack()

    root.bind()

    # Start the GUI


def delete_password_not_recognised():
    password_not_recog_screen.destroy()


def delete_user_not_found_screen():
    user_not_found_screen.destroy()


# Designing Main(first) window

def main_account_screen():
    global main_screen
    main_screen = Tk()
    main_screen.geometry("512x512")
    main_screen.title("Account Login")
    Label(text="Welcome to  Stranger Scan ", width="300", height="2", font=("Times", 18)).pack()
    Label(text="").pack()
    Button(text="Login", height="5", width="50", command=login).pack()
    Label(text="").pack()
    Button(text="Register", height="5", width="50", command=register).pack()

    main_screen.mainloop()


main_account_screen()
