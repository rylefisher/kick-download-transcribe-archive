import tkinter as tk
from tkinter import ttk, filedialog
import sv_ttk
import json
from main import VODProcessor

CONFIG_FILE = "config.json"


class VODGui:
    def __init__(self, root):
        self.root = root
        self.root.title("VOD Processor")

        self.load_config()

        # Frame for organizing widgets in columns
        self.frame = ttk.Frame(root)
        self.frame.pack(pady=20, padx=20)

        # Label and entry for Firefox path
        self.firefox_path_label = ttk.Label(self.frame, text="Firefox Path:")
        self.firefox_path_label.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)

        self.firefox_path_var = tk.StringVar(value=self.config.get("firefox_path", ""))
        self.firefox_path_entry = ttk.Entry(
            self.frame, textvariable=self.firefox_path_var, width=50
        )
        self.firefox_path_entry.grid(row=0, column=1, padx=5, pady=5)

        self.browse_button = ttk.Button(
            self.frame, text="Browse", command=self.browse_firefox_path
        )
        self.browse_button.grid(row=0, column=2, padx=5, pady=5)

        # Label and drop-down for Model Size
        self.model_label = ttk.Label(self.frame, text="Model Size:")
        self.model_label.grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)

        self.model_var = tk.StringVar(value=self.config.get("model_size", "base"))
        self.dropdown = ttk.Combobox(
            self.frame,
            textvariable=self.model_var,
            values=["tiny", "base", "medium", "large-v3"],
            width=48,
        )  # Match width with entry
        self.dropdown.grid(row=1, column=1, columnspan=2, padx=5, pady=5)

        # Button to trigger VOD processing
        self.process_button = ttk.Button(
            root, text="Process VOD", command=self.process_vod
        )
        self.process_button.pack(pady=20)

        sv_ttk.set_theme("dark")

    def browse_firefox_path(self):
        filename = filedialog.askopenfilename(
            title="Select Firefox Executable", filetypes=[("Executable Files", "*.exe")]
        )
        if filename:
            self.firefox_path_var.set(filename)

    def save_config(self):
        self.config["model_size"] = self.model_var.get()
        self.config["firefox_path"] = self.firefox_path_var.get()
        with open(CONFIG_FILE, "w") as config_file:
            json.dump(self.config, config_file)

    def load_config(self):
        try:
            with open(CONFIG_FILE, "r") as config_file:
                self.config = json.load(config_file)
        except FileNotFoundError:
            self.config = {}

    def process_vod(self):
        self.root.withdraw()  # Hide the GUI
        selected_model = self.model_var.get()
        firefox_path = self.firefox_path_var.get()

        if firefox_path:  # Ensure Firefox path is provided
            vod_processor = VODProcessor(
                channel="jstlk", firefox_path=firefox_path, model_size=selected_model
            )
            vod_processor.run()

        self.save_config()  # Save configuration after processing
        self.root.deiconify()  # Show the GUI again


if __name__ == "__main__":
    root = tk.Tk()
    app = VODGui(root)
    root.mainloop()
