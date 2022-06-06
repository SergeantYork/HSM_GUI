import tkinter
import tkinter.messagebox
from tkinter import CENTER, END, Text
import customtkinter
import os

from PIL import Image, ImageTk
from my_operation_window import OperationWindow

PATH = os.path.dirname(os.path.realpath(__file__))
WIDTH = 1200
HEIGHT = 800

customtkinter.set_appearance_mode("dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


class OpenLogFileWindow(customtkinter.CTk):

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
        self.img = ImageTk.PhotoImage(Image.open("logo.png").resize((450, 100)))
        self.image_2 = customtkinter.CTkLabel(self.frame_2, image=self.img, bg_color="white")
        self.image_2.grid(row=1, column=1)

        self.frame_1.grid(row=0, column=1, padx=10, pady=y_padding)
        self.frame_1.configure(bg ='')
        self.label_1 = customtkinter.CTkLabel(master=self.frame_1, text="Log File")
        self.label_1.pack(pady=y_padding)
        self.label_1.configure(font=("Roboto", 20, "bold"))

        # Create text widget and specify size.
        log_text = Text(self.frame_1, height=25, width=500)

        log_file_path = PATH + "/log_file.txt"
        print(log_file_path)
        log_file_path = open(log_file_path)  # or tf = open(tf, 'r')
        data = log_file_path.read()
        log_text.insert(END, data)
        log_file_path.close()

        # Create an Exit button.
        button_1 = customtkinter.CTkButton(master=self.frame_1, text="Main menu", corner_radius=8,
                                           command=lambda: [self.destroy(), open_operation_window()],
                                           fg_color=("blue", "green"), height=40,
                                           width=400)

        button_2 = customtkinter.CTkButton(master=self.frame_1, text="End", corner_radius=8,
                                           command=lambda: [self.destroy()],
                                           fg_color=("blue", "green"), height=40,
                                           width=400)
        log_text.pack()
        button_1.pack(pady=y_padding)
        button_2.pack(pady=y_padding)

    def on_closing(self):
        self.destroy()


def open_operation_window():
    operation_window = OperationWindow()
    operation_window.mainloop()


if __name__ == "__main__":
    open_log_window = OpenLogFileWindow()
    open_log_window.mainloop()
