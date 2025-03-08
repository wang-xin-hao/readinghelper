import time
import tkinter as tk
from tkinter import messagebox, scrolledtext, colorchooser, filedialog

file_path = 'd:/thinkagain/我在精神病院学斩神.txt'
progress_file = 'd:/thinkagain/progress.txt'
is_paused = False  # 全局变量来控制是否暂停

def read_file(start_line=0):
    global is_paused
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            for line_number, line in enumerate(lines[start_line:], start=start_line):
                while is_paused:
                    root.update()
                    time.sleep(0.1)  # 暂停时等待
                text_area.config(state=tk.NORMAL)
                text_area.insert(tk.END, line.strip() + '\n')
                text_area.config(state=tk.DISABLED)
                text_area.see(tk.END)  # 自动滚动到最后一行
                root.update()
                time.sleep(speed_scale.get())  # 每行打印间隔由滑块控制
                current_line.set(line_number + 1)
    except FileNotFoundError:
        text_area.config(state=tk.NORMAL)
        text_area.insert(tk.END, f"文件 {file_path} 未找到。\n")
        text_area.config(state=tk.DISABLED)
    except Exception as e:
        text_area.config(state=tk.NORMAL)
        text_area.insert(tk.END, f"读取文件时出错: {e}\n")
        text_area.config(state=tk.DISABLED)

def save_progress():
    try:
        with open(progress_file, 'w', encoding='utf-8') as pf:
            pf.write(str(current_line.get()))
        text_area.config(state=tk.NORMAL)
        text_area.insert(tk.END, "阅读进度已保存。\n")
        text_area.config(state=tk.DISABLED)
    except Exception as e:
        text_area.config(state=tk.NORMAL)
        text_area.insert(tk.END, f"保存进度时出错: {e}\n")
        text_area.config(state=tk.DISABLED)

def ask_start_point():
    start_line = 0
    if messagebox.askyesno("开始阅读", "是否从上次保存的进度开始阅读？"):
        try:
            with open(progress_file, 'r', encoding='utf-8') as pf:
                start_line = int(pf.read().strip())
        except FileNotFoundError:
            pass
        except Exception as e:
            text_area.config(state=tk.NORMAL)
            text_area.insert(tk.END, f"读取进度文件时出错: {e}\n")
            text_area.config(state=tk.DISABLED)
    read_file(start_line)

def choose_text_color():
    color = colorchooser.askcolor(title="选择阅读区颜色")[1]
    if color:
        text_area.config(bg=color)

def choose_ui_color():
    color = colorchooser.askcolor(title="选择UI界面颜色")[1]
    if color:
        right_frame.config(bg=color)
        for widget in right_frame.winfo_children():
            widget.config(bg=color)

def choose_file():
    global file_path
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if file_path:
        text_area.config(state=tk.NORMAL)
        text_area.insert(tk.END, f"已选择文件: {file_path}\n")
        text_area.config(state=tk.DISABLED)

def toggle_pause():
    global is_paused
    is_paused = not is_paused
    if is_paused:
        pause_button.config(text="继续")
    else:
        pause_button.config(text="暂停")

def on_text_click(event):
    index = text_area.index("@%s,%s" % (event.x, event.y))
    line_number = int(index.split(".")[0])
    read_file(line_number - 1)

def show_help():
    help_text = (
        "阅读助手使用说明：\n\n"
        "1. 选择文件：点击“选择文件”按钮，选择要阅读的文本文件。\n"
        "2. 开始阅读：点击“开始读取文件”按钮，从上次保存的进度或从头开始阅读。\n"
        "3. 保存进度：点击“保存阅读进度”按钮，保存当前阅读进度。\n"
        "4. 调整速度：使用滑块调整每行打印的间隔时间。\n"
        "5. 选择颜色：点击“选择阅读区颜色”或“选择UI界面颜色”按钮，选择阅读区或UI界面的颜色。\n"
        "6. 暂停/继续：点击“暂停”按钮暂停阅读，再次点击“继续”阅读。\n"
        "7. 选择段落：点击阅读区中的任意段落，从该段落开始阅读。\n"
        "8. 退出：直接关闭窗口即可退出程序。\n"
    )
    messagebox.showinfo("帮助", help_text)

# 创建主窗口
root = tk.Tk()
root.title("readinghelper")

# 创建左侧阅读区
left_frame = tk.Frame(root, width=root.winfo_screenwidth() // 2, height=root.winfo_screenheight())
left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# 创建右侧控制区
right_frame = tk.Frame(root, width=root.winfo_screenwidth() // 2, height=root.winfo_screenheight())
right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

# 创建一个滚动文本区域（只读）
text_area = scrolledtext.ScrolledText(left_frame, wrap=tk.WORD, font=("Helvetica", 12), state=tk.DISABLED)
text_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
text_area.bind("<Button-1>", on_text_click)  # 绑定鼠标左键点击事件

# 创建一个滑块来调整打印速度
speed_scale = tk.Scale(right_frame, from_=0.1, to=5.0, resolution=0.1, orient=tk.HORIZONTAL, label="打印速度 (秒)")
speed_scale.set(1)  # 默认值为 1 秒
speed_scale.pack(pady=10)

# 创建一个按钮来选择文件
file_button = tk.Button(right_frame, text="选择文件", command=choose_file)
file_button.pack(pady=10)

# 创建一个按钮来启动文件读取
start_button = tk.Button(right_frame, text="开始读取文件", command=ask_start_point)
start_button.pack(pady=10)

# 创建一个按钮来保存阅读进度
current_line = tk.IntVar(value=0)
save_button = tk.Button(right_frame, text="保存阅读进度", command=save_progress)
save_button.pack(pady=10)

# 创建一个按钮来选择阅读区颜色
text_color_button = tk.Button(right_frame, text="选择阅读区颜色", command=choose_text_color)
text_color_button.pack(pady=10)

# 创建一个按钮来选择UI界面颜色
ui_color_button = tk.Button(right_frame, text="选择UI界面颜色", command=choose_ui_color)
ui_color_button.pack(pady=10)

# 创建一个按钮来暂停和继续阅读
pause_button = tk.Button(right_frame, text="暂停", command=toggle_pause)
pause_button.pack(pady=10)

# 创建一个按钮来显示帮助信息
help_button = tk.Button(right_frame, text="帮助", command=show_help)
help_button.pack(pady=10)

# 运行主循环
root.mainloop()