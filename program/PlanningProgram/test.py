import tkinter as tk
from tkinter import filedialog

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("File Contents to Listbox")

        self.listbox = tk.Listbox(root, width=50, height=10)
        self.listbox.pack()

        load_button = tk.Button(root, text="Load File", command=self.load_file)
        load_button.pack()

    def load_file(self):
        file_path = filedialog.askopenfilename(title="Select a file", filetypes=[("Text files", "*.txt")])
        
        if file_path:
            try:
                with open(file_path, 'r') as file:
                    content = file.readlines()
                
                # Clear existing items in the listbox
                self.listbox.delete(0, tk.END)

                # Insert lines from the file into the listbox
                for line in content:
                    self.listbox.insert(tk.END, line.strip())
            except Exception as e:
                tk.messagebox.showerror("Error", f"Error loading file: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
