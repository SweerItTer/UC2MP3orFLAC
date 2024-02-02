import asyncio
import os
from infochange import Rename
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from concurrent.futures import ProcessPoolExecutor, as_completed
from datetime import datetime

def log(contents):
    """向转换日志文件添加带有当前时间戳的信息。"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open('conversion.log', "a") as l:
        l.write(f"{timestamp} - {contents}\n")
def save(output_file_path, audio_contents):
    """将转换后的音频内容保存到新文件。"""
    with open(output_file_path, 'wb') as f:
        f.write(audio_contents)

def transform(input_file_path, output_file_path):
    """转换音频文件并根据文件头信息以相应格式保存。"""
    # audio_contents = None

    with open(input_file_path, "rb") as f:
        # 通过异或每个字节与0xa3来转换音频内容
        audio_contents = bytearray(byte ^ 0xa3 for byte in f.read())

    # 检测文件头部类型（例如ID3或fLaC）
    file_header = audio_contents[:4].decode('utf-8', errors='ignore')

    try:
        # 根据文件头类型以对应格式保存转换后的文件
        format_extension = ".mp3" if 'ID3' in file_header else ".flac" if 'fLaC' in file_header else None
        if format_extension:
            save(output_file_path + format_extension, audio_contents)
        else:
            log(f'{output_file_path} 文件后缀无效')
    except Exception as e:
        print(e)

def process_files(path, progress_bar_var):
    """在指定路径中并发处理音频文件，并显示转换进度。完成后询问是否删除源文件。"""
    dir_ = "Transform"
    os.makedirs(dir_, exist_ok=True)

    # 列出指定路径下所有扩展名为.uc的文件
    files = [file for file in os.listdir(path) if os.path.splitext(file)[-1] == '.uc']

    # 确定并发进程数
    recommended_process_count = os.cpu_count()

    with ProcessPoolExecutor(max_workers=recommended_process_count) as executor:
        # 创建一个集合存储已处理的文件名
        processed_files = set()

        # 创建一个字典，键为Future对象，值为待转换的文件名
        futures = {
            executor.submit(transform, os.path.join(path, file), os.path.join(dir_, file.split(".uc")[0])):
                file for file in files if file not in processed_files
        }

        # 创建进度窗口及进度条
        progress_window = tk.Toplevel()
        progress_window.title("转换进度")
        progress_bar_length = 400
        progress_bar = ttk.Progressbar(progress_window, variable=progress_bar_var, maximum=len(futures),
                                       length=progress_bar_length)
        progress_bar.pack(padx=20, pady=20)

        x_coordinate = (screen_width - progress_bar_length) / 2
        y_coordinate = (screen_height - progress_bar.winfo_reqheight()) / 2
        progress_window.geometry("+%d+%d" % (x_coordinate, y_coordinate))

        # 遍历已完成的任务并更新进度条
        for future in as_completed(futures):
            progress_bar_var.set(progress_bar_var.get() + 1)
            file = futures[future]
            try:
                future.result()
            except Exception as e:
                # 记录处理文件时遇到的任何错误
                log(f"处理文件 {file} 时出错: {e}\n")

            # 更新Tkinter主循环以刷新GUI
            progress_window.update()

        # 转换完成后关闭进度窗口
        progress_window.destroy()

        asyncio.run(Rename.process_files(screen_width=screen_width, screen_height=screen_height))

    # 如果用户确认，则删除源文件
    if ask_confirmation():
        remove_source_files(path, files)
    root.destroy()
    # asyncio.run(Rename.process_files(screen_width=screen_width, screen_height=screen_height))

def remove_source_files(path, files):
    """如果用户确认，删除指定路径和列表中的源文件。"""
    for file in files:
        file_path = os.path.join(path, file)
        try:
            os.remove(file_path)
        except PermissionError:
            pass

def ask_confirmation():
    """弹窗询问用户是否要删除源文件，返回用户的选择结果。"""
    answer = messagebox.askyesno("确认", "您是否要删除源文件?")
    return answer

def select_folder():
    """打开文件对话框让用户选择包含UC文件的文件夹，然后开始转换过程。"""
    default_folder = r"C:\Users\Administrator_\AppData\Local\NetEase\CloudMusic\Cache\Cache"
    folder_path = filedialog.askdirectory(initialdir=default_folder)
    if folder_path:
        progress_bar_var = tk.IntVar()
        process_files(folder_path, progress_bar_var)

def create_gui():
    """创建具有标签和按钮的GUI界面，用于选择包含UC文件的文件夹。"""
    global root
    global screen_width
    global screen_height
    root = tk.Tk()
    root.title("UC文件转换器")

    # 获取屏幕宽度和高度
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # 计算窗口居中所需的坐标
    x_coordinate = (screen_width - root.winfo_reqwidth()) / 2
    y_coordinate = (screen_height - root.winfo_reqheight()) / 2

    # 设置窗口位置
    root.geometry("+%d+%d" % (x_coordinate, y_coordinate))

    # 创建GUI元素：标签和按钮
    label = tk.Label(root, text="请选择包含.UC文件的文件夹:")
    label.pack(pady=10)

    button = tk.Button(root, text="选择文件夹", command=select_folder)
    button.pack(pady=20)

    # 启动Tkinter主循环
    root.mainloop()

if __name__ == "__main__":
    create_gui()
