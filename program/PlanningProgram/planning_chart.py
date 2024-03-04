import tkinter as tk
from tkinter import simpledialog, ttk, messagebox
import os

class PlanningChart:
    def __init__(self, master, goal, opened_plans):

        self.goal = goal
        self.opened_plans = opened_plans
        self.finished_plans = []
        # self.load_file()

        self.master = master
        self.master.title(goal)

        self.master.protocol("WM_DELETE_WINDOW", self.close_plans)
        
        self.goal_label = tk.Label(master, text=goal)
        self.goal_label.pack()

        self.progress_label = tk.Label(master, text="진행도: 0% (0/0)")
        self.progress_label.pack()

        self.progress_bar = ttk.Progressbar(master, orient="horizontal", length=120)
        self.progress_bar.pack()

        self.plan_entry = tk.Entry(master)
        self.plan_entry.pack()

        self.add_plan_button = tk.Button(master, text="계획 추가", command=self.add_plan)
        self.add_plan_button.pack()

        self.modify_plan_button = tk.Button(master, text="계획 수정", command=self.modify_plan)
        self.modify_plan_button.pack()

        self.delete_plan_button = tk.Button(master, text="삭제", command=self.delete_plan)
        self.delete_plan_button.pack()

        self.chacked_plan_button = tk.Button(master, text="완료", command=self.chacked_plan)
        self.chacked_plan_button.pack()

        self.plan_listbox = tk.Listbox(master)
        self.plan_listbox.pack()

        self.save_button = tk.Button(master, text="저장 (Ctrl + S)", command=self.save_plans)
        self.save_button.pack()

        self.master.bind("<Control-s>", lambda event: self.save_plans())
        self.master.bind("<Delete>", lambda event: self.delete_plan())
        self.plan_entry.bind("<Return>", self.add_plan)

    def add_plan(self, event=None):
        plan = self.plan_entry.get()
        if plan:
            self.plan_listbox.insert(tk.END, plan)
            self.plan_entry.delete(0, tk.END)
            self.update_progress()
        else:
            messagebox.showwarning("경고", "계획을 입력하세요.")

    def modify_plan(self):
        selected_index = self.plan_listbox.curselection()
        if selected_index:
            modified_plan = simpledialog.askstring("계획 수정", "수정된 계획을 입력하세요:", parent=self.master)
            if modified_plan:
                self.plan_listbox.delete(selected_index)
                self.plan_listbox.insert(selected_index, modified_plan)
                self.update_progress()
        else:
            messagebox.showwarning("경고", "수정할 계획을 선택하세요.")

    def delete_plan(self):
        selected_index = self.plan_listbox.curselection()
        if selected_index:
            confirm = messagebox.askokcancel("삭제", "진짜로 삭제한다?")
            if confirm:
                self.plan_listbox.delete(selected_index)
                self.update_progress()
        else:
            messagebox.showwarning("경고", "삭제할 계획을 선택하세요.")

    def chacked_plan(self):
        selected_index = self.plan_listbox.curselection()
        if selected_index:
            item_bg_color = self.plan_listbox.itemcget(selected_index[0], 'bg')
            if item_bg_color=='white' or item_bg_color=='':
                self.plan_listbox.itemconfig(selected_index, {'bg': 'light green'})
                self.update_progress()
            else:
                self.plan_listbox.itemconfig(selected_index, {'bg': 'white'})
                self.update_progress()
        else:
            messagebox.showwarning("경고", "완료할 계획을 선택하세요.")

    def update_progress(self):
        total_plans = self.plan_listbox.size()
        completed_plans = sum(1 for i in range(total_plans) if 'light green' in self.plan_listbox.itemcget(i, 'bg'))
        percentage = (completed_plans / total_plans) * 100 if total_plans > 0 else 0
        self.progress_bar["value"] = percentage
        self.progress_label.config(text=f"진행도: {percentage:.2f}% ({completed_plans}/{total_plans})")

    def save_plans(self):
        if self.goal:
            file_path = os.path.join("goals", f"{self.goal}.txt")

            with open(file_path, 'w') as file:
                for i in range(self.plan_listbox.size()):
                    file.write(f"{self.plan_listbox.get(i)}\n")

            messagebox.showinfo("저장 완료", "계획이 성공적으로 저장되었습니다.")

    def close_plans(self):
        self.opened_plans.remove(self.goal)
        self.master.destroy()

    # def load_file(self):
    #     file_path = os.path.join("goals", f"{self.goal}.txt")
    #     print("작동")
    #     if file_path:
    #         with open(file_path, 'r') as file:
    #             content = file.readlines()
    #             print(content)
    #         for line in content:
    #             self.plan_listbox.insert(tk.END, line.strip())