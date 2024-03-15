import tkinter as tk
from tkinter import ttk, messagebox, font
import os
from planning_chart import PlanningChart


class Award:
    def __init__(self, master, goal):
        self.goal = goal

        self.master = master
        self.master.title(goal+" 완료!")
        self.master.geometry("250x150")
        self.master.resizable(False, False)


        self.goals_combobox = ttk.Combobox(master, values=self.goals_list, width=23)
        self.select_button = tk.Button(master, text="파일 열기", command=self.entered_goal)
        self.delete_file_button = tk.Button(master, text="파일 삭제", command=self.delete_selected_file)

        self.goals_combobox.set("랜덤")
        self.goals_combobox.pack(side="top", pady=10)
        self.select_button.pack(side="left", expand=True, ipady=5)
        self.delete_file_button.pack(side="left", expand=True, ipady=5)

    def load_award(self):
        if self.file_path:
            with open(self.file_path, 'r') as file:
                content = file.readlines()
            for line in content:
                self.plan_listbox.insert(tk.END, line.strip("\n"))