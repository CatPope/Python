import tkinter as tk
from tkinter import simpledialog, messagebox
import os

class ProgressTrackerApp:
    def __init__(self, master):
        self.master = master
        self.master.title("진행도를 알 수 있는 계획표")

        self.current_goal = None
        self.load_saved_data()

        self.goal_label = tk.Label(master, text=self.current_goal)
        self.goal_label.pack()

        self.progress_label = tk.Label(master, text="진행도: 0%")
        self.progress_label.pack()

        self.plan_entry = tk.Entry(master)
        self.plan_entry.pack()

        self.add_plan_button = tk.Button(master, text="계획 추가", command=self.add_plan)
        self.add_plan_button.pack()

        self.modify_plan_button = tk.Button(master, text="계획 수정", command=self.modify_plan)
        self.modify_plan_button.pack()

        self.delete_plan_button = tk.Button(master, text="계획 삭제", command=self.delete_plan)
        self.delete_plan_button.pack()

        self.plan_listbox = tk.Listbox(master)
        self.plan_listbox.pack()

        self.complete_plan_button = tk.Button(master, text="계획 완료", command=self.complete_plan)
        self.complete_plan_button.pack()

        self.save_button = tk.Button(master, text="저장 (Ctrl + S)", command=self.save_plans)
        self.save_button.pack()

        self.master.bind("<Control-s>", lambda event: self.save_plans())

    def add_plan(self):
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
            self.plan_listbox.delete(selected_index)
            self.update_progress()
        else:
            messagebox.showwarning("경고", "삭제할 계획을 선택하세요.")

    def complete_plan(self):
        selected_index = self.plan_listbox.curselection()
        if selected_index:
            self.plan_listbox.itemconfig(selected_index, {'bg': 'light green'})
            self.update_progress()
        else:
            messagebox.showwarning("경고", "완료할 계획을 선택하세요.")

    def update_progress(self):
        total_plans = self.plan_listbox.size()
        completed_plans = sum(1 for i in range(total_plans) if 'light green' in self.plan_listbox.itemcget(i, 'bg'))
        percentage = (completed_plans / total_plans) * 100 if total_plans > 0 else 0
        self.progress_label.config(text=f"진행도: {percentage:.1f}%")

    def save_plans(self):
        if self.current_goal:
            goal_folder = os.path.join("plans", self.current_goal)
            os.makedirs(goal_folder, exist_ok=True)
            file_path = os.path.join(goal_folder, "plans.txt")

            with open(file_path, 'w') as file:
                for i in range(self.plan_listbox.size()):
                    file.write(f"{self.plan_listbox.get(i)}\n")

            messagebox.showinfo("저장 완료", "계획이 성공적으로 저장되었습니다.")

    def load_plans(self):
        if self.current_goal:
            goal_folder = os.path.join("plans", self.current_goal)
            file_path = os.path.join(goal_folder, "plans.txt")

            if os.path.exists(file_path):
                with open(file_path, 'r') as file:
                    plans = [line.strip() for line in file.readlines()]
                    for plan in plans:
                        self.plan_listbox.insert(tk.END, plan)

    def load_saved_data(self):
        self.current_goal = simpledialog.askstring("불러오기", "불러올 목표를 입력하세요:", parent=self.master)
        if self.current_goal:
            self.load_plans()
        else:
            messagebox.showwarning("경고", "목표를 입력하세요.")

if __name__ == "__main__":
    root = tk.Tk()
    app = ProgressTrackerApp(root)
    root.mainloop()
