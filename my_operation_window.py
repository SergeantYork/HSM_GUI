import tkinter
import tkinter.messagebox
from tkinter import CENTER
import customtkinter
import os

from PIL import Image, ImageTk
PATH = os.path.dirname(os.path.realpath(__file__))
WIDTH = 1600
HEIGHT = 1200

customtkinter.set_appearance_mode("dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


class OperationWindow(customtkinter.CTk):

    def button_function(self):
        from my_signing_file_window import SigningFileWindow
        from my_signing_digest_window import SigningDigestWindow
        from my_encrypt_file_window import EncryptWindow
        from my_decrypt_file_window import DecryptWindow

        print("operation selected {}".format(self.operation_selection.get()))
        if self.operation_selection.get() == 1:
            SigningFileWindow()
        if self.operation_selection.get() == 2:
            SigningDigestWindow()
        if self.operation_selection.get() == 3:
            EncryptWindow()
        if self.operation_selection.get() == 4:
            DecryptWindow()

    def __init__(self):
        super().__init__()

        self.title("Faurecia HSM Application")
        self.geometry(f"{WIDTH}x{HEIGHT}")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)  # call .on_closing() when app gets closed

        # ============ create two frames ============

        # configure grid layout (2x1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        image = Image.open(PATH + "/HSMsymmetrickey_0.jpg").resize((WIDTH, HEIGHT))
        self.bg_image = ImageTk.PhotoImage(image)
        self.image_label = tkinter.Label(master=self, image=self.bg_image)
        self.image_label.place(relx=0.5, rely=0.5, anchor=CENTER)

        # ============ frames ============
        y_padding = 15

        self.frame_1 = customtkinter.CTkFrame(master=self, corner_radius=15)

        self.frame_2 = customtkinter.CTkFrame(master=self, corner_radius=15)
        self.frame_2.grid(row=1, column=1, padx=10, pady=y_padding)

        img = Image.open(PATH + "/logo.png").resize((450, 100))
        self.logo_image = ImageTk.PhotoImage(img)
        self.image_2 = customtkinter.CTkLabel(self.frame_2, image=self.logo_image, bg_color="white")
        self.image_2.grid(row=1, column=1)

        self.frame_1.grid(row=0, column=1, padx=10, pady=y_padding)

        self.label_1 = customtkinter.CTkLabel(master=self.frame_1, text="Choose cryptographic operation")
        self.label_1.grid(row=1, column=2, pady=10, padx=0, sticky="W")
        self.label_1.configure(font=("Roboto", 20, "bold"))

        self.operation_selection = tkinter.IntVar(value=1)

        self.radio_button_1 = customtkinter.CTkRadioButton(master=self.frame_1,
                                                           variable=self.operation_selection, value=1,
                                                           text="Signing a file",
                                                           text_font=("Roboto Small", -15))
        self.radio_button_1.grid(row=2, column=2, pady=10, padx=20, sticky="W")

        self.radio_button_2 = customtkinter.CTkRadioButton(master=self.frame_1,
                                                           variable=self.operation_selection, value=2,
                                                           text="Signing a digest",
                                                           text_font=("Roboto Small", -15))
        self.radio_button_2.grid(row=3, column=2, pady=10, padx=20, sticky="W")

        self.radio_button_3 = customtkinter.CTkRadioButton(master=self.frame_1,
                                                           variable=self.operation_selection, value=3,
                                                           text="Encryption",
                                                           text_font=("Roboto Small", -15))
        self.radio_button_3.grid(row=4, column=2, pady=10, padx=20, sticky="W")

        self.radio_button_4 = customtkinter.CTkRadioButton(master=self.frame_1,
                                                           variable=self.operation_selection, value=4,
                                                           text="Decryption",
                                                           text_font=("Roboto Small", -15))
        self.radio_button_4.grid(row=5, column=2, pady=10, padx=20, sticky="W")

        self.button_1 = customtkinter.CTkButton(master=self.frame_1, corner_radius=8,
                                                command=lambda: [self.destroy(),
                                                                 self.button_function()],
                                                text="Submit", fg_color=("blue", "green"), height=40,
                                                width=400)
        self.button_1.grid(row=6, column=2, columnspan=2, pady=10, padx=40, sticky="W")

    def on_closing(self):
        self.destroy()


if __name__ == "__main__":
    operation_window = OperationWindow()
    operation_window.mainloop()
