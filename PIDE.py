# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, simpledialog
import sys
from io import StringIO

class InputRequest(Exception):
    def __init__(self, prompt):
        self.prompt = prompt
        super().__init__(prompt)

def mock_input(prompt=""):
    raise InputRequest(prompt)
def save_file():
    content = text_box.get("1.0", "end-1c")
    if not content.strip():
        messagebox.showwarning("Empty content","The text box content is empty and does not need to be saved")
        return
    file_path = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("text file", "*.txt"), ("Python file", "*.py"), ("all file", "*.*")]
    )
    if file_path:
        try:
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(content)
            messagebox.showinfo("Save successfully", f"The file has been saved to:\n{file_path}")
        except Exception as e:
            messagebox.showerror("Save failed", f"Error saving the file:\n{str(e)}")

def open_file():
    file_path = filedialog.askopenfilename(
        filetypes=[("text file", "*.txt"), ("Python file", "*.py"), ("all file", "*.*")]
    )
    if file_path:
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()
                text_box.delete("1.0", tk.END)
                text_box.insert(tk.END, content)
            root.title(f"Python Code editor - {file_path}")
        except Exception as e:
            messagebox.showerror("Save failed", f"Error saving the file:\n{str(e)}")

def run_code():
    content = text_box.get("1.0", "end-1c")
    if not content.strip():
        messagebox.showwarning("Empty content", "There is no executable code")
        return
    output_window = tk.Toplevel(root)
    output_window.title("Code run results")
    output_window.geometry("800x600")
    output_text = scrolledtext.ScrolledText(
        output_window,
        wrap=tk.WORD,
        font=("Microsoft YaHei", 12),
        padx=10,
        pady=10
    )
    output_text.pack(fill=tk.BOTH, expand=True)
    old_stdout = sys.stdout
    sys.stdout = StringIO()
    builtins = __import__('builtins')
    original_input = builtins.input
    builtins.input = mock_input
    try:
        exec(content, {'__builtins__': builtins})
        output = sys.stdout.getvalue()
        output_text.insert(tk.END, output)
    except InputRequest as e:
        output_text.insert(tk.END, e.prompt)
        output_text.see(tk.END)
        output_window.update()
        user_input = simpledialog.askstring("Enter the request", e.prompt, parent=output_window)
        if user_input is not None:
            sys.stdout.write(user_input + "\n")
            output_text.insert(tk.END, user_input + "\n")
        else:
            output_text.insert(tk.END, "\n\n")
    except Exception as e:
        output_text.insert(tk.END, f"Runtime error:\n{str(e)}\n")
    finally:
        sys.stdout = old_stdout
        builtins.input = original_input
        output_text.config(state=tk.DISABLED)

def close_app():
    if messagebox.askyesno("Exit", "Are you sure you want to opt out of the program?"):
        root.destroy()

root = tk.Tk()
root.title("Python Code editor")
root.geometry("1600x900")
COLORS = {
    "bg": "#888888",
    "text_bg": "#a1a1a1",
    "save_btn": "#505050",
    "run_btn": "#505050",
    "close_btn": "#505050",
    "open_btn": "#505050",
    "text_fg": "white"
}
root.configure(bg=COLORS["bg"])
text_frame = tk.Frame(root, bg=COLORS["bg"])
text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(50, 20))
scrollbar = tk.Scrollbar(text_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
text_box = tk.Text(
    text_frame,
    height=25,
    width=80,
    wrap=tk.WORD,
    yscrollcommand=scrollbar.set,
    font=("Consolas", 20),
    padx=10,
    pady=10,
    bg=COLORS["text_bg"],
    fg="black"
)
text_box.pack(fill=tk.BOTH, expand=True)
scrollbar.config(command=text_box.yview)
button_frame = tk.Frame(root, bg=COLORS["bg"])
button_frame.place(x=6, y=0, height=40)
button_style = {
    "fg": COLORS["text_fg"],
    "font": ("Microsoft YaHei", 12),
    "padx": 15,
    "borderwidth": 2,
    "relief": tk.RAISED
}
open_button = tk.Button(
    button_frame,
    text="Open the file",
    command=open_file,
    bg=COLORS["open_btn"],
    **button_style
)
open_button.pack(side=tk.LEFT, padx=5)
save_button = tk.Button(
    button_frame,
    text="Save the file",
    command=save_file,
    bg=COLORS["save_btn"],
    **button_style
)
save_button.pack(side=tk.LEFT, padx=5)
run_button = tk.Button(
    button_frame,
    text="Run the code",
    command=run_code,
    bg=COLORS["run_btn"],
    **button_style
)
run_button.pack(side=tk.LEFT, padx=5)
close_button = tk.Button(
    button_frame,
    text="Close the program",
    command=close_app,
    bg=COLORS["close_btn"],
    **button_style
)
close_button.pack(side=tk.LEFT, padx=5)
root.mainloop()
