下面是关于程序的一些说明：

程序目的： 这个程序是一个用于将`.uc`音频文件转换为`.mp3`或`.flac`格式的工具。它利用并发处理（`concurrent.futures.ProcessPoolExecutor`）来提高转换效率，并提供一个基本的Tkinter GUI界面。

程序结构：

1. 主要功能函数：
    - `save(output_file_path, audio_contents)`: 保存转换后的音频内容到新文件。
    - `log(contents)`: 记录带有时间戳的转换日志。
    - `transform(input_file_path, output_file_path)`: 对音频文件进行转换并保存为相应格式。
    - `process_files(path, progress_bar_var)`: 并发处理音频文件转换，显示转换进度的Tkinter GUI窗口。
    - `remove_source_files(path, files)`: 在用户确认后删除源文件。
    - `ask_confirmation()`: 询问用户是否确认删除源文件。

2. Tkinter GUI相关函数：
    - `select_folder()`: 打开文件夹选择对话框，开始处理所选文件夹中的音频文件。
    - `create_gui()`: 创建主Tkinter GUI界面，包括一个标签和一个选择文件夹的按钮。

3. 全局变量：
    - `root`: Tkinter主窗口。
    - `screen_width`, `screen_height`: 屏幕宽度和高度。

使用说明：
1. 运行程序后，点击“Select Folder”按钮选择包含`.uc`文件的文件夹。
2. 转换进度将以Tkinter GUI的形式显示在新窗口中。
3. 完成后，询问用户是否删除源文件。

注意事项：
- 如果进度条不更新，请确保在主循环中调用`root.update_idletasks()`，以确保Tkinter界面更新。

这个程序是一个简单的音频文件批量转换工具，用户可以通过界面方便地选择文件夹和控制转换的过程。
_________________________________________________________________________________________________________
作者:SweerItTer 
(小菜鸟,纯找乐子)
_________________________________________________________________________________________________________

Here's an English version of the explanation the program:

Program Purpose:
This program is a tool designed to convert `.uc` audio files to either `.mp3` or `.flac` formats. It utilizes concurrent processing (`concurrent.futures.ProcessPoolExecutor`) to improve conversion efficiency and provides a basic Tkinter GUI interface.

Program Structure:

1. Main Functional Functions:
    - `save(output_file_path, audio_contents)`: Saves the converted audio content to a new file.
    - `log(contents)`: Records conversion logs with timestamps.
    - `transform(input_file_path, output_file_path)`: Converts audio files and saves them in the corresponding format.
    - `process_files(path, progress_bar_var)`: Concurrently processes audio file conversions, displaying progress through a Tkinter GUI window.
    - `remove_source_files(path, files)`: Deletes source files after user confirmation.
    - `ask_confirmation()`: Asks the user for confirmation before deleting source files.

2. Tkinter GUI-related Functions:
    - `select_folder()`: Opens a folder selection dialog, initiating the processing of audio files in the selected folder.
    - `create_gui()`: Creates the main Tkinter GUI interface, consisting of a label and a button to select a folder.

3. Global Variables:
    - `root`: Tkinter main window.
    - `screen_width`, `screen_height`: Screen width and height.

Usage Instructions:
1. Run the program and click the "Select Folder" button to choose a folder containing `.uc` files.
2. The conversion progress will be displayed in a Tkinter GUI window.
3. After completion, the user will be prompted to confirm the deletion of the source files.

Notes:
- If the progress bar does not update, make sure to call `root.update_idletasks()` within the main loop to ensure Tkinter interface updates.

This program serves as a straightforward batch audio file conversion tool, allowing users to easily select folders and control the conversion process through the interface.

__________________________

Creator SweerItTer 