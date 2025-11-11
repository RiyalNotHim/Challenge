import tkinter as tk
from tkinter import ttk, messagebox, font, filedialog, scrolledtext
import json
import os
import shutil
import threading
import time
from datetime import datetime

# --- Configuration ---
CONFIG_FILE = os.path.join(os.path.dirname(__file__), '..', 'data', 'config.json')

# --- Main Application Class ---
class FileOrganizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("File Organizer Bot")
        self.root.geometry("700x500")

        self.extension_map = {}
        
        self.setup_styles()
        self.create_widgets()
        
        self.load_config()

    def setup_styles(self):
        """Configure the dark theme."""
        self.bg_color = "#2b2b2b"
        self.fg_color = "#e0e0e0"
        self.entry_bg = "#3c3c3c"
        self.button_bg = "#007acc"
        self.button_fg = "#ffffff"
        self.list_bg = "#333333"
        
        self.root.configure(bg=self.bg_color)
        
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TCombobox", fieldbackground=self.entry_bg, background=self.entry_bg, foreground=self.fg_color, darkcolor=self.entry_bg, lightcolor=self.entry_bg, selectbackground=self.entry_bg, selectforeground=self.fg_color)
        style.map('TCombobox', fieldbackground=[('readonly', self.entry_bg)])
        style.configure("TButton", background=self.button_bg, foreground=self.button_fg, font=("Arial", 10, "bold"), borderwidth=0)
        style.map("TButton", background=[('active', '#005f9e')])
        style.configure("TFrame", background=self.bg_color)
        style.configure("TLabel", background=self.bg_color, foreground=self.fg_color, font=("Arial", 10))
        style.configure("TEntry", fieldbackground=self.entry_bg, foreground=self.fg_color, insertbackground=self.fg_color)
        style.configure("Header.TLabel", font=("Arial", 14, "bold"))

    def create_widgets(self):
        """Create all GUI elements."""
        main_frame = ttk.Frame(self.root, padding="15")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # --- Top Controls Frame ---
        controls_frame = ttk.Frame(main_frame)
        controls_frame.pack(fill="x", pady=(0, 10))

        ttk.Label(controls_frame, text="Target Directory:", font=("Arial", 11, "bold")).pack(anchor="w")

        # Directory Selection
        dir_frame = ttk.Frame(controls_frame)
        dir_frame.pack(fill="x", pady=5)
        
        self.dir_entry = ttk.Entry(dir_frame, width=70)
        self.dir_entry.pack(side=tk.LEFT, fill="x", expand=True, ipady=4)
        
        self.browse_button = ttk.Button(dir_frame, text="Browse", command=self.browse_directory)
        self.browse_button.pack(side=tk.LEFT, padx=(10, 0))

        # Sort Options
        options_frame = ttk.Frame(controls_frame)
        options_frame.pack(fill="x", pady=10)
        
        ttk.Label(options_frame, text="Sort Mode:").pack(side=tk.LEFT, anchor="w")
        
        self.sort_mode = ttk.Combobox(options_frame, values=[
            "Sort by Extension", 
            "Sort by Date (YYYY-MM-DD)",
            "Sort by Date (YYYY-MM)"
        ], state="readonly", width=30)
        self.sort_mode.pack(side=tk.LEFT, padx=10)
        self.sort_mode.current(0)
        
        self.start_button = ttk.Button(options_frame, text="Start Organizing", command=self.start_sort_thread)
        self.start_button.pack(side=tk.LEFT, padx=10, ipady=5)

        # --- Log Viewer ---
        log_frame = ttk.Frame(main_frame)
        log_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(log_frame, text="Log", font=("Arial", 11, "bold")).pack(anchor="w", pady=(5,2))
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=15, bg=self.list_bg, fg=self.fg_color, relief=tk.FLAT, state="disabled", font=("Courier New", 9))
        self.log_text.pack(fill="both", expand=True)

    def browse_directory(self):
        """Open a dialog to select a directory."""
        directory = filedialog.askdirectory()
        if directory:
            self.dir_entry.delete(0, tk.END)
            self.dir_entry.insert(0, directory)
            
    def log(self, message):
        """Inserts a message into the log text area (thread-safe)."""
        def _log_to_gui():
            self.log_text.config(state="normal")
            self.log_text.insert(tk.END, f"{message}\n")
            self.log_text.config(state="disabled")
            self.log_text.see(tk.END) # Auto-scroll
        # Schedule the GUI update on the main thread
        self.root.after(0, _log_to_gui)

    def load_config(self):
        """Loads extension mappings from config.json."""
        try:
            with open(CONFIG_FILE, 'r') as f:
                config = json.load(f)
                mappings = config.get("extension_mappings", {})
                
                # Reverse the map for faster lookup
                self.extension_map = {}
                for category, extensions in mappings.items():
                    for ext in extensions:
                        self.extension_map[ext.lower()] = category
            self.log(f"Successfully loaded {len(self.extension_map)} file type mappings from config.json")
        except FileNotFoundError:
            self.log(f"ERROR: config.json not found at {CONFIG_FILE}")
            messagebox.showerror("Error", "config.json not found. Please create it in the 'data' folder.")
        except json.JSONDecodeError:
            self.log(f"ERROR: Could not parse config.json. Check for syntax errors.")
            messagebox.showerror("Error", "Could not parse config.json. Check for syntax errors.")

    def start_sort_thread(self):
        """Starts the sorting process in a new thread to keep the GUI responsive."""
        target_dir = self.dir_entry.get()
        if not os.path.isdir(target_dir):
            messagebox.showwarning("Invalid Directory", "Please select a valid directory to organize.")
            return
            
        self.start_button.config(state="disabled", text="Organizing...")
        self.log("="*50)
        self.log(f"Starting organization for: {target_dir}")
        
        # Run the sorting in a separate thread
        sort_thread = threading.Thread(target=self.organize_files, daemon=True)
        sort_thread.start()

    def organize_files(self):
        """The main file organization logic."""
        target_dir = self.dir_entry.get()
        mode = self.sort_mode.get()
        
        try:
            if mode == "Sort by Extension":
                self.sort_by_extension(target_dir)
            elif mode == "Sort by Date (YYYY-MM-DD)":
                self.sort_by_date(target_dir, "%Y-%m-%d")
            elif mode == "Sort by Date (YYYY-MM)":
                self.sort_by_date(target_dir, "%Y-%m")
            
            self.log("Organization complete!")
            
        except Exception as e:
            self.log(f"An error occurred: {e}")
            messagebox.showerror("Error", f"An error occurred during organization: {e}")
        
        # Re-enable the button (must be run on main thread via 'after')
        self.root.after(0, lambda: self.start_button.config(state="normal", text="Start Organizing"))

    def sort_by_extension(self, target_dir):
        """Sorts files into folders based on their extension."""
        if not self.extension_map:
            self.log("Error: Extension map is empty. Cannot sort.")
            return
            
        file_count = 0
        for filename in os.listdir(target_dir):
            src_path = os.path.join(target_dir, filename)
            
            # Skip directories
            if os.path.isdir(src_path):
                continue
                
            _, ext = os.path.splitext(filename)
            ext = ext.lower()
            
            # Determine target folder
            target_folder_name = self.extension_map.get(ext, "Other")
            dest_folder = os.path.join(target_dir, target_folder_name)
            
            # Create destination folder if it doesn't exist
            os.makedirs(dest_folder, exist_ok=True)
            
            dest_path = os.path.join(dest_folder, filename)
            
            # Move the file
            try:
                shutil.move(src_path, dest_path)
                self.log(f"Moved: {filename}  ->  {target_folder_name}/")
                file_count += 1
            except Exception as e:
                self.log(f"Error moving {filename}: {e}")
        
        self.log(f"Successfully sorted {file_count} files by extension.")

    def sort_by_date(self, target_dir, date_format):
        """Sorts files into folders based on modification date."""
        file_count = 0
        for filename in os.listdir(target_dir):
            src_path = os.path.join(target_dir, filename)
            
            # Skip directories
            if os.path.isdir(src_path):
                continue
            
            try:
                # Get modification time
                m_time = os.path.getmtime(src_path)
                date_str = datetime.fromtimestamp(m_time).strftime(date_format)
                
                # Determine target folder
                dest_folder = os.path.join(target_dir, date_str)
                
                # Create destination folder if it doesn't exist
                os.makedirs(dest_folder, exist_ok=True)
                
                dest_path = os.path.join(dest_folder, filename)
                
                # Move the file
                shutil.move(src_path, dest_path)
                self.log(f"Moved: {filename}  ->  {date_str}/")
                file_count += 1
            except Exception as e:
                self.log(f"Error processing {filename}: {e}")
                
        self.log(f"Successfully sorted {file_count} files by date ({date_format}).")

# --- Run the Application ---
if __name__ == "__main__":
    if not os.path.exists(CONFIG_FILE):
        messagebox.showerror("Config Error", f"Fatal Error: 'data/config.json' not found.\n\nPlease create it before running the app.")
    else:
        root = tk.Tk()
        app = FileOrganizerApp(root)
        root.mainloop()