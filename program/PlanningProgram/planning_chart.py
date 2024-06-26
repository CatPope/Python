import tkinter as tk
from tkinter import simpledialog, ttk, messagebox, font
import os
from gift import Gift

class PlanningChart:
    def __init__(self, master, goal, opened_plans):

        self.goal = goal
        self.file_path = os.path.join("목표", self.goal+".txt")
        self.opened_plans = opened_plans
        self.customfont = font.Font(family="Comic Sans MS", size=20, weight="bold")

        self.master = master
        self.master.title(goal)
        self.master.geometry("300x470")
        self.master.protocol("WM_DELETE_WINDOW", self.close_plans)

        self.goal_label = tk.Label(master, text=goal, font=self.customfont)
        self.progress_label = tk.Label(master, text="진행도: 0% (0/0)")
        self.progress_bar = ttk.Progressbar(master, orient="horizontal", length=120)
        self.plan_entry = tk.Entry(master)

        self.listbox_frame = tk.Frame(master)
        self.plans_scrollbar = tk.Scrollbar(self.listbox_frame, orient=tk.VERTICAL)
        self.plan_listbox = tk.Listbox(self.listbox_frame, yscrollcommand=self.plans_scrollbar.set)

        self.buttons_frame = tk.Frame(master)
        self.add_plan_button = tk.Button(self.buttons_frame, text="추가", command=self.add_plan)
        self.delete_plan_button = tk.Button(self.buttons_frame, text="삭제", command=self.delete_plan)
        self.modify_plan_button = tk.Button(self.buttons_frame, text="수정", command=self.modify_plan)
        self.check_plan_button = tk.Button(self.buttons_frame, text="완료", command=self.check_plan)
        self.save_button = tk.Button(master, text="저장 (Ctrl + S)", command=self.save_plans)

        self.goal_label.pack(side="top", fill="x", padx=10, pady=10)
        self.progress_label.pack(side="top", expand=False)
        self.progress_bar.pack(side="top", fill="x", padx=20, pady=3)
        self.plan_entry.pack(side="top", fill="x", padx=15, pady=2)
        self.save_button.pack(side="bottom", pady=10)

        self.listbox_frame.pack(side="bottom", expand=True, fill="both", padx=20)
        self.plans_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.plan_listbox.pack(expand=True, fill="both")
        self.plans_scrollbar.config(command=self.plan_listbox.yview)
        self.plan_listbox.config(selectmode="extended")

        self.buttons_frame.pack(side="left", expand=True, fill="x", padx=10)
        self.add_plan_button.pack(side="left", expand=True, pady=10, ipadx=5, ipady=5)
        self.delete_plan_button.pack(side="left", expand=True, pady=10, ipadx=5, ipady=5)
        self.modify_plan_button.pack(side="left", expand=True, pady=10, ipadx=5, ipady=5)
        self.check_plan_button.pack(side="left", expand=True, pady=10, ipadx=5, ipady=5)

        self.master.bind("<Control-s>", lambda event: self.save_plans())
        self.master.bind("<Control-w>", lambda event: self.close_plans)
        self.master.bind("<Delete>", lambda event: self.delete_plan())
        self.plan_entry.bind("<Return>", self.add_plan)

        self.load_file()
        self.update_progress()


    def add_plan(self, event=None):
        plan = self.plan_entry.get()
        if plan:
            self.plan_listbox.insert(0, plan)
            self.plan_entry.delete(0, tk.END)
            self.update_progress()
        else:
            messagebox.showwarning("경고", "계획을 입력하세요", icon='warning')

    def modify_plan(self):
        selected_indices = self.plan_listbox.curselection()
        if len(selected_indices) == 1:
            checked_list = self.plan_color(selected_indices)
            index, checked = checked_list[0]
            modified_plan = simpledialog.askstring("계획 수정", "수정된 계획을 입력하세요", parent=self.master)
            if modified_plan:
                if checked != ' ':
                    modified_plan = modified_plan+' ' 
                self.plan_listbox.delete(index)
                self.plan_listbox.insert(index, modified_plan)
                self.check_plan(selected_indices)
        else:
            messagebox.showwarning("경고", "한 가지 계획 만 선택하세요", icon='warning')

    def delete_plan(self):
        selected_indices = self.plan_listbox.curselection()
        if selected_indices:
            confirm = messagebox.askokcancel("삭제", "정말로 삭제하시겠습니까?", icon='warning', default="cancel")
            if confirm:
                try:
                    for index in reversed(selected_indices):
                        self.plan_listbox.delete(index)
                    self.update_progress()
                except Exception as e:
                    messagebox.showerror("오류", f"파일 삭제중 오류가 발생했습니다: {e}", icon='error', default='error')
        else:
            messagebox.showwarning("경고", "계획을 선택하세요", icon='warning')

    def plan_color(self, selected_indices, get_list=False):
        checked_list = []
        if selected_indices:
            for index in reversed(selected_indices):
                plan_text = self.plan_listbox.get(index)
                checked = plan_text[-1]
                checked_list.append((index, checked))
                if checked == ' ':
                    self.plan_listbox.itemconfig(index, {'bg': 'light green'})
                else:
                    self.plan_listbox.itemconfig(index, {'bg': 'white'})
            self.update_progress()
            return checked_list
        elif selected_indices == False:
            pass
        elif get_list == True:
            return checked_list
        else:
            messagebox.showwarning("경고", "계획을 선택하세요", icon='warning')
            return []

    def check_plan(self, selected_indices=None):
        if selected_indices == None:
            selected_indices = self.plan_listbox.curselection()
        chacked_list = self.plan_color(selected_indices, get_list=True)
        for index, checked in chacked_list:
            plan_text = self.plan_listbox.get(index)
            if checked == ' ':
                self.plan_listbox.delete(index)
                self.plan_listbox.insert(index, plan_text[0:len(plan_text)-1])
            else:
                self.plan_listbox.delete(index)
                self.plan_listbox.insert(index, plan_text+' ')
        self.plan_color(selected_indices)
        self.finished_plan()
        self.update_progress()

    def update_progress(self):
        total_plans = self.plan_listbox.size()
        completed_plans = sum(1 for i in range(total_plans) if 'light green' in self.plan_listbox.itemcget(i, 'bg'))
        percentage = (completed_plans / total_plans) * 100 if total_plans > 0 else 0
        self.progress_bar["value"] = percentage
        self.progress_label.config(text=f"진행도: {percentage:.2f}% ({completed_plans}/{total_plans})")

    def finished_plan(self):
        colors = self.chack_all()
        if colors:
            for color in colors:
                if color[1] != ' ':
                    return False
            window_gift = tk.Toplevel(self.master)
            app_gift = Gift(window_gift, self.goal)

    def chack_all(self):
        all_index = self.plan_listbox.size()
        index_list = list(range(all_index)) if all_index !=0 else False
        color = self.plan_color(index_list)
        return color

    def save_plans(self):
        try:
            with open(self.file_path, 'w', encoding="utf-8") as file:
                for plan in self.plan_listbox.get(0, tk.END):
                    file.write(plan +"\n")
        except Exception as e:
            messagebox.showerror("Error", f"파일을 저장하는중 오류가 발생했습니다: {e}", default='error')

    def close_plans(self):
        confirm = messagebox.askyesnocancel("종료", "저장 하시겠습니까?", icon='question')
        if confirm == True:
            try:
                self.save_plans()
                self.opened_plans.remove(self.goal)
                self.master.destroy()
            except Exception as e:
                messagebox.showerror("오류", f"파일 저장중 오류가 발생했습니다: {e}", default='error')
        elif confirm == False:
            self.opened_plans.remove(self.goal)
            self.master.destroy()

    def load_file(self):
        try:
            if self.file_path:
                with open(self.file_path, 'r', encoding="utf-8") as file:
                    content = file.readlines()
                for line in content:
                    self.plan_listbox.insert(tk.END, line.rstrip("\n"))
                color = self.chack_all()
        except Exception as e:
            messagebox.showerror("Error", f"파일을 불러오는중 오류가 발생했습니다: {e}", default='error')