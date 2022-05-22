import tkinter
from tkinter import *
from tkinter import messagebox
from HSM_encrypt_decpryt import call_streaming_encrypt_decrypt

from HSM_Signing import call_streaming_signing


def second_window():
    encrypt_decrypt_window = Tk()
    encrypt_decrypt_window.geometry("300x300")
    encrypt_decrypt_window.title("HSM_GUI")

    def encrypt():
        endpoint = "https://eu.smartkey.io"
        key = api_key_text.get("1.0", "end-1c")
        file = encrypt_file_path.get("1.0", "end-1c")
        aes = encrypt_key_text.get("1.0", "end-1c")

        call_streaming_encrypt_decrypt(endpoint, key, file, out_data='file_encrypted', key_name=aes,
                                       operation='encrypt')

    def decrypt():
        endpoint = "https://eu.smartkey.io/"
        key = api_key_text.get("1.0", "end-1c")
        file = encrypt_file_path.get("1.0", "end-1c")
        aes = encrypt_key_text.get("1.0", "end-1c")
        iv = iv_text.get("1.0", "end-1c")

        call_streaming_encrypt_decrypt(endpoint, key, file, out_data='file_encrypted.txt', key_name=aes,
                                       operation='decrypt', iv=iv)

    encrypt_key = Label(encrypt_decrypt_window, text='Enter Key name')

    encrypt_key_text = Text(encrypt_decrypt_window, height=2,
                            width=15,
                            bg="light yellow")

    api_key = Label(encrypt_decrypt_window, text='Enter API Key')

    api_key_text = Text(encrypt_decrypt_window, height=2,
                        width=15,
                        bg="light yellow")

    encrypt_file = Label(encrypt_decrypt_window, text='Enter file name')
    encrypt_file_path = Text(encrypt_decrypt_window, height=2,
                             width=15,
                             bg="light yellow")

    iv_label = Label(encrypt_decrypt_window, text='Enter iv for decryption')
    iv_text = Text(encrypt_decrypt_window, height=2,
                   width=15,
                   bg="light yellow")

    encrypt_bt = Button(encrypt_decrypt_window, height=2,
                        width=20,
                        text="encrypt",
                        command=lambda: [encrypt(), encrypt_decrypt_window.destroy()])
    decrypt_bt = Button(encrypt_decrypt_window, height=2,
                        width=20,
                        text="decrypt",
                        command=lambda: [decrypt(), encrypt_decrypt_window.destroy()])

    api_key.grid(column=1, row=1)
    api_key_text.grid(column=2, row=1)

    encrypt_key.grid(column=1, row=2)
    encrypt_key_text.grid(column=2, row=2)

    encrypt_file.grid(column=1, row=4)
    encrypt_file_path.grid(column=2, row=4)

    iv_label.grid(column=1, row=5)
    iv_text.grid(column=2, row=5)

    encrypt_bt.grid(column=1, row=6)
    decrypt_bt.grid(column=2, row=6)

    mainloop()


def signing(sign_key_text, api_key_text, sign_file_path, signing_algorithm):
    endpoint = "https://eu.smartkey.io/"
    key = api_key_text.get("1.0", "end-1c")
    file = sign_file_path.get("1.0", "end-1c")
    signing_key = sign_key_text.get("1.0", "end-1c")

    call_streaming_signing(endpoint, key, file, out_data='file_signed.txt', key_name=signing_key,
                           operation=signing_algorithm)


def third_window():
    signing_window = tkinter.Tk()
    signing_window.geometry("300x300")
    signing_window.title("HSM_GUI")

    sign_key = Label(signing_window, text='Enter Key name')

    sign_key_text = Text(signing_window, height=2,
                         width=15,
                         bg="light yellow")

    api_key = Label(signing_window, text='Enter API Key')

    api_key_text = Text(signing_window, height=2,
                        width=15,
                        bg="light yellow")

    sign_file = Label(signing_window, text='Enter file name')
    sign_file_path = Text(signing_window, height=2,
                          width=15,
                          bg="light yellow")

    options_list = ["SHA2-128", "SHA2-256", "SHA3-128", "SHA3-256"]
    signing_algorithm = tkinter.StringVar(signing_window)
    signing_algorithm.set("Select an Option")
    multiple_choice = OptionMenu(signing_window, signing_algorithm, *options_list)

    print(signing_algorithm.get())

    sign_bt = Button(signing_window, height=2,
                     width=20,
                     text="sign",
                     command=lambda: [signing(sign_key_text, api_key_text, sign_file_path, signing_algorithm),
                                      signing_window.destroy()])

    api_key.grid(column=1, row=1)
    api_key_text.grid(column=2, row=1)

    sign_key.grid(column=1, row=2)
    sign_key_text.grid(column=2, row=2)

    sign_file.grid(column=1, row=4)
    sign_file_path.grid(column=2, row=4)

    multiple_choice.grid(column=1, row=5)

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
        print("Signing")
        third_window()
    if operation_selection.get() == 2:
        print("encryption/decryption")
        second_window()


Btn = Button(frame, text="Submit", command=lambda: [operation_window.destroy(), check_value()])

Btn.pack()
operation_window.mainloop()
