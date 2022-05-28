import os
import tkinter as tk
from tkinter import *
from HSM_encrypt_decpryt import call_streaming_encrypt_decrypt
from HSM_Signing import call_streaming_signing
from tkinter import filedialog


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
    encrypt_decrypt_window.geometry('{}x{}'.format(800, 400))
    encrypt_decrypt_window.title("HSM_GUI")
    top_frame = Frame(encrypt_decrypt_window, bg='cyan', width=800, height=200)
    bottom_frame = Frame(encrypt_decrypt_window, bg='black', width=800, height=200)

    encrypt_decrypt_window.grid_rowconfigure(1, weight=1)
    encrypt_decrypt_window.grid_columnconfigure(0, weight=1)

    top_frame.grid(row=0, column=0)
    bottom_frame.grid(row=1, column=0)
    wid = bottom_frame.winfo_id()
    os.system('xterm -into %d -geometry 40x20 -sb &' % wid)

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
