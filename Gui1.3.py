import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from concurrent.futures import ProcessPoolExecutor, as_completed
from datetime import datetime

def save(output_file_path, audio_contents):
    """Save the transformed audio contents to a new file."""
    with open(output_file_path, 'wb') as f:
        f.write(audio_contents)

def log(contents):
    """Log information to a conversion log file with timestamp."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open('conversion.log', "a") as l:
        l.write(f"{timestamp} - {contents}\n")

def transform(input_file_path, output_file_path):
    """Transform the audio file and save it with the corresponding format."""
    audio_contents = bytearray()

    with open(input_file_path, "rb") as f:
        # Transform the audio contents by XOR-ing each byte with 0xa3
        audio_contents = bytearray(byte ^ 0xa3 for byte in f.read())

    # Detect the file header type (e.g., ID3, fLaC)
    file_header = audio_contents[:4].decode('utf-8', errors='ignore')

    try:
        # Save the transformed file with the corresponding format
        format_extension = ".mp3" if 'ID3' in file_header else ".flac" if 'fLaC' in file_header else None
        if format_extension:
            save(output_file_path + format_extension, audio_contents)
        else:
            log(f'Invalid file suffix for {output_file_path}')
    except Exception as e:
        print(e)

def process_files(path, progress_bar_var):
    """Process audio files in the specified path using concurrent processing."""
    dir_ = "Transform"
    os.makedirs(dir_, exist_ok=True)

    # List all files in the specified path
    files = [file for file in os.listdir(path) if os.path.splitext(file)[-1] == '.uc']

    # Determine the number of concurrent processes to use
    recommended_process_count = os.cpu_count()

    with ProcessPoolExecutor(max_workers=recommended_process_count) as executor:
        # Create a set to keep track of processed file names
        processed_files = set()

        # Create a dictionary of futures for each file conversion task
        futures = {
            executor.submit(transform, os.path.join(path, file), os.path.join(dir_, file.split(".uc")[0])):
                file for file in files if file not in processed_files
        }

        # Create a progress window to display the conversion progress
        progress_window = tk.Toplevel()
        progress_window.title("Conversion Progress")
        progress_bar_length = 400
        progress_bar = ttk.Progressbar(progress_window, variable=progress_bar_var, maximum=len(futures),
                                       length=progress_bar_length)
        progress_bar.pack(padx=20, pady=20)

        x_coordinate = (screen_width - progress_bar_length) / 2
        y_coordinate = (screen_height - progress_bar.winfo_reqheight()) / 2
        progress_window.geometry("+%d+%d" % (x_coordinate, y_coordinate))

        # Iterate through completed futures and update the progress bar
        for future in as_completed(futures):
            progress_bar_var.set(progress_bar_var.get() + 1)
            file = futures[future]
            try:
                future.result()
            except Exception as e:
                # Log any errors encountered during file processing
                log(f"Error processing file {file}: {e}\n")

            # Update Tkinter main loop to refresh GUI
            progress_window.update()

        # Close the progress window once the conversion is complete
        progress_window.destroy()

    # Ask for confirmation to delete the source files
    if ask_confirmation():
        remove_source_files(path, files)
    root.destroy()

def remove_source_files(path, files):
    """Remove the source files if user confirms."""
    for file in files:
        file_path = os.path.join(path, file)
        try:
            os.remove(file_path)
        except PermissionError:
            pass

def ask_confirmation():
    """Ask the user for confirmation to delete the source files."""
    answer = messagebox.askyesno("Confirmation", f"Do you want to delete the source files?")
    return answer

def select_folder():
    """Open a dialog to select the folder containing .uc files."""
    default_folder = r"C:\Users\Administrator_\AppData\Local\NetEase\CloudMusic\Cache\Cache"
    folder_path = filedialog.askdirectory(initialdir=default_folder)
    if folder_path:
        progress_bar_var = tk.IntVar()
        process_files(folder_path, progress_bar_var)

def create_gui():
    """Create the GUI with a label and button for selecting the folder."""
    global root
    global screen_width
    global screen_height
    root = tk.Tk()
    root.title("UC File Converter")

    # Get the screen width and height
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Calculate the X and Y coordinates to center the window
    x_coordinate = (screen_width - root.winfo_reqwidth()) / 2
    y_coordinate = (screen_height - root.winfo_reqheight()) / 2

    # Set the window position
    root.geometry("+%d+%d" % (x_coordinate, y_coordinate))

    # Create the GUI with a label and button for selecting the folder
    label = tk.Label(root, text="Select the folder containing .uc files:")
    label.pack(pady=10)

    button = tk.Button(root, text="Select Folder", command=select_folder)
    button.pack(pady=20)

    # Start the Tkinter main loop
    root.mainloop()

if __name__ == "__main__":
    create_gui()
