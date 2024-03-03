import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import os
from planning_chart import PlanningChart


class LoadPlans:
    def __init__(self, master):
        self.master = master
        self.master.title("목표 선택")

        self.goals_list = self.load_goals()

        self.opened_plans = []

        self.new_goal_entry = tk.Entry(master)
        self.new_goal_entry.pack()

        self.new_goal_button = tk.Button(master, text="생성", command=self.make_goal)
        self.new_goal_button.pack()

        self.goals_combobox = ttk.Combobox(master, values=self.goals_list)
        self.goals_combobox.set("목표 선택")
        self.goals_combobox.pack()

        self.select_button = tk.Button(master, text="불러오기", command=self.select_goal)
        self.select_button.pack()

    def goals_path(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        goals_dir = os.path.join(current_dir, '목표')
        return goals_dir

    def make_goal(self):
        new_goal_value = self.new_goal_entry.get()
        file_name = new_goal_value + ".txt"
        if file_name.split() == [".txt"]:
            messagebox.showwarning("경고", "목표를 입력해 주세요")
        elif file_name in self.goals_list:
            messagebox.showwarning("경고", "존제하는 목표입니다")
        else:
            save_path = os.path.join(self.goals_path(), file_name)
            with open(save_path, 'w') as file:
                file.write(file_name)
            self.goals_list = self.load_goals()
            self.goals_combobox.config(values=self.goals_list)
            self.open_plans(file_name)

    def select_goal(self):
        selected_goal_value = self.goals_combobox.get()
        if selected_goal_value == "목표 선택":
            messagebox.showwarning("경고", "목표를 선택하세요")
        else:
            self.open_plans(selected_goal_value)

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

    def open_plans(self, goal):
        if goal in self.opened_plans:
            messagebox.showwarning("경고", "이미 열려있는 창입니다")
        else:
            self.opened_plans.append(goal)
            window_planning = tk.Toplevel(self.master)
            # root.iconify() #화면 최소화
            app_planning = PlanningChart(window_planning, goal)

if __name__ == "__main__":
    root = tk.Tk()
    app_load = LoadPlans(root)
    root.mainloop()
