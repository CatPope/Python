import tkinter as tk

class PlanningChart:
    def __init__(self, master):
        self.master = master
        self.master.title("Planning Chart")

        self.plan_listbox = tk.Listbox(self.master, selectmode="extended")
        self.plan_listbox.pack(fill=tk.BOTH, expand=True)

        self.plans_scrollbar = tk.Scrollbar(self.master)
        self.plans_scrollbar.config(command=self.plan_listbox.yview)
        self.plans_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # 연결
        self.plan_listbox.config(yscrollcommand=self.plans_scrollbar.set)

        # 예시로 몇 가지 아이템 추가
        for i in range(1, 21):
            self.plan_listbox.insert(tk.END, f"Plan {i}")

if __name__ == "__main__":
    root = tk.Tk()
    app = PlanningChart(root)
    root.mainloop()

