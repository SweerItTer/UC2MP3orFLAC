import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from concurrent.futures import ProcessPoolExecutor, as_completed
# 缓存的UC文件似乎不具备歌曲名字等信息,算了
"""
# from mutagen.easyid3 import EasyID3
# from mutagen.flac import FLAC

# def get_song_name(audio_file_path):
#     _, file_extension = os.path.splitext(audio_file_path)
#     if file_extension.lower() == '.mp3':
#         audio = EasyID3(audio_file_path)
#     elif file_extension.lower() == '.flac':
#         audio = FLAC(audio_file_path)
#     else:
#         # Add support for other formats as needed
#         pass
#     if 'title' in audio:
#         return audio['title'][0]
#     return None

# def rename(file_path):
#     # 获取文件路径和文件名
#     file_dir, file_name = os.path.split(file_path)
#     new_name = get_song_name(os.path.abspath(file_path))
#     # 构建新的文件路径
#     new_file_path = os.path.join(file_dir, new_name)
#     # 重命名文件
#     os.rename(file_path, new_file_path)
"""

def save(output_file_path, Audio_contents):
    with open(output_file_path, 'wb') as f:
        f.write(Audio_contents)

def Log(contents):
    with open('conversion.log', "a") as l:
        l.write(contents+"\n")

def transform(input_file_path, output_file_path):
    Audio_contents = None

    with open(input_file_path, "rb") as f:
        Audio_contents = bytearray(f.read())
        for i, byte in enumerate(Audio_contents):
            byte ^= 0xa3
            Audio_contents[i] = byte

        # Detect the file header type (e.g., ID3, fLaC)
    file_header = Audio_contents[:4].decode('utf-8', errors='ignore')
    # print(file_header)
    try:
        # Save the file with the corresponding format
        if 'ID3' in file_header:
            save(output_file_path + ".mp3", Audio_contents)
            # rename(output_file_path + ".mp3")
        elif 'fLaC' in file_header:
            save(output_file_path + ".flac", Audio_contents)
            # rename(output_file_path + ".flac")
        else:
            Log(f'文件 {output_file_path} 后缀无效')
    except Exception as e:
        # Log(f'{output_file_path} 重命名失败,或者转换失败')
        print(e)

def process_files(path, progress_bar_var):
    dir_ = "Transform"
    if not os.path.isdir(dir_):
        os.makedirs(dir_)

    files = os.listdir(path)
    files_new = [file for file in files if os.path.splitext(file)[-1] == '.uc']

    recommended_process_count = os.cpu_count()
    with ProcessPoolExecutor(max_workers=recommended_process_count) as executor:
        futures = {executor.submit(transform, os.path.join(path, file),
                                   os.path.join(dir_, file.split(".uc")[0])): file for file in files_new}

        # Use Toplevel for progress bar
        progress_window = tk.Toplevel()
        progress_window.title("转换进度")
        progress_bar = ttk.Progressbar(progress_window, variable=progress_bar_var, maximum=len(futures))
        progress_bar.pack(padx=20, pady=20)

        for future in as_completed(futures):
            progress_bar_var.set(progress_bar_var.get() + 1)
            file = futures[future]
            try:
                future.result()
            except Exception as e:
                Log(f"处理文件 {file} 时发生错误: {e}\n")

            # Update Tkinter main loop to refresh GUI
            progress_window.update()

        progress_window.destroy()

    if ask_confirmation():
        for file in files_new:
            file_path = os.path.join(path, file)
            try:
                os.remove(file_path)
            except PermissionError:
                pass
    root.destroy()


def ask_confirmation():
    answer = messagebox.askyesno("确认", f"是否要删除源文件?")
    return answer


def select_folder():
    default_folder = r"C:\Users\Administrator_\AppData\Local\NetEase\CloudMusic\Cache\Cache"
    folder_path = filedialog.askdirectory(initialdir=default_folder)
    if folder_path:
        progress_bar_var = tk.IntVar()
        process_files(folder_path, progress_bar_var)

def create_gui():
    global root
    root = tk.Tk()
    root.title("UC文件转换器")

    label = tk.Label(root, text="选择包含.uc文件的文件夹:")
    label.pack(pady=10)

    button = tk.Button(root, text="选择文件夹", command=select_folder)
    button.pack(pady=20)

    root.mainloop()


if __name__ == "__main__":
    create_gui()


