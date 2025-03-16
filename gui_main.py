import tkinter as tk
from tkinter import ttk, filedialog
import sv_ttk
from app import VODProcessor
from dotenv import load_dotenv, set_key
import os

load_dotenv()  # Load environment variables


# Utility to save value to .env file
def save_to_env(key, value):
    set_key(".env", key, value)


# Browse file for Firefox path
def browse_firefox_path():
    filepath = filedialog.askopenfilename(
        filetypes=[("Executable files", "*.exe"), ("All files", "*.*")]
    )
    firefox_path_entry.delete(0, tk.END)
    firefox_path_entry.insert(0, filepath)
    save_to_env("firefox_path", filepath)  # Save browser path


# Ensure values are retrieved and saved
def run_vodprocessor():
    channel = channel_entry.get()
    firefox_path = firefox_path_entry.get()
    params = {
        "delete_video_when_done": delete_video_var.get(),
        "open_log_when_done": open_log_var.get(),
        "monitor": monitor_var.get(),
        "headless_browser": headless_var.get(),
    }
    vod_processor = VODProcessor(channel=channel, firefox_path=firefox_path, **params)
    vod_processor.run()

    # Save inputs to environment
    save_to_env("channel", channel)
    for key, value in params.items():
        save_to_env(key, str(value))


def create_gui():
    root = tk.Tk()
    root.title("VOD Processor Config")
    root.geometry("500x500")
    sv_ttk.set_theme("dark")

    global channel_entry, firefox_path_entry, delete_video_var, open_log_var, monitor_var, headless_var

    # Email and Password
    email_label = ttk.Label(root, text="Rumble Archive Email")
    email_label.pack(pady=5)
    email_entry = ttk.Entry(root)
    email_entry.insert(0, os.getenv("email", ""))  # Load saved value
    email_entry.pack(fill=tk.X, padx=10)
    save_to_env("email", email_entry.get())  # Save email immediately

    password_label = ttk.Label(root, text="Rumble Archive Password")
    password_label.pack(pady=5)
    password_entry = ttk.Entry(root, show="*")  # Hide password input
    password_entry.insert(0, os.getenv("password", ""))  # Load saved password
    password_entry.pack(fill=tk.X, padx=10)
    save_to_env("password", password_entry.get())  # Save password immediately

    # Channel
    channel_label = ttk.Label(root, text="Kick Channel")
    channel_label.pack(pady=5)
    channel_entry = ttk.Entry(root)
    channel_entry.insert(0, os.getenv("channel", ""))  # Load saved channel
    channel_entry.pack(fill=tk.X, padx=10)

    # Firefox path
    firefox_path_label = ttk.Label(root, text="Firefox Executable Path")
    firefox_path_label.pack(pady=5)
    firefox_path_frame = ttk.Frame(root)
    firefox_path_frame.pack(fill=tk.X, padx=10)
    firefox_path_entry = ttk.Entry(firefox_path_frame)
    firefox_path_entry.insert(0, os.getenv("firefox_path", ""))  # Load saved path
    firefox_path_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
    browse_button = ttk.Button(
        firefox_path_frame, text="Browse", command=browse_firefox_path
    )
    browse_button.pack(side=tk.RIGHT)

    # Options
    delete_video_var = tk.BooleanVar(
        value=os.getenv("delete_video_when_done", False) == "True"
    )
    delete_video_check = ttk.Checkbutton(
        root, text="Delete video when done", variable=delete_video_var
    )
    delete_video_check.pack(pady=5)

    open_log_var = tk.BooleanVar(value=os.getenv("open_log_when_done", True) == "True")
    open_log_check = ttk.Checkbutton(
        root, text="Open log when done", variable=open_log_var
    )
    open_log_check.pack(pady=5)

    monitor_var = tk.BooleanVar(value=os.getenv("monitor", True) == "True")
    monitor_check = ttk.Checkbutton(
        root, text="Monitor directory", variable=monitor_var
    )
    monitor_check.pack(pady=5)

    headless_var = tk.BooleanVar(value=os.getenv("headless_browser", False) == "True")
    headless_check = ttk.Checkbutton(
        root, text="Use headless browser", variable=headless_var
    )
    headless_check.pack(pady=5)

    # Start button
    start_button = ttk.Button(root, text="Run VOD Processor (Download Latest, Transcribe, Archive)", command=run_vodprocessor)
    start_button.pack(pady=20)

    root.mainloop()


if __name__ == "__main__":
    create_gui()
