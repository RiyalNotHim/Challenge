import tkinter as tk
from tkinter import ttk, messagebox, font, filedialog, scrolledtext
import os
import threading
import fitz  # This is PyMuPDF

# --- Main Application Class ---
class PDFUtilityApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Utility")
        self.root.geometry("700x600")

        self.setup_styles()
        self.create_widgets()

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
        
        # Configure all ttk widgets
        style.configure(".", background=self.bg_color, foreground=self.fg_color, font=("Arial", 10))
        style.configure("TFrame", background=self.bg_color)
        style.configure("TLabel", background=self.bg_color, foreground=self.fg_color)
        style.configure("Header.TLabel", font=("Arial", 14, "bold"))
        
        # Button style
        style.configure("TButton", background=self.button_bg, foreground=self.button_fg, font=("Arial", 10, "bold"), borderwidth=0)
        style.map("TButton", background=[('active', '#005f9e')])
        
        # Notebook (Tabs) style
        style.configure("TNotebook", background=self.bg_color, borderwidth=0)
        style.configure("TNotebook.Tab", background=self.button_bg, foreground=self.button_fg, padding=[10, 5], font=("Arial", 10, "bold"))
        style.map("TNotebook.Tab", background=[("selected", self.button_bg), ("active", "#005f9e")], foreground=[("selected", self.button_fg)])

    def create_widgets(self):
        """Create the main GUI elements, including tabs."""
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # --- Tab Control ---
        self.tab_control = ttk.Notebook(main_frame)
        
        self.merge_tab = ttk.Frame(self.tab_control, padding="10")
        self.compress_tab = ttk.Frame(self.tab_control, padding="10")
        
        self.tab_control.add(self.merge_tab, text='Merge PDFs')
        self.tab_control.add(self.compress_tab, text='Compress PDFs')
        
        self.tab_control.pack(fill="both", expand=True)
        
        # --- Create content for each tab ---
        self.create_merge_tab_widgets()
        self.create_compress_tab_widgets()

        # --- Log Viewer (Common to all) ---
        log_frame = ttk.Frame(main_frame, height=150)
        log_frame.pack(fill="x", expand=False, pady=(10, 0))
        
        ttk.Label(log_frame, text="Log", font=("Arial", 12, "bold")).pack(anchor="w")
        self.log_text = scrolledtext.ScrolledText(log_frame, height=10, bg=self.list_bg, fg=self.fg_color, relief=tk.FLAT, state="disabled", font=("Courier New", 9))
        self.log_text.pack(fill="both", expand=True)

    def create_merge_tab_widgets(self):
        """Populate the Merge PDFs tab."""
        # --- File List Frame ---
        list_frame = ttk.Frame(self.merge_tab)
        list_frame.pack(fill="both", expand=True)
        
        ttk.Label(list_frame, text="Files to Merge (in order):").pack(anchor="w")
        
        list_sub_frame = ttk.Frame(list_frame)
        list_sub_frame.pack(fill="both", expand=True, pady=5)
        
        scrollbar = tk.Scrollbar(list_sub_frame, orient=tk.VERTICAL)
        self.merge_listbox = tk.Listbox(list_sub_frame, yscrollcommand=scrollbar.set, 
                                        bg=self.list_bg, fg=self.fg_color, 
                                        selectbackground=self.button_bg, selectforeground=self.button_fg,
                                        font=("Arial", 10), relief=tk.FLAT, height=10)
        scrollbar.config(command=self.merge_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.merge_listbox.pack(fill="both", expand=True)
        
        # --- File Control Buttons ---
        file_btn_frame = ttk.Frame(self.merge_tab)
        file_btn_frame.pack(fill="x", pady=5)
        
        ttk.Button(file_btn_frame, text="Add PDF(s)", command=self.add_pdfs_to_merge).pack(side=tk.LEFT, expand=True, fill="x")
        ttk.Button(file_btn_frame, text="Remove Selected", command=self.remove_from_merge).pack(side=tk.LEFT, expand=True, fill="x", padx=5)
        ttk.Button(file_btn_frame, text="Clear List", command=self.clear_merge).pack(side=tk.LEFT, expand=True, fill="x")
        
        # --- Ordering Buttons ---
        order_btn_frame = ttk.Frame(self.merge_tab)
        order_btn_frame.pack(fill="x", pady=5)
        
        ttk.Button(order_btn_frame, text="Move Up", command=self.move_up_merge).pack(side=tk.LEFT, expand=True, fill="x", padx=(0,5))
        ttk.Button(order_btn_frame, text="Move Down", command=self.move_down_merge).pack(side=tk.LEFT, expand=True, fill="x")
        
        # --- Main Action Button ---
        self.merge_button = ttk.Button(self.merge_tab, text="Merge and Save As...", command=self.start_merge_thread)
        self.merge_button.pack(fill="x", pady=10, ipady=5)

    def create_compress_tab_widgets(self):
        """Populate the Compress PDFs tab."""
        # --- File List Frame ---
        list_frame = ttk.Frame(self.compress_tab)
        list_frame.pack(fill="both", expand=True)
        
        ttk.Label(list_frame, text="Files to Compress (Batch):").pack(anchor="w")
        
        list_sub_frame = ttk.Frame(list_frame)
        list_sub_frame.pack(fill="both", expand=True, pady=5)
        
        scrollbar = tk.Scrollbar(list_sub_frame, orient=tk.VERTICAL)
        self.compress_listbox = tk.Listbox(list_sub_frame, yscrollcommand=scrollbar.set, 
                                        bg=self.list_bg, fg=self.fg_color, 
                                        selectbackground=self.button_bg, selectforeground=self.button_fg,
                                        font=("Arial", 10), relief=tk.FLAT, height=10, selectmode=tk.EXTENDED)
        scrollbar.config(command=self.compress_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.compress_listbox.pack(fill="both", expand=True)
        
        # --- File Control Buttons ---
        file_btn_frame = ttk.Frame(self.compress_tab)
        file_btn_frame.pack(fill="x", pady=5)
        
        ttk.Button(file_btn_frame, text="Add PDF(s)", command=self.add_pdfs_to_compress).pack(side=tk.LEFT, expand=True, fill="x")
        ttk.Button(file_btn_frame, text="Remove Selected", command=self.remove_from_compress).pack(side=tk.LEFT, expand=True, fill="x", padx=5)
        ttk.Button(file_btn_frame, text="Clear List", command=self.clear_compress).pack(side=tk.LEFT, expand=True, fill="x")
        
        # --- Main Action Button ---
        self.compress_button = ttk.Button(self.compress_tab, text="Compress Selected Files", command=self.start_compress_thread)
        self.compress_button.pack(fill="x", pady=10, ipady=5)

    # --- Logging ---
    def log(self, message):
        """Inserts a message into the log text area (thread-safe)."""
        def _log_to_gui():
            self.log_text.config(state="normal")
            self.log_text.insert(tk.END, f"{message}\n")
            self.log_text.config(state="disabled")
            self.log_text.see(tk.END) # Auto-scroll
        self.root.after(0, _log_to_gui)

    # --- Merge Tab Functions ---
    def add_pdfs_to_merge(self):
        files = filedialog.askopenfilenames(title="Select PDFs", filetypes=[("PDF files", "*.pdf")])
        for f in files:
            self.merge_listbox.insert(tk.END, f)
            
    def remove_from_merge(self):
        try:
            indices = self.merge_listbox.curselection()
            for i in reversed(indices): # Remove from back to front
                self.merge_listbox.delete(i)
        except: pass
        
    def clear_merge(self):
        self.merge_listbox.delete(0, tk.END)

    def move_up_merge(self):
        try:
            idx = self.merge_listbox.curselection()[0]
            if idx > 0:
                text = self.merge_listbox.get(idx)
                self.merge_listbox.delete(idx)
                self.merge_listbox.insert(idx - 1, text)
                self.merge_listbox.selection_set(idx - 1)
        except: pass

    def move_down_merge(self):
        try:
            idx = self.merge_listbox.curselection()[0]
            if idx < self.merge_listbox.size() - 1:
                text = self.merge_listbox.get(idx)
                self.merge_listbox.delete(idx)
                self.merge_listbox.insert(idx + 1, text)
                self.merge_listbox.selection_set(idx + 1)
        except: pass

    def start_merge_thread(self):
        files = self.merge_listbox.get(0, tk.END)
        if len(files) < 2:
            messagebox.showwarning("Not Enough Files", "Please add at least two PDF files to merge.")
            return

        save_path = filedialog.asksaveasfilename(title="Save Merged PDF As...", filetypes=[("PDF files", "*.pdf")], defaultextension=".pdf")
        if not save_path:
            return # User cancelled save dialog

        self.merge_button.config(state="disabled", text="Merging...")
        self.log("="*50)
        self.log(f"Starting merge... saving to {save_path}")
        
        thread = threading.Thread(target=self.merge_files, args=(files, save_path), daemon=True)
        thread.start()

    def merge_files(self, files, save_path):
        try:
            output_pdf = fitz.open() # Create a new, empty PDF
            for filepath in files:
                self.log(f"  Adding: {os.path.basename(filepath)}")
                pdf = fitz.open(filepath)
                output_pdf.insert_pdf(pdf) # Append all pages from pdf
                pdf.close()
            
            output_pdf.save(save_path)
            output_pdf.close()
            self.log(f"SUCCESS: Merged {len(files)} files and saved to {save_path}")
            
        except Exception as e:
            self.log(f"ERROR during merge: {e}")
            messagebox.showerror("Merge Error", f"An error occurred: {e}")
        
        self.root.after(0, lambda: self.merge_button.config(state="normal", text="Merge and Save As..."))

    # --- Compress Tab Functions ---
    def add_pdfs_to_compress(self):
        files = filedialog.askopenfilenames(title="Select PDFs", filetypes=[("PDF files", "*.pdf")])
        for f in files:
            self.compress_listbox.insert(tk.END, f)
            
    def remove_from_compress(self):
        try:
            indices = self.compress_listbox.curselection()
            for i in reversed(indices): # Remove from back to front
                self.compress_listbox.delete(i)
        except: pass
        
    def clear_compress(self):
        self.compress_listbox.delete(0, tk.END)

    def start_compress_thread(self):
        files = self.compress_listbox.get(0, tk.END)
        if not files:
            messagebox.showwarning("No Files", "Please add at least one PDF file to compress.")
            return

        if not messagebox.askyesno("Confirm Compression", f"This will compress {len(files)} file(s) and save them with a '_compressed.pdf' suffix in their original folders.\n\nContinue?"):
            return

        self.compress_button.config(state="disabled", text="Compressing...")
        self.log("="*50)
        self.log(f"Starting batch compression for {len(files)} file(s)...")
        
        thread = threading.Thread(target=self.compress_files, args=(files,), daemon=True)
        thread.start()

    def compress_files(self, files):
        success_count = 0
        fail_count = 0
        try:
            for src_path in files:
                try:
                    self.log(f"  Compressing: {os.path.basename(src_path)}...")
                    pdf = fitz.open(src_path)
                    
                    # Define destination path
                    base, ext = os.path.splitext(src_path)
                    dest_path = f"{base}_compressed.pdf"
                    
                    # Save with garbage collection, deflation, and optimization
                    pdf.save(dest_path, garbage=4, deflate=True, clean=True)
                    pdf.close()
                    
                    self.log(f"  -> Saved: {os.path.basename(dest_path)}")
                    success_count += 1
                except Exception as e:
                    self.log(f"  !! FAILED to compress {os.path.basename(src_path)}: {e}")
                    fail_count += 1
            
            self.log(f"SUCCESS: Batch compression complete. {success_count} files compressed, {fail_count} failed.")
            
        except Exception as e:
            self.log(f"FATAL ERROR during batch compression: {e}")
        
        self.root.after(0, lambda: self.compress_button.config(state="normal", text="Compress Selected Files"))

# --- Run the Application ---
if __name__ == "__main__":
    try:
        import fitz
    except ImportError:
        messagebox.showerror("Dependency Error", "Required library 'PyMuPDF' is not installed.\n\nPlease run: pip install PyMuPDF")
    else:
        root = tk.Tk()
        app = PDFUtilityApp(root)
        root.mainloop()