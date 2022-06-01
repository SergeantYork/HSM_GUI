import tkinter
import tkinter.messagebox
from tkinter import CENTER, W, E
import customtkinter
import os

from PIL import Image, ImageTk
from my_operation_window import OperationWindow

PATH = os.path.dirname(os.path.realpath(__file__))
WIDTH = 1600
HEIGHT = 1200

customtkinter.set_appearance_mode("dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


class ProgressWindow(customtkinter.CTk):

    def __init__(self):
        super().__init__()
        self.title("Faurecia HSM Tool")
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

        self.img = ImageTk.PhotoImage(Image.open("logo.png").resize((450, 100)))
        self.image_2 = customtkinter.CTkLabel(self.frame_2, image=self.img, bg_color="white")
        self.image_2.grid(row=1, column=1)

        self.frame_1.grid(row=0, column=1, padx=10, pady=y_padding)

        self.label_1 = customtkinter.CTkLabel(master=self.frame_1, text="Progress window")
        self.label_1.grid(row=1, column=2, pady=10, padx=0, sticky="W")
        self.label_1.configure(font=("Roboto", 20, "bold"))

        self.terminal_output = customtkinter.CTkLabel(master=self.frame_1,
                                                      text="")
        self.terminal_output.configure(font=("Roboto", 10, "bold"))
        self.terminal_output.grid(row=3, column=2, columnspan=4, pady=10, padx=0, sticky="W")

        self.terminal_output.configure(font=("Roboto", 14, "bold"))

        self.progress_bar = customtkinter.CTkProgressBar(master=self.frame_1, width=1200)
        self.progress_bar.grid(row=2, column=2, columnspan=4, pady=10, padx=20, sticky="W")
        self.progress_bar.set(0)

        self.button_1 = customtkinter.CTkButton(master=self.frame_1, corner_radius=8,
                                                command=lambda: [self.destroy(), open_operation_window()],
                                                text="Main menu", fg_color=("blue", "green"), height=40,
                                                width=500)
        self.button_1.grid(row=4, column=2, pady=10, padx=40, sticky="W")

        self.button_2 = customtkinter.CTkButton(master=self.frame_1, corner_radius=8,
                                                command=lambda: [self.destroy()],
                                                text="End", fg_color=("blue", "green"), height=40,
                                                width=500)
        self.button_2.grid(row=4, column=4, pady=10, padx=0, sticky="E")

    def on_closing(self):
        self.destroy()


def open_operation_window():
    operation_window = OperationWindow()
    operation_window.mainloop()


if __name__ == "__main__":
    progress_window = ProgressWindow()
    progress_window.mainloop()
