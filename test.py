import tkinter as tk

root = tk.Tk()


def do_something(event=None):
    print("did something!")


btn = tk.Button(root, text="submit", command=do_something)
btn.pack()
btn.bind("<Return>", do_something)
# root.bind("<Return>", do_something) will work without the button having focus.

root.mainloop()
