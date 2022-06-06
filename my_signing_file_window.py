import tkinter
import tkinter.messagebox
from tkinter import CENTER, END, Tk, Text
import customtkinter
import os

from tkinter import filedialog
from PIL import Image, ImageTk
from my_operation_window import OperationWindow
from my_HSM_Signing import call_streaming_signing  # previous version HSM_Signing

PATH = os.path.dirname(os.path.realpath(__file__))
WIDTH = 1200
HEIGHT = 800

customtkinter.set_appearance_mode("dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


class SigningFileWindow(customtkinter.CTk):

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

        self.api_key_text = tkinter.StringVar()
        self.key_name_text = tkinter.StringVar()
        self.file_path_text = tkinter.StringVar()
        self.operation_selection = tkinter.IntVar()

        self.frame_1 = customtkinter.CTkFrame(master=self, corner_radius=15)

        self.frame_2 = customtkinter.CTkFrame(master=self, corner_radius=15)
        self.frame_2.grid(row=1, column=1, padx=10, pady=y_padding)

        self.img = ImageTk.PhotoImage(Image.open("logo.png").resize((450, 100)))
        self.image_2 = customtkinter.CTkLabel(self.frame_2, image=self.img, bg_color="white")
        self.image_2.grid(row=1, column=1)

        self.frame_1.grid(row=0, column=1, padx=10, pady=y_padding)

        self.label_1 = customtkinter.CTkLabel(master=self.frame_1, text="Signing file window")
        self.label_1.grid(row=1, column=2, pady=10, padx=0, sticky="W")
        self.label_1.configure(font=("Roboto", 20, "bold"))

        def browse_files():
            file_name = filedialog.askopenfilename(initialdir="/",
                                                   title="Select a File")
            self.file_path_text.set(file_name)

        def sign():
            endpoint = "https://eu.smartkey.io/"
            api_key = self.api_key_text.get()
            signing_key = self.key_name_text.get()
            file = self.file_path_text.get()
            if self.operation_selection.get() == 1:
                signing_algorithm = 'SHA2-256'
            if self.operation_selection.get() == 2:
                signing_algorithm = 'SHA3-256'
            digest = False
            call_streaming_signing(endpoint, api_key, file, out_data='file_signed.txt', key_name=signing_key,
                                   operation=signing_algorithm, digest=digest)

        self.api_key_entry = customtkinter.CTkEntry(master=self.frame_1, textvariable=self.api_key_text,
                                                    width=400,
                                                    placeholder_text="Enter API key")

        self.api_key_entry.grid(row=2, column=2, columnspan=4, pady=10, padx=20, sticky="W")

        self.key_name_entry = customtkinter.CTkEntry(master=self.frame_1, textvariable=self.key_name_text,
                                                     width=400,
                                                     placeholder_text="Enter key name")
        self.key_name_entry.grid(row=3, column=2, columnspan=2, pady=10, padx=20, sticky="W")

        self.radio_button_1 = customtkinter.CTkRadioButton(master=self.frame_1,
                                                           variable=self.operation_selection, value=1,
                                                           text="SHA2-256", text_font=("Roboto Small", -12))
        self.radio_button_1.grid(row=4, column=2, pady=10, padx=20, sticky="W")

        self.radio_button_2 = customtkinter.CTkRadioButton(master=self.frame_1,
                                                           variable=self.operation_selection, value=2,
                                                           text="SHA3-256", text_font=("Roboto Small", -12))
        self.radio_button_2.grid(row=4, column=2, pady=10, padx=150, sticky="W")

        self.file_path_entry = customtkinter.CTkEntry(master=self.frame_1, textvariable=self.file_path_text,
                                                      width=250)
        self.file_path_entry.grid(row=5, column=2, columnspan=2, pady=10, padx=20, sticky="W")

        self.button_2 = customtkinter.CTkButton(master=self.frame_1, corner_radius=8,
                                                command=lambda: [browse_files()],
                                                text="Select a file", fg_color=("blue", "green"), height=40,
                                                width=50)
        self.button_2.grid(row=5, column=2, columnspan=2, pady=10, padx=20, sticky="E")

        self.button_1 = customtkinter.CTkButton(master=self.frame_1, corner_radius=8,
                                                command=lambda: [self.destroy(), sign()],
                                                text="Sign", fg_color=("blue", "green"), height=40,
                                                width=400)
        self.button_1.grid(row=6, column=2, pady=10, padx=20, sticky="W")

    def on_closing(self):
        self.destroy()


def open_operation_window():
    operation_window = OperationWindow()
    operation_window.mainloop()


if __name__ == "__main__":
    signing_file_window = SigningFileWindow()
    signing_file_window.mainloop()
