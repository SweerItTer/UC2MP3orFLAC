import os
import re

import aiohttp
import asyncio
import tkinter as tk
from tkinter import ttk

class Rename:
    @staticmethod
    async def get_song_info(song_id, row_name):
        try:
            url = 'http://music.163.com/api/song/detail/?id={0}&ids=%5B{1}%5D'.format(song_id, song_id)
            headers = {'Accept': 'application/json'}
            async with aiohttp.ClientSession(headers=headers) as session:
                async with session.get(url) as response:
                    jsons = await response.json()
                    song_name = jsons['songs'][0]['name']
                    singer = jsons['songs'][0]['artists'][0]['name']
                    return song_name + "-" + singer
        except Exception as e:
            print("Warning Song Info", Warning(str(e)))
            return row_name

    @staticmethod
    def sanitize_filename(filename):
        # Remove characters that are not allowed in Windows file names
        return re.sub(r'[\\/:*?"<>|]', '_', filename)

    @staticmethod
    async def process_files(screen_width=2520, screen_height=1680):
        transform_dir = ".\Transform"
        dirs = os.listdir(transform_dir)

        # Create the main Tkinter window
        root = tk.Tk()
        root.withdraw()  # Hide the main window

        progress_bar_var = tk.IntVar()
        # Create progress window after the main window is created
        progress_window = tk.Toplevel()
        progress_window.title("转换进度")
        progress_bar_length = 400
        progress_bar = ttk.Progressbar(progress_window, variable=progress_bar_var, maximum=len(dirs),
                                       length=progress_bar_length)
        progress_bar.pack(padx=20, pady=20)

        x_coordinate = (screen_width - progress_bar_length) / 2
        y_coordinate = (screen_height - progress_bar.winfo_reqheight()) / 2
        progress_window.geometry("+%d+%d" % (x_coordinate, y_coordinate))

        for old_filename in dirs:
            old_path = os.path.join(transform_dir, old_filename)
            song_id = os.path.splitext(old_filename)[0].split('-')[0]
            # 判断song_id是否为数字
            if not song_id.isdigit():
                # 如果不是数字，直接跳过并更新进度条
                progress_bar_var.set(progress_bar_var.get() + 1)
                progress_window.update()
                continue
            new_name = await Rename.get_song_info(song_id, old_filename)
            new_filename = Rename.sanitize_filename(new_name) + os.path.splitext(old_filename)[-1]
            new_path = os.path.join(transform_dir, new_filename)

            # Introduce a small delay (e.g., 1 second) between iterations
            await asyncio.sleep(1)

            if old_filename != new_filename and not os.path.exists(new_path):
                try:
                    os.rename(old_path, new_path)
                    progress_bar_var.set(progress_bar_var.get() + 1)
                except PermissionError as pe:
                    print(f"PermissionError: {pe}. Skipping file: {old_path}")
            else:
                os.remove(old_path)
                progress_bar_var.set(progress_bar_var.get() + 1)

            # 更新Tkinter主循环以刷新GUI
            progress_window.update()
            # 转换完成后关闭进度窗口
        progress_window.destroy()
        root.destroy()  # Destroy the main window


if __name__ == "__main__":
    asyncio.run(Rename.process_files())
