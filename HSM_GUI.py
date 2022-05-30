import tkinter
import tkinter.messagebox
from tkinter import CENTER, W, E
from tkinter import filedialog
import customtkinter
import os

from HSM_encrypt_decpryt import call_streaming_encrypt_decrypt
from HSM_Signing import call_streaming_signing
from PIL import Image, ImageTk

PATH = os.path.dirname(os.path.realpath(__file__))
WIDTH = 1600
HEIGHT = 1200


def signing_file_window():
    def browse_files():
        file_name = filedialog.askopenfilename(initialdir="/",
                                               title="Select a File")
        file_path_text.set(file_name)

    def sign():
        endpoint = "https://eu.smartkey.io/"
        api_key = api_key_text.get()
        signing_key = key_name_text.get()
        file = file_path_text.get()
        if operation_selection.get() == 1:
            signing_algorithm = 'SHA2-256'
        if operation_selection.get() == 2:
            signing_algorithm = 'SHA3-256'
        digest = False
        call_streaming_signing(endpoint, api_key, file, out_data='file_signed.txt', key_name=signing_key,
                               operation=signing_algorithm,digest=digest)

    customtkinter.set_appearance_mode("dark")  # Modes: "System" (standard), "Dark", "Light"
    customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

    signing_window = customtkinter.CTk()  # create CTk window like you do with the Tk window
    signing_window.geometry("{}x{}".format(WIDTH, HEIGHT))
    signing_window.title("Faurecia HSM Tool")

    signing_window.grid_columnconfigure(1, weight=1)
    signing_window.grid_rowconfigure(0, weight=1)

    y_padding = 15

    api_key_text = tkinter.StringVar()
    key_name_text = tkinter.StringVar()
    file_path_text = tkinter.StringVar()
    operation_selection = tkinter.IntVar()

    image = Image.open(PATH + "/HSMsymmetrickey_0.jpg").resize((WIDTH, HEIGHT))
    signing_window.bg_image = ImageTk.PhotoImage(image)

    signing_window.image_label = tkinter.Label(master=signing_window, image=signing_window.bg_image)
    signing_window.image_label.place(relx=0.5, rely=0.5, anchor=CENTER)

    frame_1 = customtkinter.CTkFrame(master=signing_window, corner_radius=15)

    frame_2 = customtkinter.CTkFrame(master=signing_window, corner_radius=15)

    frame_1.grid(row=0, column=1, padx=10, pady=y_padding)

    frame_2.grid(row=1, column=1, padx=10, pady=y_padding)

    img = ImageTk.PhotoImage(Image.open("logo.png").resize((450, 100)))
    image_2 = customtkinter.CTkLabel(master=frame_2, image=img, bg_color="white")
    image_2.grid(row=1, column=1)

    label_1 = customtkinter.CTkLabel(master=frame_1, text="Signing a file")
    label_1.grid(row=1, column=2, pady=10, padx=20, sticky="")
    label_1.configure(font=("Roboto", 20, "bold"))

    api_key_entry = customtkinter.CTkEntry(master=frame_1, textvariable=api_key_text,
                                           width=400,
                                           placeholder_text="Enter API key")

    api_key_entry.grid(row=2, column=2, columnspan=4, pady=10, padx=20, sticky="W")

    key_name_entry = customtkinter.CTkEntry(master=frame_1, textvariable=key_name_text,
                                            width=400,
                                            placeholder_text="Enter key name")
    key_name_entry.grid(row=3, column=2, columnspan=2, pady=10, padx=20, sticky="W")

    radio_button_1 = customtkinter.CTkRadioButton(master=frame_1,
                                                  variable=operation_selection, value=1,
                                                  text="SHA2-256", text_font=("Roboto Small", -12))
    radio_button_1.grid(row=4, column=2, pady=10, padx=20, sticky="W")

    radio_button_2 = customtkinter.CTkRadioButton(master=frame_1,
                                                  variable=operation_selection, value=2,
                                                  text="SHA3-256", text_font=("Roboto Small", -12))
    radio_button_2.grid(row=4, column=2, pady=10, padx=150, sticky="W")

    file_path_entry = customtkinter.CTkEntry(master=frame_1, textvariable=file_path_text,
                                             width=250)
    file_path_entry.grid(row=5, column=2, columnspan=2, pady=10, padx=20, sticky="W")

    button_2 = customtkinter.CTkButton(master=frame_1, corner_radius=8,
                                       command=lambda: [browse_files()],
                                       text="Select a file", fg_color=("blue", "green"), height=40,
                                       width=50)
    button_2.grid(row=5, column=2, columnspan=2, pady=10, padx=20, sticky="E")

    button_1 = customtkinter.CTkButton(master=frame_1, corner_radius=8,
                                       command=lambda: [signing_window.destroy(), sign(), operation_window()],
                                       text="Sign", fg_color=("blue", "green"), height=40,
                                       width=400)
    button_1.grid(row=6, column=2, pady=10, padx=20, sticky="W")

    signing_window.mainloop()


def signing_digest_window():
    def browse_files():
        file_name = filedialog.askopenfilename(initialdir="/",
                                               title="Select a File")
        file_path_text.set(file_name)

    def sign():
        endpoint = "https://eu.smartkey.io/"
        api_key = api_key_text.get()
        signing_key = key_name_text.get()
        file = file_path_text.get()
        if operation_selection.get() == 1:
            signing_algorithm = 'SHA2-256'
        if operation_selection.get() == 2:
            signing_algorithm = 'SHA3-256'
        digest = True
        call_streaming_signing(endpoint, api_key, file, out_data='file_signed.txt', key_name=signing_key,
                               operation=signing_algorithm, digest=digest)

    customtkinter.set_appearance_mode("dark")  # Modes: "System" (standard), "Dark", "Light"
    customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

    signing_window = customtkinter.CTk()  # create CTk window like you do with the Tk window
    signing_window.geometry("{}x{}".format(WIDTH, HEIGHT))
    signing_window.title("Faurecia HSM Tool")

    signing_window.grid_columnconfigure(1, weight=1)
    signing_window.grid_rowconfigure(0, weight=1)

    y_padding = 15

    api_key_text = tkinter.StringVar()
    key_name_text = tkinter.StringVar()
    file_path_text = tkinter.StringVar()
    operation_selection = tkinter.IntVar()

    image = Image.open(PATH + "/HSMsymmetrickey_0.jpg").resize((WIDTH, HEIGHT))
    signing_window.bg_image = ImageTk.PhotoImage(image)

    signing_window.image_label = tkinter.Label(master=signing_window, image=signing_window.bg_image)
    signing_window.image_label.place(relx=0.5, rely=0.5, anchor=CENTER)

    frame_1 = customtkinter.CTkFrame(master=signing_window, corner_radius=15)

    frame_2 = customtkinter.CTkFrame(master=signing_window, corner_radius=15)

    frame_1.grid(row=0, column=1, padx=10, pady=y_padding)

    frame_2.grid(row=1, column=1, padx=10, pady=y_padding)

    img = ImageTk.PhotoImage(Image.open("logo.png").resize((450, 100)))
    image_2 = customtkinter.CTkLabel(master=frame_2, image=img, bg_color="white")
    image_2.grid(row=1, column=1)

    label_1 = customtkinter.CTkLabel(master=frame_1, text="Signing a digest")
    label_1.grid(row=1, column=2, pady=10, padx=20, sticky="")
    label_1.configure(font=("Roboto", 20, "bold"))

    api_key_entry = customtkinter.CTkEntry(master=frame_1, textvariable=api_key_text,
                                           width=400,
                                           placeholder_text="Enter API key")

    api_key_entry.grid(row=2, column=2, columnspan=4, pady=10, padx=20, sticky="W")

    key_name_entry = customtkinter.CTkEntry(master=frame_1, textvariable=key_name_text,
                                            width=400,
                                            placeholder_text="Enter key name")
    key_name_entry.grid(row=3, column=2, columnspan=2, pady=10, padx=20, sticky="W")

    radio_button_1 = customtkinter.CTkRadioButton(master=frame_1,
                                                  variable=operation_selection, value=1,
                                                  text="SHA2-256", text_font=("Roboto Small", -12))
    radio_button_1.grid(row=4, column=2, pady=10, padx=20, sticky="W")

    radio_button_2 = customtkinter.CTkRadioButton(master=frame_1,
                                                  variable=operation_selection, value=2,
                                                  text="SHA3-256", text_font=("Roboto Small", -12))
    radio_button_2.grid(row=4, column=2, pady=10, padx=150, sticky="W")

    file_path_entry = customtkinter.CTkEntry(master=frame_1, textvariable=file_path_text,
                                             width=250)
    file_path_entry.grid(row=5, column=2, columnspan=2, pady=10, padx=20, sticky="W")

    button_2 = customtkinter.CTkButton(master=frame_1, corner_radius=8,
                                       command=lambda: [browse_files()],
                                       text="Select a digest", fg_color=("blue", "green"), height=40,
                                       width=50)
    button_2.grid(row=5, column=2, columnspan=2, pady=10, padx=20, sticky="E")

    button_1 = customtkinter.CTkButton(master=frame_1, corner_radius=8,
                                       command=lambda: [signing_window.destroy(), sign(), operation_window()],
                                       text="Sign", fg_color=("blue", "green"), height=40,
                                       width=400)
    button_1.grid(row=6, column=2, pady=10, padx=20, sticky="W")

    signing_window.mainloop()


def encrypt_file_window():
    def browse_files():
        file_name = filedialog.askopenfilename(initialdir="/",
                                               title="Select a File")
        file_path_text.set(file_name)

    def encrypt():
        endpoint = "https://eu.smartkey.io/"
        api_key = api_key_text.get()
        encrypt_key = key_name_text.get()
        file = file_path_text.get()

        file_ending = file.split(".")
        file_ending = file_ending[-1]

        call_streaming_encrypt_decrypt(endpoint, api_key, file, out_data='{}_encrypted.{}'.format(file, file_ending),
                                       key_name=encrypt_key, operation='encrypt')

    customtkinter.set_appearance_mode("dark")  # Modes: "System" (standard), "Dark", "Light"
    customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

    signing_window = customtkinter.CTk()  # create CTk window like you do with the Tk window
    signing_window.geometry("{}x{}".format(WIDTH, HEIGHT))
    signing_window.title("Faurecia HSM Tool")

    signing_window.grid_columnconfigure(1, weight=1)
    signing_window.grid_rowconfigure(0, weight=1)

    y_padding = 15

    api_key_text = tkinter.StringVar()
    key_name_text = tkinter.StringVar()
    file_path_text = tkinter.StringVar()

    image = Image.open(PATH + "/HSMsymmetrickey_0.jpg").resize((WIDTH, HEIGHT))
    signing_window.bg_image = ImageTk.PhotoImage(image)

    signing_window.image_label = tkinter.Label(master=signing_window, image=signing_window.bg_image)
    signing_window.image_label.place(relx=0.5, rely=0.5, anchor=CENTER)

    frame_1 = customtkinter.CTkFrame(master=signing_window, corner_radius=15)

    frame_2 = customtkinter.CTkFrame(master=signing_window, corner_radius=15)

    frame_1.grid(row=0, column=1, padx=10, pady=y_padding)

    frame_2.grid(row=1, column=1, padx=10, pady=y_padding)

    img = ImageTk.PhotoImage(Image.open("logo.png").resize((450, 100)))
    image_2 = customtkinter.CTkLabel(master=frame_2, image=img, bg_color="white")
    image_2.grid(row=1, column=1)

    label_1 = customtkinter.CTkLabel(master=frame_1, text="Encrypt a file")
    label_1.grid(row=1, column=2, pady=10, padx=20, sticky="")
    label_1.configure(font=("Roboto", 20, "bold"))

    api_key_entry = customtkinter.CTkEntry(master=frame_1, textvariable=api_key_text,
                                           width=400,
                                           placeholder_text="Enter API key")

    api_key_entry.grid(row=2, column=2, columnspan=4, pady=10, padx=20, sticky="W")

    key_name_entry = customtkinter.CTkEntry(master=frame_1, textvariable=key_name_text,
                                            width=400,
                                            placeholder_text="Enter key name")
    key_name_entry.grid(row=3, column=2, columnspan=2, pady=10, padx=20, sticky="W")

    file_path_entry = customtkinter.CTkEntry(master=frame_1, textvariable=file_path_text,
                                             width=250)
    file_path_entry.grid(row=4, column=2, columnspan=2, pady=10, padx=20, sticky="W")

    button_2 = customtkinter.CTkButton(master=frame_1, corner_radius=8,
                                       command=lambda: [browse_files()],
                                       text="Select a file", fg_color=("blue", "green"), height=40,
                                       width=50)
    button_2.grid(row=4, column=2, columnspan=2, pady=10, padx=20, sticky="E")

    button_1 = customtkinter.CTkButton(master=frame_1, corner_radius=8,
                                       command=lambda: [signing_window.destroy(), encrypt(),operation_window()],
                                       text="Encrypt", fg_color=("blue", "green"), height=40,
                                       width=400)
    button_1.grid(row=5, column=2, pady=10, padx=20, sticky="W")

    signing_window.mainloop()


def decrypt_file_window():
    def browse_files():
        file_name = filedialog.askopenfilename(initialdir="/",
                                               title="Select a File")
        file_path_text.set(file_name)

    def decrypt():
        endpoint = "https://eu.smartkey.io/"
        api_key = api_key_text.get()
        decrypt_key = key_name_text.get()
        file = file_path_text.get()
        iv = iv_text.get()

        file_path = file.partition('_encrypted')[0]
        print(file_path)
        file_ending = file.split(".")
        file_ending = file_ending[-1]

        call_streaming_encrypt_decrypt(endpoint, api_key, file,
                                       out_data='{}_decrypted.{}'.format(file_path, file_ending),
                                       key_name=decrypt_key, operation='decrypt', iv=iv)

    customtkinter.set_appearance_mode("dark")  # Modes: "System" (standard), "Dark", "Light"
    customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

    signing_window = customtkinter.CTk()  # create CTk window like you do with the Tk window
    signing_window.geometry("{}x{}".format(WIDTH, HEIGHT))
    signing_window.title("Faurecia HSM Tool")

    signing_window.grid_columnconfigure(1, weight=1)
    signing_window.grid_rowconfigure(0, weight=1)

    y_padding = 15

    api_key_text = tkinter.StringVar()
    key_name_text = tkinter.StringVar()
    file_path_text = tkinter.StringVar()
    iv_text = tkinter.StringVar()

    image = Image.open(PATH + "/HSMsymmetrickey_0.jpg").resize((WIDTH, HEIGHT))
    signing_window.bg_image = ImageTk.PhotoImage(image)

    signing_window.image_label = tkinter.Label(master=signing_window, image=signing_window.bg_image)
    signing_window.image_label.place(relx=0.5, rely=0.5, anchor=CENTER)

    frame_1 = customtkinter.CTkFrame(master=signing_window, corner_radius=15)

    frame_2 = customtkinter.CTkFrame(master=signing_window, corner_radius=15)

    frame_1.grid(row=0, column=1, padx=10, pady=y_padding)

    frame_2.grid(row=1, column=1, padx=10, pady=y_padding)

    img = ImageTk.PhotoImage(Image.open("logo.png").resize((450, 100)))
    image_2 = customtkinter.CTkLabel(master=frame_2, image=img, bg_color="white")
    image_2.grid(row=1, column=1)

    label_1 = customtkinter.CTkLabel(master=frame_1, text="Decrypt a cipher")
    label_1.grid(row=1, column=2, pady=10, padx=20, sticky="")
    label_1.configure(font=("Roboto", 20, "bold"))

    api_key_entry = customtkinter.CTkEntry(master=frame_1, textvariable=api_key_text,
                                           width=400,
                                           placeholder_text="Enter API key")

    api_key_entry.grid(row=2, column=2, columnspan=4, pady=10, padx=20, sticky="W")

    key_name_entry = customtkinter.CTkEntry(master=frame_1, textvariable=key_name_text,
                                            width=400,
                                            placeholder_text="Enter key name")
    key_name_entry.grid(row=3, column=2, columnspan=2, pady=10, padx=20, sticky="W")

    iv_entry = customtkinter.CTkEntry(master=frame_1, textvariable=iv_text,
                                      width=400,
                                      placeholder_text="Enter initialize vector")
    iv_entry.grid(row=4, column=2, columnspan=2, pady=10, padx=20, sticky="W")

    file_path_entry = customtkinter.CTkEntry(master=frame_1, textvariable=file_path_text,
                                             width=250)
    file_path_entry.grid(row=5, column=2, columnspan=2, pady=10, padx=20, sticky="W")

    button_2 = customtkinter.CTkButton(master=frame_1, corner_radius=8,
                                       command=lambda: [browse_files()],
                                       text="Select a cipher", fg_color=("blue", "green"), height=40,
                                       width=50)
    button_2.grid(row=5, column=2, columnspan=2, pady=10, padx=20, sticky="E")

    button_1 = customtkinter.CTkButton(master=frame_1, corner_radius=8,
                                       command=lambda: [signing_window.destroy(), decrypt(), operation_window()],
                                       text="Decrypt", fg_color=("blue", "green"), height=40,
                                       width=400)
    button_1.grid(row=6, column=2, pady=10, padx=20, sticky="W")

    signing_window.mainloop()


def button_function(operation_selection):
    print("operation selected {}".format(operation_selection.get()))
    if operation_selection.get() == 1:
        print("Start signing file")
        signing_file_window()
    if operation_selection.get() == 2:
        print("Start signing digest")
        signing_digest_window()
    if operation_selection.get() == 3:
        print("Start encryption")
        encrypt_file_window()
    if operation_selection.get() == 4:
        print("Start decryption")
        decrypt_file_window()


def operation_window():
    customtkinter.set_appearance_mode("dark")  # Modes: "System" (standard), "Dark", "Light"
    customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

    app = customtkinter.CTk()  # create CTk window like you do with the Tk window
    app.geometry("{}x{}".format(WIDTH, HEIGHT))
    app.title("Faurecia HSM Tool")

    app.grid_columnconfigure(1, weight=1)
    app.grid_rowconfigure(0, weight=1)

    y_padding = 15

    image = Image.open(PATH + "/HSMsymmetrickey_0.jpg").resize((WIDTH, HEIGHT))
    app.bg_image = ImageTk.PhotoImage(image)

    app.image_label = tkinter.Label(master=app, image=app.bg_image)
    app.image_label.place(relx=0.5, rely=0.5, anchor=CENTER)

    frame_1 = customtkinter.CTkFrame(master=app, corner_radius=15)
    frame_2 = customtkinter.CTkFrame(master=app, corner_radius=15)
    frame_1.grid(row=0, column=1, padx=(100, 100))
    frame_2.grid(row=1, column=1, padx=10, pady=y_padding)
    img = ImageTk.PhotoImage(Image.open("logo.png").resize((450, 150)))
    image_2 = customtkinter.CTkLabel(master=frame_2, image=img, bg_color="white")
    image_2.grid(row=1, column=1)
    label_1 = customtkinter.CTkLabel(master=frame_1, justify=tkinter.LEFT,
                                     text="Choose cryptographic operation")
    label_1.pack(pady=y_padding, padx=10)
    label_1.configure(font=("Roboto", 20, "bold"))

    operation_selection = tkinter.IntVar(value=1)

    radio_button_1 = customtkinter.CTkRadioButton(master=frame_1,
                                                  variable=operation_selection, value=1, text="Signing a file",
                                                  text_font=("Roboto Small", -15))

    radio_button_1.pack(pady=y_padding, padx=50, anchor=W)

    radio_button_2 = customtkinter.CTkRadioButton(master=frame_1, variable=operation_selection,
                                                  value=2, text="Signing a digest",
                                                  text_font=("Roboto Small", -15))
    radio_button_2.pack(pady=y_padding, padx=50, anchor=W)

    radio_button_3 = customtkinter.CTkRadioButton(master=frame_1, variable=operation_selection,
                                                  value=3, text="Encryption",
                                                  text_font=("Roboto Small", -15))
    radio_button_3.pack(pady=y_padding, padx=50, anchor=W)

    radio_button_4 = customtkinter.CTkRadioButton(master=frame_1, variable=operation_selection,
                                                  value=4, text="Decryption",
                                                  text_font=("Roboto Small", -15))
    radio_button_4.pack(pady=y_padding, padx=50, anchor=W)

    button_1 = customtkinter.CTkButton(master=frame_1, corner_radius=8,
                                       command=lambda: [app.destroy(),
                                                        button_function(operation_selection)],
                                       text="Submit", fg_color=("blue", "green"), height=40,
                                       width=400)
    button_1.pack(pady=50, padx=10)

    app.mainloop()


def main():
    operation_window()


if __name__ == "__main__":
    main()
import os
import tkinter as tk
from tkinter import *
from HSM_encrypt_decpryt import call_streaming_encrypt_decrypt
from HSM_Signing import call_streaming_signing
from tkinter import filedialog
from Terminal import MyWindow


# TODO: open terminal window
# TODO: API & key error message
# TODO: correct sha3 encryption with Dipak
# TODO: add version

def encryption_decryption_window():
    def encrypt():
        endpoint = "https://eu.smartkey.io"
        key = api_key_text.get("1.0", "end-1c")
        file = encrypt_file_path.cget("text")
        aes = encrypt_key_text.get("1.0", "end-1c")

        file_ending = file.split(".")
        file_ending = file_ending[-1]
        call_streaming_encrypt_decrypt(endpoint, key, file, out_data='{}_encrypted.{}'.format(file, file_ending),
                                       key_name=aes, operation='encrypt')

    def decrypt():
        endpoint = "https://eu.smartkey.io/"
        key = api_key_text.get("1.0", "end-1c")
        file = encrypt_file_path.cget("text")
        aes = encrypt_key_text.get("1.0", "end-1c")
        iv = iv_text.get("1.0", "end-1c")

        file_path = file.partition('_encrypted')[0]
        print(file_path)

        file_ending = file.split(".")
        file_ending = file_ending[-1]

        call_streaming_encrypt_decrypt(endpoint, key, file, out_data='{}_decrypted.{}'.format(file_path, file_ending),
                                       key_name=aes, operation='decrypt', iv=iv)

    encrypt_decrypt_window = Tk()
    encrypt_decrypt_window.geometry('{}x{}'.format(900, 400))
    encrypt_decrypt_window.title("HSM_GUI")
    top_frame = Frame(encrypt_decrypt_window, bg='cyan', width=900, height=400)
    # bottom_frame = Frame(encrypt_decrypt_window, bg='white', width=800, height=200)
    encrypt_decrypt_window.grid_rowconfigure(1, weight=1)
    encrypt_decrypt_window.grid_columnconfigure(0, weight=1)
    top_frame.grid(row=0, column=0)
    # bottom_frame.grid(row=1, column=0)
    # wid = bottom_frame.winfo_id()
    # os.system('xterm -into %d -geometry 450x200 -sb &' % wid)

    encrypt_key = Label(top_frame, text='Enter Key name')

    encrypt_key_text = Text(top_frame, height=2,
                            width=40,
                            bg="light yellow")

    api_key = Label(top_frame, text='Enter API Key')

    api_key_text = Text(top_frame, height=2,
                        width=40,
                        bg="light yellow")

    encrypt_file = Label(top_frame, text='Enter file name')

    encrypt_file_path = Label(top_frame, height=2,
                              width=40,
                              bg="light yellow")

    def browse_files():
        filename = filedialog.askopenfilename(initialdir="/",
                                              title="Select a File")

        encrypt_file_path.configure(text="" + filename)

    button_explore = Button(top_frame,
                            text="Browse Files",
                            command=browse_files)

    iv_label = Label(top_frame, text='Enter iv for decryption')
    iv_text = Text(top_frame, height=2,
                   width=40,
                   bg="light yellow")

    encrypt_bt = Button(top_frame, height=2,
                        width=40,
                        text="encrypt",
                        command=lambda: [encrypt(), encrypt_decrypt_window.destroy()])
    decrypt_bt = Button(top_frame, height=2,
                        width=40,
                        text="decrypt",
                        command=lambda: [decrypt(), encrypt_decrypt_window.destroy()])

    api_key.grid(column=0, row=1)
    api_key_text.grid(column=1, row=1)

    encrypt_key.grid(column=0, row=2)
    encrypt_key_text.grid(column=1, row=2)

    encrypt_file.grid(column=0, row=4)
    encrypt_file_path.grid(column=1, row=4)

    button_explore.grid(column=2, row=4)

    iv_label.grid(column=0, row=5)
    iv_text.grid(column=1, row=5)

    encrypt_bt.grid(column=0, row=6)
    decrypt_bt.grid(column=1, row=6)

    mainloop()


def signing(sign_key_text, api_key_text, sign_file_path, signing_algorithm):
    endpoint = "https://eu.smartkey.io/"
    key = api_key_text.get("1.0", "end-1c")
    file = sign_file_path.cget("text")
    signing_key = sign_key_text.get("1.0", "end-1c")
    call_streaming_signing(endpoint, key, file, out_data='file_signed.txt', key_name=signing_key,
                           operation=signing_algorithm.get())


def sign_window():
    signing_window = tk.Tk()
    signing_window.geometry("800x400")
    signing_window.title("HSM Tool")

    sign_key = Label(signing_window, text='Enter Key name')

    sign_key_text = Text(signing_window, height=2,
                         width=30,
                         bg="light yellow")

    api_key = Label(signing_window, text='Enter API Key')

    api_key_text = Text(signing_window, height=2,
                        width=30,
                        bg="light yellow")

    sign_file = Label(signing_window, text='Select a file ')

    sign_file_path = Label(signing_window, height=2,
                           width=30,
                           bg="light yellow")

    def browse_files():
        filename = filedialog.askopenfilename(initialdir="/",
                                              title="Select a File")

        sign_file_path.configure(text="" + filename)

    button_explore = Button(signing_window,
                            text="Browse Files",
                            command=browse_files)

    def print_sign(choice):
        operation = signing_algorithm.get()

    options_list = ["SHA2-256", "SHA3-256"]
    signing_algorithm = StringVar()
    signing_algorithm.set("Select hash function")
    multiple_choice = tk.OptionMenu(signing_window, signing_algorithm, *options_list, command=print_sign)

    api_key.grid(column=1, row=1)

    api_key_text.grid(column=2, row=1)

    sign_key.grid(column=1, row=2)

    sign_key_text.grid(column=2, row=2)

    sign_file.grid(column=1, row=4)

    sign_file_path.grid(column=2, row=4)

    multiple_choice.grid(column=1, row=5)

    button_explore.grid(column=3, row=4)

    sign_bt = Button(signing_window, height=2,
                     width=30,
                     text="sign",
                     command=lambda: [signing(sign_key_text, api_key_text, sign_file_path, signing_algorithm),
                                      signing_window.destroy()])

    sign_bt.grid(column=2, row=6, columnspan=3, sticky=EW)

    mainloop()


operation_window = Tk()
operation_window.geometry('400x150')
operation_window.title('Choose operation')

frame = Frame(operation_window)
frame.pack()

operation_selection = IntVar()
radio_signing_btn = Radiobutton(frame, text="Signing", variable=operation_selection,
                                value=1)
radio_signing_btn.pack(padx=10, pady=10)
radio_encryption_btn = Radiobutton(frame, text="Encryption and Decryption ", variable=operation_selection,
                                   value=2)
radio_encryption_btn.pack(padx=10, pady=10)


def check_value():
    if operation_selection.get() == 1:
        sign_window()
    if operation_selection.get() == 2:
        encryption_decryption_window()


Btn = Button(frame, text="Submit", command=lambda: [operation_window.destroy(), check_value()])

Btn.pack()
operation_window.mainloop()
