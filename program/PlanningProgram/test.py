import tkinter as tk

def on_enter(event):
    entry_text = entry.get()
    print(entry_text)
    print(f"Enter key pressed. Entered text: {entry_text}")

root = tk.Tk()

entry = tk.Entry(root)
entry.pack()

# Entry 위젯에 엔터 키에 대한 이벤트 바인딩
entry.bind('<Return>', on_enter)

root.mainloop()
