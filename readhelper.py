import time
import tkinter as tk
from tkinter import messagebox, scrolledtext, colorchooser, filedialog

file_path = 'd:/thinkagain/我在精神病院学斩神.txt'
progress_file = 'd:/thinkagain/progress.txt'

def read_file(start_line=0):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            for line_number, line in enumerate(lines[start_line:], start=start_line):
                text_area.insert(tk.END, line.strip() + '\n')
                text_area.see(tk.END)  # 自动滚动到最后一行
                root.update()
                time.sleep(speed_scale.get())  # 每行打印间隔由滑块控制
                current_line.set(line_number + 1)
    except FileNotFoundError:
        text_area.insert(tk.END, f"文件 {file_path} 未找到。\n")
    except Exception as e:
        text_area.insert(tk.END, f"读取文件时出错: {e}\n")

def save_progress():
    try:
        with open(progress_file, 'w', encoding='utf-8') as pf:
            pf.write(str(current_line.get()))
        text_area.insert(tk.END, "阅读进度已保存。\n")
    except Exception as e:
        text_area.insert(tk.END, f"保存进度时出错: {e}\n")

def ask_start_point():
    start_line = 0
    if messagebox.askyesno("开始阅读", "是否从上次保存的进度开始阅读？"):
        try:
            with open(progress_file, 'r', encoding='utf-8') as pf:
                start_line = int(pf.read().strip())
        except FileNotFoundError:
            pass
        except Exception as e:
            text_area.insert(tk.END, f"读取进度文件时出错: {e}\n")
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
        text_area.insert(tk.END, f"已选择文件: {file_path}\n")

# 创建主窗口
root = tk.Tk()
root.title("逐行打印文件内容")
root.attributes('-fullscreen', True)  # 设置窗口全屏

# 绑定 Esc 键退出
root.bind("<Escape>", lambda e: root.quit())

# 创建左侧阅读区
left_frame = tk.Frame(root, width=root.winfo_screenwidth() // 2, height=root.winfo_screenheight())
left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# 创建右侧控制区
right_frame = tk.Frame(root, width=root.winfo_screenwidth() // 2, height=root.winfo_screenheight())
right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

# 创建一个滚动文本区域
text_area = scrolledtext.ScrolledText(left_frame, wrap=tk.WORD, font=("Helvetica", 12))
text_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

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

# 创建一个按钮来退出程序
exit_button = tk.Button(right_frame, text="退出", command=root.quit)
exit_button.pack(pady=10)

# 运行主循环
root.mainloop()