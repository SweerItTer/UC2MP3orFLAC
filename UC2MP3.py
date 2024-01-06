# uc cache path:  C:\Users\Administrator_\AppData\Local\NetEase\CloudMusic\Cache\Cache
# 原理 ^= 0xa3 文件数据异或'163'

import os
from concurrent.futures import ProcessPoolExecutor, as_completed
from colorama import Fore, Style  # 引入 colorama 中的颜色常量
from tqdm import tqdm


def transform(input_file_path, output_file_path):
    Mp3_contents = None

    with open(input_file_path, "rb") as f:
        Mp3_contents = bytearray(f.read())
        for i, byte in enumerate(Mp3_contents):
            byte ^= 0xa3
            Mp3_contents[i] = byte
    # print(input_file_path)
    with open(output_file_path, "wb") as wf:
        wf.write(bytes(Mp3_contents))


if __name__ == "__main__":
    path = r'C:\Users\Administrator_\AppData\Local\NetEase\CloudMusic\Cache\Cache'

    files = os.listdir(path)
    files_new = []

    for file in files:
        if os.path.splitext(file)[-1] == '.uc':
            files_new.append(file)
        else:
            continue

    # 使用多线程处理
    recommended_thread_count = os.cpu_count()  # 获取 CPU 核心数
    with ProcessPoolExecutor(max_workers=recommended_thread_count) as executor:
        futures = {executor.submit(transform, os.path.join(path, file), os.path.join(file.split(".uc")[0] + ".mp3")): file for file in files_new}

        progress_bar = tqdm(total=len(futures), desc="Converting", unit="file")

        for future in as_completed(futures):
            # 更新进度条
            progress_bar.update(1)
            file = futures[future]
            try:
                future.result()  # 获取任务结果，如果任务失败，这里会抛出异常
            except Exception as e:
                with open('Log.log',"a") as l:
                    l.write(f"Error processing file {file}: {e}")
        # 关闭进度条
        progress_bar.close()

# 尝试删除C盘里的.uc文件，跳过正在被调用的文件
    for file in files_new:
        file_path = os.path.join(path, file)
        try:
            os.remove(file_path)
            print(f"Deleted: {file}")
        except PermissionError:
            print(f"Could not delete {Fore.RED}{file}{Style.RESET_ALL}. It is still in use. Skipping...")

    print("All tasks completed and .uc files deleted.")
