import tkinter as tk

def delete_last_character():
    selected_index = listbox.curselection()
    if selected_index:
        # Get the text of the selected item
        current_text = listbox.get(selected_index)

        # Check if the text has at least one character
        if current_text:
            # Remove the last character
            modified_text = current_text[:-1]

            # Delete the current item
            listbox.delete(selected_index)

            # Insert the modified text back to the listbox
            listbox.insert(selected_index, modified_text)

# Create the main window
root = tk.Tk()

# Create a Listbox
listbox = tk.Listbox(root)
listbox.pack()

# Insert some items for demonstration
listbox.insert(tk.END, "Item 1")
listbox.insert(tk.END, "Item 2")
listbox.insert(tk.END, "Item 3")

# Create a button to delete the last character
delete_button = tk.Button(root, text="Delete Last Character", command=delete_last_character)
delete_button.pack()

# Run the Tkinter main loop
root.mainloop()
