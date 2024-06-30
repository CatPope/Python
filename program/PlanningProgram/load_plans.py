import tkinter as tk
from tkinter import ttk, messagebox, font
import os
from planning_chart import PlanningChart


class LoadPlans:
    def __init__(self, master):
        self.master = master
        self.master.title("관리자")
        self.master.geometry("210x100")
        self.master.resizable(False, False)
        self.master.protocol("WM_DELETE_WINDOW", self.close_master)

        self.goals_list = self.load_goals()
        self.opened_plans = []

        self.goals_combobox = ttk.Combobox(master, values=self.goals_list, width=23)
        self.select_button = tk.Button(master, text="파일 열기", command=self.entered_goal)
        self.delete_file_button = tk.Button(master, text="파일 삭제", command=self.delete_selected_file)

        self.goals_combobox.set("목표 선택")
        self.goals_combobox.pack(side="top", pady=8, ipady=5)
        self.select_button.pack(side="left", expand=True, padx=10, ipady=5, ipadx=10)
        self.delete_file_button.pack(side="left", expand=True, padx=10, ipady=5, ipadx=10)

        self.master.bind("<FocusIn>", lambda event: self.goals_combobox.config(values=self.goals_list))
        self.goals_combobox.bind("<FocusIn>", lambda event: self.on_combobox_selected())
        self.goals_combobox.bind("<Return>", self.entered_goal)

    def goals_path(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        goals_dir = os.path.join(current_dir, '목표')
        return goals_dir

    def entered_goal(self, event=None):
        selected_goal_value = self.goals_combobox.get()
        no_selected = selected_goal_value=="목표 선택" or selected_goal_value==""
        if no_selected:
            messagebox.showwarning("경고", "목표를 선택하거나 입력하세요", icon='warning')
        elif selected_goal_value in self.goals_list:
            self.open_plans(selected_goal_value)
        else:
            self.make_goal(selected_goal_value)

    def make_goal(self, goal_value, event=None):
        if goal_value.strip():
            file_name = goal_value + ".txt"
            save_path = os.path.join(self.goals_path(), file_name)
            with open(save_path, 'w') as file:
                pass
            self.update_combobox()
            self.open_plans(goal_value)
        else:
            messagebox.showwarning("경고", "목를 입력하세요", icon='warning')        

    def on_combobox_selected(self, event=None):
        current_value = self.goals_combobox.get()
        if current_value == "목표 선택":
            self.goals_combobox.set("")

    def load_goals(self):
        load_path = self.goals_path()
        if not os.path.exists(load_path):
            os.makedirs(load_path)
        goals_file_list = os.listdir(path=load_path)
        goals_list = []
        for goal_file in goals_file_list:
            sp_file = goal_file.split('.')
            goals_list.append(sp_file[0])
        return goals_list

    def update_combobox(self):
        self.goals_list = self.load_goals()
        self.goals_combobox.config(values=self.goals_list)

    def delete_selected_file(self):
        selected_goal_value = self.goals_combobox.get()
        if selected_goal_value == "목표 선택":
            messagebox.showwarning("경고", "목표를 선택하세요", icon='warning')
        else:
            try:
                confirm = messagebox.askokcancel("파일 삭제", "정말로 삭제하시겠습니까?", icon='warning', default="cancel")
                if confirm:
                    file_path = os.path.join(self.goals_path(), f"{selected_goal_value}.txt")
                    if os.path.exists(file_path):
                        os.remove(file_path)
                        messagebox.showinfo("파일 삭제 완료", "파일이 성공적으로 삭제되었습니다", icon='info')
                        self.update_combobox()
                    else:
                        messagebox.showwarning("경고", "삭제할 파일이 존재하지 않습니다", icon='warning')
            except Exception as e:
                messagebox.showerror("오류", f"파일 삭제 중 오류가 발생했습니다: {e}", icon='error', default='error')

    def open_plans(self, goal):
        if goal in self.opened_plans:
            messagebox.showwarning("경고", "이미 열려있는 창입니다", icon='info')
        else:
            self.opened_plans.append(goal)
            window_planning = tk.Toplevel(self.master)
            app_planning = PlanningChart(window_planning, goal, self.opened_plans)

    def close_master(self):
        if self.opened_plans:
            confirm = messagebox.askyesno("종료", "모든 화면이 종료됩니다. 종료 하시겠 습니까?", icon='warning', default="no")
            if confirm:
                root.quit()
        else:
            root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app_load = LoadPlans(root)
    root.mainloop()
