import tkinter as tk
from tkinter import messagebox, ttk, simpledialog
import random

class Gift:
    def __init__(self, master):
        self.gifts_list = []

        self.master = master
        self.master.title("완료!")
        self.master.geometry("210x100")
        self.master.resizable(False, False)

        self.gifts_combobox = ttk.Combobox(master, values=self.gifts_list, width=23)
        self.select_button = tk.Button(master, text="선택", command=self.select_gift)
        self.add_button = tk.Button(master, text="추가", command=self.add_gift)
        self.delete_button = tk.Button(master, text="삭제", command=self.delete_gift)

        self.gifts_combobox.set("랜덤")
        self.gifts_combobox.pack(pady= 5, ipady=8)
        self.select_button.pack(side="left", expand=True, ipady=5, ipadx=20)
        self.add_button.pack(side="left", ipady=5, ipadx=5)
        self.delete_button.pack(side="left", expand=True, ipady=5, ipadx=5)

        self.load_file()

    def select_gift(self):
        selected_gift = self.gifts_combobox.get()
        if selected_gift == "랜덤":
            random_gift = random.choice(self.gifts_list)
            self.show_result(random_gift)
        else:
            self.show_result(selected_gift)

    def add_gift(self):
        selected_gift = self.gifts_combobox.get()
        new_gift = simpledialog.askstring("추가", "추가할 선물을 입력하세요")
        can_add = new_gift and selected_gift not in self.gifts_list
        if can_add:
            file_name = "선물.txt"
            print(selected_gift)
            with open(file_name, 'a', encoding="utf-8") as file:
                file.write(new_gift + "\n")
        self.load_file()

    def delete_gift(self):
        selected_gift = self.gifts_combobox.get()
        if selected_gift in self.gifts_list:
            confirm = messagebox.askokcancel("삭제", "정말로 삭제 하시겠습니까?", default="cancel")
            if confirm:
                self.gifts_list.remove(selected_gift)
                file_name = "선물.txt"
                with open(file_name, 'w+', encoding="utf-8") as file:
                    for gift in self.gifts_list:
                        file.write(gift + "\n")
                self.load_file()
        else:
            messagebox.showwarning("경고", "존재하지 않는 선물입니다.")

    def show_result(self, result):
        messagebox.showinfo("선물이에요!", "당신에게 "+ result +"을(를) 선물해 주세요!")

    def load_file(self):
        try:
            with open("선물.txt", "r", encoding="utf-8") as file:
                self.gifts_list = file.readlines()
                self.gifts_list = [gift.rstrip("\n") for gift in self.gifts_list]
            self.gifts_combobox.config(values=self.gifts_list)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")