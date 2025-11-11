import tkinter as tk
from tkinter import ttk, messagebox, font, simpledialog, scrolledtext
import json
import os
import threading
import time
from datetime import datetime
import subprocess
import queue

# --- Configuration ---
DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
TASKS_FILE = os.path.join(DATA_DIR, 'tasks.json')

# --- Helper Functions ---
def ensure_files():
    """Ensure data directory and tasks.json exist."""
    os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, 'w') as f:
            json.dump([], f)

# --- Main Application Class ---
class TaskAutomatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Task Automator")
        self.root.geometry("800x600")

        self.tasks = []
        self.last_run_times = {} # For interval tasks
        self.log_queue = queue.Queue()

        self.setup_styles()
        self.create_widgets()

        self.load_tasks()
        self.start_scheduler()
        self.poll_log_queue()

    def setup_styles(self):
        """Configure the 'attractive' dark theme."""
        self.bg_color = "#2b2b2b"
        self.fg_color = "#e0e0e0"
        self.entry_bg = "#3c3c3c"
        self.button_bg = "#007acc"
        self.button_fg = "#ffffff"
        self.list_bg = "#333333"
        
        self.root.configure(bg=self.bg_color)
        
        # Style for TTK widgets (Combobox, etc.)
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TCombobox", fieldbackground=self.entry_bg, background=self.entry_bg, foreground=self.fg_color, darkcolor=self.entry_bg, lightcolor=self.entry_bg, selectbackground=self.entry_bg, selectforeground=self.fg_color)
        style.map('TCombobox', fieldbackground=[('readonly', self.entry_bg)])
        style.configure("TButton", background=self.button_bg, foreground=self.button_fg, font=("Arial", 10, "bold"), borderwidth=0)
        style.map("TButton", background=[('active', '#005f9e')])
        style.configure("TFrame", background=self.bg_color)
        style.configure("TLabel", background=self.bg_color, foreground=self.fg_color, font=("Arial", 10))
        style.configure("TEntry", fieldbackground=self.entry_bg, foreground=self.fg_color, insertbackground=self.fg_color)

    def create_widgets(self):
        """Create all GUI elements."""
        
        # --- Main layout frames ---
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Paned window to split controls and task list
        paned_window = tk.PanedWindow(main_frame, orient=tk.HORIZONTAL, sashrelief=tk.RAISED, bg=self.bg_color)
        paned_window.pack(fill=tk.BOTH, expand=True, pady=5)

        controls_frame = ttk.Frame(paned_window, padding="10", width=300)
        list_frame = ttk.Frame(paned_window, padding="10")
        paned_window.add(controls_frame, stretch="never")
        paned_window.add(list_frame, stretch="always")

        # --- Left Side: Controls ---
        ttk.Label(controls_frame, text="Add New Task", font=("Arial", 14, "bold")).pack(pady=(0, 10), anchor="w")
        
        # Name
        ttk.Label(controls_frame, text="Task Name:").pack(anchor="w", pady=(5, 0))
        self.name_entry = ttk.Entry(controls_frame, width=40)
        self.name_entry.pack(fill="x", anchor="w")
        
        # Command
        ttk.Label(controls_frame, text="Command:").pack(anchor="w", pady=(5, 0))
        self.command_entry = ttk.Entry(controls_frame, width=40)
        self.command_entry.pack(fill="x", anchor="w")
        
        # Trigger Type
        ttk.Label(controls_frame, text="Trigger Type:").pack(anchor="w", pady=(10, 0))
        self.trigger_type = ttk.Combobox(controls_frame, values=["Daily", "Weekly", "Interval"], state="readonly")
        self.trigger_type.pack(fill="x", anchor="w")
        self.trigger_type.current(0)
        self.trigger_type.bind("<<ComboboxSelected>>", self.update_trigger_options)
        
        # Dynamic Trigger Options Frame
        self.trigger_options_frame = ttk.Frame(controls_frame)
        self.trigger_options_frame.pack(fill="x", anchor="w", pady=5)
        
        self.day_options = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        
        # -- Widgets for options (we create them all and show/hide) --
        self.daily_frame = ttk.Frame(self.trigger_options_frame)
        ttk.Label(self.daily_frame, text="Time (HH:MM):").pack(side=tk.LEFT)
        self.daily_time = ttk.Entry(self.daily_frame, width=8)
        self.daily_time.pack(side=tk.LEFT, padx=5)
        
        # --- START: UI FIX ---
        # Replaced .pack() with .grid() for this frame to solve congestion
        self.weekly_frame = ttk.Frame(self.trigger_options_frame)
        
        # Configure columns to share space
        self.weekly_frame.columnconfigure(1, weight=1) # Allow 'day' combobox to use space
        self.weekly_frame.columnconfigure(3, weight=1) # Allow 'time' entry to use space

        ttk.Label(self.weekly_frame, text="Day:").grid(row=0, column=0, sticky="w", pady=2)
        self.weekly_day = ttk.Combobox(self.weekly_frame, values=self.day_options, width=10, state="readonly")
        self.weekly_day.grid(row=0, column=1, sticky="ew", padx=(5, 10))
        self.weekly_day.current(0)
        
        ttk.Label(self.weekly_frame, text="Time (HH:MM):").grid(row=0, column=2, sticky="w", pady=2, padx=(5,0))
        self.weekly_time = ttk.Entry(self.weekly_frame, width=8)
        self.weekly_time.grid(row=0, column=3, sticky="ew", padx=5)
        # --- END: UI FIX ---
        
        self.interval_frame = ttk.Frame(self.trigger_options_frame)
        ttk.Label(self.interval_frame, text="Interval (mins):").pack(side=tk.LEFT)
        self.interval_mins = ttk.Entry(self.interval_frame, width=8)
        self.interval_mins.pack(side=tk.LEFT, padx=5)

        self.update_trigger_options(None) # Set initial view

        # Add Task Button
        self.add_button = ttk.Button(controls_frame, text="Add Task", command=self.add_task)
        self.add_button.pack(fill="x", pady=20)
        
        # --- Right Side: Task List ---
        ttk.Label(list_frame, text="Scheduled Tasks", font=("Arial", 14, "bold")).pack(pady=(0, 10), anchor="w")
        
        list_sub_frame = ttk.Frame(list_frame)
        list_sub_frame.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = tk.Scrollbar(list_sub_frame, orient=tk.VERTICAL)
        self.task_listbox = tk.Listbox(list_sub_frame, yscrollcommand=scrollbar.set, 
                                        bg=self.list_bg, fg=self.fg_color, 
                                        selectbackground=self.button_bg, selectforeground=self.button_fg,
                                        font=("Arial", 10), relief=tk.FLAT, height=15)
        scrollbar.config(command=self.task_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.task_listbox.pack(fill="both", expand=True)
        
        self.delete_button = ttk.Button(list_frame, text="Delete Selected Task", command=self.delete_task, style="TButton")
        self.delete_button.pack(fill="x", pady=10)

        # --- Bottom: Log Viewer ---
        log_frame = ttk.Frame(main_frame, height=150)
        log_frame.pack(fill="x", expand=False, pady=(10, 0))
        
        ttk.Label(log_frame, text="Scheduler Log", font=("Arial", 12, "bold")).pack(anchor="w")
        self.log_text = scrolledtext.ScrolledText(log_frame, height=10, bg=self.list_bg, fg=self.fg_color, relief=tk.FLAT, state="disabled")
        self.log_text.pack(fill="x", expand=True)

    def update_trigger_options(self, event):
        """Show/hide trigger-specific entry fields."""
        self.daily_frame.pack_forget()
        self.weekly_frame.pack_forget()
        self.interval_frame.pack_forget()
        
        trigger = self.trigger_type.get()
        if trigger == "Daily":
            self.daily_frame.pack(fill="x", pady=5)
        elif trigger == "Weekly":
            self.weekly_frame.pack(fill="x", pady=5)
        elif trigger == "Interval":
            self.interval_frame.pack(fill="x", pady=5)

    def add_task(self):
        """Validates input and adds a new task."""
        name = self.name_entry.get()
        command = self.command_entry.get()
        trigger = self.trigger_type.get()
        
        if not name or not command:
            messagebox.showwarning("Input Error", "Task Name and Command are required.")
            return

        task = {"name": name, "command": command, "trigger": trigger}
        
        try:
            if trigger == "Daily":
                time_str = self.daily_time.get()
                datetime.strptime(time_str, "%H:%M") # Validate format
                task["time"] = time_str
            elif trigger == "Weekly":
                time_str = self.weekly_time.get()
                datetime.strptime(time_str, "%H:%M") # Validate format
                task["time"] = time_str
                task["day"] = self.weekly_day.get()
            elif trigger == "Interval":
                task["interval"] = int(self.interval_mins.get())
        except ValueError as e:
            messagebox.showwarning("Input Error", f"Invalid trigger value: {e}\n\nTime must be HH:MM\nInterval must be a number.")
            return

        self.tasks.append(task)
        self.update_listbox()
        self.save_tasks()
        self.log(f"Added task: {name}")

        # Clear inputs
        self.name_entry.delete(0, tk.END)
        self.command_entry.delete(0, tk.END)
        self.daily_time.delete(0, tk.END)
        self.weekly_time.delete(0, tk.END)
        self.interval_mins.delete(0, tk.END)

    def delete_task(self):
        """Deletes the selected task."""
        try:
            selected_index = self.task_listbox.curselection()[0]
            task_name = self.tasks[selected_index]["name"]
            
            if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete task '{task_name}'?"):
                del self.tasks[selected_index]
                self.update_listbox()
                self.save_tasks()
                self.log(f"Deleted task: {task_name}")
        except IndexError:
            messagebox.showwarning("No Selection", "Please select a task to delete.")

    def update_listbox(self):
        """Refreshes the task listbox from the self.tasks list."""
        self.task_listbox.delete(0, tk.END)
        for task in self.tasks:
            if task['trigger'] == 'Daily':
                display = f"[{task['trigger']}] {task['name']} @ {task['time']} -- (Cmd: {task['command']})"
            elif task['trigger'] == 'Weekly':
                display = f"[{task['trigger']}] {task['name']} @ {task['day']}, {task['time']} -- (Cmd: {task['command']})"
            elif task['trigger'] == 'Interval':
                display = f"[{task['trigger']}] {task['name']} @ Every {task['interval']} mins -- (Cmd: {task['command']})"
            self.task_listbox.insert(tk.END, display)

    def load_tasks(self):
        """Loads tasks from tasks.json."""
        try:
            with open(TASKS_FILE, 'r') as f:
                self.tasks = json.load(f)
            self.update_listbox()
            self.log(f"Loaded {len(self.tasks)} tasks from {TASKS_FILE}")
        except (IOError, json.JSONDecodeError) as e:
            self.log(f"Error loading tasks: {e}. Starting fresh.")
            self.tasks = []

    def save_tasks(self):
        """Saves the current self.tasks list to tasks.json."""
        try:
            with open(TASKS_FILE, 'w') as f:
                json.dump(self.tasks, f, indent=2)
        except IOError as e:
            self.log(f"Error saving tasks: {e}")
            messagebox.showerror("Save Error", f"Could not save tasks to file: {e}")

    # --- Scheduler and Logging ---

    def log(self, message):
        """Adds a message to the log queue (thread-safe)."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.log_queue.put(f"[{timestamp}] {message}\n")

    def poll_log_queue(self):
        """Checks the log queue and updates the GUI."""
        while not self.log_queue.empty():
            try:
                message = self.log_queue.get_nowait()
                self.log_text.config(state="normal")
                self.log_text.insert(tk.END, message)
                self.log_text.config(state="disabled")
                self.log_text.see(tk.END) # Auto-scroll
            except queue.Empty:
                pass
        # Check again in 100ms
        self.root.after(100, self.poll_log_queue)

    def start_scheduler(self):
        """Starts the background scheduler thread."""
        scheduler_thread = threading.Thread(target=self.run_scheduler, daemon=True)
        scheduler_thread.start()
        self.log("Scheduler thread started. Checking every 60 seconds.")

    def run_scheduler(self):
        """The background thread loop."""
        while True:
            now = datetime.now()
            current_time_str = now.strftime("%H:%M")
            current_day_str = now.strftime("%A")
            
            for task in self.tasks:
                try:
                    task_name = task.get("name", "Unnamed Task")
                    is_due = False

                    if task["trigger"] == "Daily":
                        if task["time"] == current_time_str:
                            is_due = self.check_last_run(task_name, 60 * 23) # Only run once a day
                            
                    elif task["trigger"] == "Weekly":
                        if task["day"] == current_day_str and task["time"] == current_time_str:
                            is_due = self.check_last_run(task_name, 60 * 60 * 24 * 6) # Only run once a week
                    
                    elif task["trigger"] == "Interval":
                        interval_seconds = task["interval"] * 60
                        is_due = self.check_last_run(task_name, interval_seconds - 30) # -30s buffer

                    if is_due:
                        self.execute_task(task)

                except Exception as e:
                    self.log(f"Scheduler Error processing task '{task.get('name')}': {e}")
            
            time.sleep(60) # Check once per minute

    def check_last_run(self, task_name, throttle_seconds):
        """Checks if a task has run within the throttle period."""
        now = time.time()
        last_run = self.last_run_times.get(task_name, 0)
        
        if (now - last_run) > throttle_seconds:
            self.last_run_times[task_name] = now
            return True
        return False

    def execute_task(self, task):
        """Runs the task's command in a subprocess."""
        command = task["command"]
        self.log(f"EXECUTING task: '{task['name']}' (Cmd: {command})")
        try:
            # Use Popen for non-blocking execution
            subprocess.Popen(command, shell=True)
        except Exception as e:
            self.log(f"Failed to execute task '{task['name']}': {e}")


# --- Run the Application ---
if __name__ == "__main__":
    ensure_files()
    root = tk.Tk()
    app = TaskAutomatorApp(root)
    root.mainloop()