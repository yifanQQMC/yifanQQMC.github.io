import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, simpledialog
import sys
from io import StringIO
#纯ai

class InputRequest(Exception):
    """自定义异常用于请求用户输入"""

    def __init__(self, prompt):
        self.prompt = prompt
        super().__init__(prompt)


def mock_input(prompt=""):
    """替换内置input函数，抛出特殊异常"""
    raise InputRequest(prompt)


def save_file():
    """保存文本框内容到文件"""
    content = text_box.get("1.0", "end-1c")
    if not content.strip():
        messagebox.showwarning("空内容", "文本框内容为空，无需保存")
        return

    file_path = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("文本文件", "*.txt"), ("Python文件", "*.py"), ("所有文件", "*.*")]
    )

    if file_path:
        try:
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(content)
            messagebox.showinfo("保存成功", f"文件已保存到:\n{file_path}")
        except Exception as e:
            messagebox.showerror("保存失败", f"保存文件时出错:\n{str(e)}")


def open_file():
    """打开本地文件并将内容加载到文本框中"""
    file_path = filedialog.askopenfilename(
        filetypes=[("文本文件", "*.txt"), ("Python文件", "*.py"), ("所有文件", "*.*")]
    )

    if file_path:
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()
                text_box.delete("1.0", tk.END)  # 清空当前内容
                text_box.insert(tk.END, content)
            root.title(f"Python代码编辑器 - {file_path}")  # 更新窗口标题显示当前文件路径
        except Exception as e:
            messagebox.showerror("打开失败", f"打开文件时出错:\n{str(e)}")


def run_code():
    """运行文本框中的Python代码，处理input调用"""
    content = text_box.get("1.0", "end-1c")
    if not content.strip():
        messagebox.showwarning("空内容", "没有可执行的代码")
        return

    # 创建输出窗口
    output_window = tk.Toplevel(root)
    output_window.title("代码运行结果")
    output_window.geometry("800x600")

    output_text = scrolledtext.ScrolledText(
        output_window,
        wrap=tk.WORD,
        font=("微软雅黑", 12),
        padx=10,
        pady=10
    )
    output_text.pack(fill=tk.BOTH, expand=True)

    # 重定向标准输出
    old_stdout = sys.stdout
    sys.stdout = StringIO()

    # 替换内置input函数
    builtins = __import__('builtins')
    original_input = builtins.input
    builtins.input = mock_input

    try:
        # 执行代码
        exec(content, {'__builtins__': builtins})

        # 获取输出内容
        output = sys.stdout.getvalue()
        output_text.insert(tk.END, output)

    except InputRequest as e:
        # 处理input请求
        output_text.insert(tk.END, e.prompt)
        output_text.see(tk.END)  # 滚动到末尾
        output_window.update()  # 更新窗口

        # 弹出输入对话框
        user_input = simpledialog.askstring("输入请求", e.prompt, parent=output_window)

        if user_input is not None:
            # 模拟input返回值
            sys.stdout.write(user_input + "\n")
            output_text.insert(tk.END, user_input + "\n")
        else:
            output_text.insert(tk.END, "\n\n")

    except Exception as e:
        output_text.insert(tk.END, f"运行时错误:\n{str(e)}\n")

    finally:
        # 恢复原始设置
        sys.stdout = old_stdout
        builtins.input = original_input
        output_text.config(state=tk.DISABLED)


def close_app():
    """关闭应用程序"""
    if messagebox.askyesno("退出", "确定要退出程序吗？"):
        root.destroy()


# 创建主窗口
root = tk.Tk()
root.title("Python代码编辑器")
root.geometry("1600x900")

# 颜色定义
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

# 主文本框区域
text_frame = tk.Frame(root, bg=COLORS["bg"])
text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(50, 20))  # 顶部留出按钮空间

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

# 按钮区域 - 使用place精确定位在顶部
button_frame = tk.Frame(root, bg=COLORS["bg"])
button_frame.place(x=6, y=0, height=40)  # 固定高度

# 按钮公共样式
button_style = {
    "fg": COLORS["text_fg"],
    "font": ("微软雅黑", 12),
    "padx": 15,
    "borderwidth": 2,
    "relief": tk.RAISED
}

# 打开按钮
open_button = tk.Button(
    button_frame,
    text="打开文件",
    command=open_file,
    bg=COLORS["open_btn"],
    **button_style
)
open_button.pack(side=tk.LEFT, padx=5)

# 保存按钮
save_button = tk.Button(
    button_frame,
    text="保存文件",
    command=save_file,
    bg=COLORS["save_btn"],
    **button_style
)
save_button.pack(side=tk.LEFT, padx=5)

# 运行按钮
run_button = tk.Button(
    button_frame,
    text="运行代码",
    command=run_code,
    bg=COLORS["run_btn"],
    **button_style
)
run_button.pack(side=tk.LEFT, padx=5)

# 关闭按钮
close_button = tk.Button(
    button_frame,
    text="关闭程序",
    command=close_app,
    bg=COLORS["close_btn"],
    **button_style
)
close_button.pack(side=tk.LEFT, padx=5)

root.mainloop()