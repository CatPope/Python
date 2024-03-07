import tkinter as tk
from tkinter import simpledialog, ttk, messagebox
import os

class PlanningChart:
    def __init__(self, master, goal, opened_plans):

        self.goal = goal
        self.opened_plans = opened_plans
        self.finished_plans = []

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

        self.check_plan_button = tk.Button(master, text="완료", command=self.check_plan)
        self.check_plan_button.pack()

        self.plan_listbox = tk.Listbox(master)
        self.plan_listbox.config(selectmode="extended")
        self.load_file()
        self.plan_listbox.pack()

        self.save_button = tk.Button(master, text="저장 (Ctrl + S)", command=self.save_plans)
        self.save_button.pack()

        self.master.bind("<Control-s>", lambda event: self.save_plans())
        self.master.bind("<Control-w>", lambda event: self.close_plans)
        self.master.bind("<Delete>", lambda event: self.delete_plan())
        self.plan_entry.bind("<Return>", self.add_plan)

        
        self.update_progress()

    def add_plan(self, event=None):
        plan = self.plan_entry.get()
        if plan:
            self.plan_listbox.insert(0, plan)
            self.plan_entry.delete(0, tk.END)
            self.update_progress()
        else:
            messagebox.showwarning("경고", "계획을 입력하세요")

    def modify_plan(self):
        checked_list = self.checked_or_no()
        print(checked_list)
        if len(checked_list) == 1:
            index, checked = checked_list[0]
            modified_plan = simpledialog.askstring("계획 수정", "수정된 계획을 입력하세요:", parent=self.master)
            if checked == '$$':
                modified_plan = modified_plan+'$$'
                print(modified_plan)
            if modified_plan:
                self.plan_listbox.delete(index)
                self.plan_listbox.insert(index, modified_plan)
                self.check_plan()
        else:
            messagebox.showwarning("경고", "계획을 한개만 선택하세요")

    def delete_plan(self):
        selected_indices = self.plan_listbox.curselection()
        if selected_indices:
            confirm = messagebox.askokcancel("삭제", "진짜로 삭제한다?")
            if confirm:
                for index in reversed(selected_indices):
                    self.plan_listbox.delete(index)
                self.update_progress()
        else:
            messagebox.showwarning("경고", "계획을 선택하세요")

    def checked_or_no(self):
        selected_indices = self.plan_listbox.curselection()
        checked_list = []
        if selected_indices:
            for index in reversed(selected_indices):
                plan_text = self.plan_listbox.get(index)
                checked = plan_text[-2]
                checked_list.append((index, checked))
            return checked_list
        else:
            messagebox.showwarning("경고", "계획을 선택하세요")
            return []


    def check_plan(self):
        for index, checked in self.checked_or_no():
            if checked == '$$':
                self.plan_listbox.itemconfig(index, {'bg': 'white'})
            else:
                self.plan_listbox.itemconfig(index, {'bg': 'light green'})
        self.update_progress()

    def update_progress(self):
        total_plans = self.plan_listbox.size()
        completed_plans = sum(1 for i in range(total_plans) if 'light green' in self.plan_listbox.itemcget(i, 'bg'))
        percentage = (completed_plans / total_plans) * 100 if total_plans > 0 else 0
        self.progress_bar["value"] = percentage
        self.progress_label.config(text=f"진행도: {percentage:.2f}% ({completed_plans}/{total_plans})")

    def save_plans(self):
        if self.goal:
            file_path = os.path.join("목표", f"{self.goal}.txt")

            with open(file_path, 'w') as file:
                for i in range(self.plan_listbox.size()):
                    file.write(f"{self.plan_listbox.get(i)}\n")

            messagebox.showinfo("저장 완료", "계획이 성공적으로 저장되었습니다")

    def close_plans(self):
        confirm = messagebox.askokcancel("저장", "저장 하시겠습니까?")
        if confirm:
            self.save_plans()
            self.opened_plans.remove(self.goal)
            self.master.destroy()

    def load_file(self):
        file_path = os.path.join("목표", f"{self.goal}.txt")
        if file_path:
            with open(file_path, 'r') as file:
                content = file.readlines()
            for line in content:
                self.plan_listbox.insert(tk.END, line.strip(" $$"))