import tkinter as tk
from tkinter import messagebox
import random

class Award:
    def __init__(self, master):
        self.master = master
        self.master.title("Random Content")

        self.random_button = tk.Button(master, text="Random Content", command=self.show_random_content)
        self.random_button.pack(pady=10)

    def show_random_content(self):
        try:
            with open("상.txt", "r", encoding="utf-8") as file:
                lines = file.readlines()
                random_line = random.choice(lines)
                messagebox.showinfo("Random Content", random_line)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = Award(root)
    root.mainloop()