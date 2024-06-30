import tkinter as tk
import datetime as dt
from tkinter import messagebox, ttk, simpledialog
import random

class Gift:
    def __init__(self, master, goal):
        self.goal = goal
        self.gifts_list = []

        self.master = master
        self.master.title("완료!")
        self.master.geometry("200x130")
        self.master.resizable(False, False)
        self.master.grab_set()

        self.gifts_combobox = ttk.Combobox(master, values=self.gifts_list, width=23)
        self.records_button = tk.Button(master, text="기록", command=self.records_window)
        self.select_button = tk.Button(master, text="선택", command=self.select_gift)
        self.add_button = tk.Button(master, text="추가", command=self.add_gift)
        self.delete_button = tk.Button(master, text="삭제", command=self.delete_gift)

        self.records_button.pack(side="top", anchor="nw", padx=5, pady=5)
        self.gifts_combobox.set("선택 & 입력")
        self.gifts_combobox.pack(pady= 5, ipady=8)
        self.select_button.pack(side="left", expand=True, ipady=5, ipadx=20)
        self.add_button.pack(side="left", ipady=5, ipadx=5)
        self.delete_button.pack(side="left", expand=True, ipady=5, ipadx=5)

        self.gifts_combobox.bind("<FocusIn>", lambda event: self.on_combobox_selected())
        self.master.bind("<Delete>", self.delete_gift)
        self.master.bind("<Return>", self.add_gift)

        self.load_file()

    def on_combobox_selected(self, event=None):
        selected_gift = self.gifts_combobox.get()
        if selected_gift == "선택 & 입력":
            self.gifts_combobox.set("")

    def select_gift(self):
        selected_gift = self.gifts_combobox.get()
        r_can_select = selected_gift == "랜덤" and selected_gift.rstrip() != '' and len(self.gifts_list)>1
        s_can_select = self.gifts_list[1:] and selected_gift in self.gifts_list
        if r_can_select:
            random_gift = random.choice(self.gifts_list[1:])
            self.show_result(random_gift)
        elif s_can_select:
            self.show_result(selected_gift)
        else:
            messagebox.showwarning("경고", "선물을 추가하세요", icon='warning')

    def add_gift(self, event=None):
        selected_gift = self.gifts_combobox.get()
        if selected_gift == "선택 & 입력" or selected_gift == "랜덤":
            messagebox.showwarning("경고", "추가 할 수 없는 선물입니다", icon='warning')
        elif selected_gift.rstrip() == '':
            messagebox.showwarning("경고", "선물을 입력해 주세요", icon='warning')
        elif selected_gift in self.gifts_list:
            messagebox.showwarning("경고", "이미 존재하는 선물입니다", icon='warning')
        else:
            with open("선물.txt", 'a', encoding="utf-8") as file:
                if "랜덤" not in self.gifts_list:
                    file.write("랜덤\n")
                file.write(selected_gift + "\n")
            messagebox.showinfo("완료", "추가되었습니다", icon='info')
        self.load_file()

    def delete_gift(self, event=None):
        selected_gift = self.gifts_combobox.get()
        if selected_gift not in self.gifts_list:
            messagebox.showwarning("경고", "존재하지 않는 선물입니다", icon='warning')
        elif selected_gift == "랜덤":
            messagebox.showwarning("경고", "삭제 할수 없는 선물입니다", icon='warning')
        else:
            confirm = messagebox.askokcancel("삭제", "정말로 삭제 하시겠습니까?", icon='warning', default="cancel")
            if confirm:
                self.gifts_list.remove(selected_gift)
                with open("선물.txt", 'w+', encoding="utf-8") as file:
                    for gift in self.gifts_list:
                        file.write(gift + "\n")
                self.load_file()
                messagebox.showinfo("완료", "삭제되었습니다", icon='info')

    def show_result(self, result):
        confirm = messagebox.askyesno("선물이에요!", "당신에게 "+ result +"을(를) 선물해 주세요!", icon='info')
        if confirm:
            self.completed_file(result)

    def load_file(self):
        try:
            with open("선물.txt", "r", encoding="utf-8") as file:
                self.gifts_list = file.readlines()
                self.gifts_list = [gift.rstrip("\n") for gift in self.gifts_list]
            self.gifts_combobox.config(values=self.gifts_list)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}", icon='error', default='error')

    def close_window(self):
        self.master.grab_release()
        self.master.destroy()

    def completed_file(self, gift):
        today = self.time_data()
        with open("성공기록.txt", 'a', encoding="utf-8") as file:
            file.write(self.goal +' | '+ gift +' | '+ today +"\n")

    def time_data(self):
        today = dt.datetime.now().strftime('%F')
        w_list = ['월', '화', '수', '목', '금', '토', '일']
        w_index = dt.datetime.today().weekday()
        weekday = w_list[w_index]
        result = today +'('+ weekday +')'
        return result

    def records_window(self):
        window_record = tk.Toplevel(self.master)
        app_record = Record(window_record)



class Record:
    def __init__(self, master):
        self.master = master
        self.master.title("성공기록")
        self.master.geometry("400x190")
        master.grab_set()

        self.records_list = []

        self.master.protocol("WM_DELETE_WINDOW", self.close_window)

        self.listbox_frame = tk.Frame(master)
        self.records_scrollbar = tk.Scrollbar(self.listbox_frame, orient=tk.VERTICAL)
        self.records_listbox = tk.Listbox(self.listbox_frame, yscrollcommand=self.records_scrollbar.set)
        self.delete_button = tk.Button(master, text="삭제", command= self.delete_listbox)

        self.listbox_frame.pack(expand=True, fill="both")
        self.records_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.records_listbox.pack(expand=True, fill="both")
        self.records_scrollbar.config(command=self.records_listbox.yview)
        self.records_listbox.config(selectmode="extended")
        self.delete_button.pack(side="bottom", ipadx=5)

        self.load_file()


    def delete_listbox(self):
        selected_index = self.records_listbox.curselection()
        if selected_index:
            confirm = messagebox.askokcancel("삭제", "정말로 삭제하시겠습니까?", icon='warning')
            if confirm:
                for index in reversed(selected_index):
                    del self.records_list[index]
                with open("성공기록.txt", 'w', encoding="utf-8") as file:
                    self.records_listbox.delete(0, tk.END)
                    for record in self.records_list:
                        file.write(record)
                self.load_file()
                messagebox.showinfo("완료", "삭제되었습니다", icon='info')

    def load_file(self):
        try:
            with open("성공기록.txt", "r", encoding="utf-8") as file:
                self.records_list = file.readlines()
                self.records_list = [record.rstrip("\n") for record in self.records_list]
                self.records_listbox.delete(0, tk.END)
                if self.records_list:
                    for text in self.records_list:
                        self.records_listbox.insert(tk.END, text)
                else:
                    self.records_listbox.insert(tk.END, "선물을 선택해 보세요!")
        except FileNotFoundError:
            with open("성공기록.txt", "w", encoding="utf-8") as file:
                pass
            self.records_listbox.insert(tk.END, "선물을 선택해 보세요!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}", icon='error', default='error')


    def close_window(self):
        self.master.grab_release()
        self.master.destroy()

        
if __name__ == "__main__":
    root = tk.Tk()
    app_load = Gift(root)
    root.mainloop()