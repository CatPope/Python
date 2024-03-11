import tkinter as tk

root = tk.Tk()

frame = tk.Frame(root)
frame.pack(expand=True, fill="both")  # Frame이 부모 위젯의 크기에 따라 확장되도록 설정

listbox = tk.Listbox(frame)
listbox.pack(expand=True, fill="both")  # Listbox가 Frame 내에서 가로와 세로로 채워지도록 설정

# Listbox에 아이템 추가
for i in range(10):
    listbox.insert(tk.END, f"Item {i}")

root.mainloop()
