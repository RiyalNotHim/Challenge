import tkinter as tk
from tkinter import ttk, messagebox, font, scrolledtext
import os
import threading
try:
    from sklearn.feature_extraction.text import CountVectorizer
except ImportError:
    pass # We will handle this in the __main__ block

# --- Main Application Class ---
class ResumeTailorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Resume Tailor")
        self.root.geometry("1000x700")

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
        self.success_fg = "#2ecc71"
        self.warn_fg = "#f39c12"
        
        self.root.configure(bg=self.bg_color)
        
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure all ttk widgets
        style.configure(".", background=self.bg_color, foreground=self.fg_color, font=("Arial", 10), borderwidth=0)
        style.configure("TFrame", background=self.bg_color)
        style.configure("TLabel", background=self.bg_color, foreground=self.fg_color)
        style.configure("Header.TLabel", font=("Arial", 14, "bold"))
        
        # Button style
        style.configure("TButton", background=self.button_bg, foreground=self.button_fg, font=("Arial", 10, "bold"), padding=5)
        style.map("TButton", background=[('active', '#005f9e')])
        
        # PanedWindow Sash
        style.configure("TPanedWindow", background=self.bg_color)
        style.configure("Sash", background=self.bg_color, bordercolor=self.bg_color, lightcolor=self.bg_color, darkcolor=self.bg_color)

    def create_widgets(self):
        """Create the main GUI elements."""
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # --- Main Paned Window (Left/Right) ---
        main_pane = ttk.PanedWindow(main_frame, orient=tk.HORIZONTAL)
        main_pane.pack(fill=tk.BOTH, expand=True)

        # --- LEFT PANE (Inputs) ---
        input_pane = ttk.PanedWindow(main_pane, orient=tk.VERTICAL)
        main_pane.add(input_pane, weight=1)
        
        # Resume Frame
        resume_frame = ttk.Frame(input_pane, padding=5)
        ttk.Label(resume_frame, text="📄 Paste Your Resume Here", style="Header.TLabel").pack(anchor="w", pady=5)
        self.resume_text = scrolledtext.ScrolledText(resume_frame, height=15, bg=self.list_bg, fg=self.fg_color, relief=tk.FLAT, font=("Arial", 10), insertbackground=self.fg_color)
        self.resume_text.pack(fill="both", expand=True)
        input_pane.add(resume_frame, weight=1)
        
        # Job Description Frame
        jd_frame = ttk.Frame(input_pane, padding=5)
        ttk.Label(jd_frame, text="📋 Paste Job Description Here", style="Header.TLabel").pack(anchor="w", pady=5)
        self.jd_text = scrolledtext.ScrolledText(jd_frame, height=10, bg=self.list_bg, fg=self.fg_color, relief=tk.FLAT, font=("Arial", 10), insertbackground=self.fg_color)
        self.jd_text.pack(fill="both", expand=True)
        input_pane.add(jd_frame, weight=1)

        # --- RIGHT PANE (Outputs) ---
        output_frame = ttk.Frame(main_pane, padding=5)
        main_pane.add(output_frame, weight=1)
        
        # Control Buttons
        control_frame = ttk.Frame(output_frame)
        control_frame.pack(fill="x", pady=5)
        
        self.analyze_button = ttk.Button(control_frame, text="Analyze", command=self.start_analysis_thread)
        self.analyze_button.pack(side=tk.LEFT, fill="x", expand=True, ipady=5, padx=(0,5))
        
        self.clear_button = ttk.Button(control_frame, text="Clear All", command=self.clear_all)
        self.clear_button.pack(side=tk.LEFT, fill="x", expand=True, ipady=5, padx=5)

        # Output Panes
        output_pane = ttk.PanedWindow(output_frame, orient=tk.VERTICAL)
        output_pane.pack(fill="both", expand=True, pady=(10,0))
        
        # Matching Keywords
        match_frame = ttk.Frame(output_pane)
        ttk.Label(match_frame, text="✅ Matching Keywords", style="Header.TLabel", foreground=self.success_fg).pack(anchor="w", pady=5)
        self.match_list = tk.Listbox(match_frame, bg=self.list_bg, fg=self.success_fg, relief=tk.FLAT, height=10, font=("Arial", 10))
        self.match_list.pack(fill="both", expand=True)
        output_pane.add(match_frame, weight=1)
        
        # Missing Keywords
        missing_frame = ttk.Frame(output_pane)
        ttk.Label(missing_frame, text="⚠️ Missing Keywords", style="Header.TLabel", foreground=self.warn_fg).pack(anchor="w", pady=5)
        self.missing_list = tk.Listbox(missing_frame, bg=self.list_bg, fg=self.warn_fg, relief=tk.FLAT, height=10, font=("Arial", 10))
        self.missing_list.pack(fill="both", expand=True)
        output_pane.add(missing_frame, weight=1)

    def clear_all(self):
        """Clears all text boxes and lists."""
        self.resume_text.delete('1.0', tk.END)
        self.jd_text.delete('1.0', tk.END)
        self.match_list.delete(0, tk.END)
        self.missing_list.delete(0, tk.END)
        
    def start_analysis_thread(self):
        """Starts the NLP analysis in a new thread."""
        resume_text = self.resume_text.get('1.0', tk.END)
        jd_text = self.jd_text.get('1.0', tk.END)

        if len(resume_text.strip()) < 50 or len(jd_text.strip()) < 50:
            messagebox.showwarning("Not Enough Text", "Please paste your full resume and job description.")
            return

        self.analyze_button.config(state="disabled", text="Analyzing...")
        
        thread = threading.Thread(target=self.analyze_text, args=(resume_text, jd_text), daemon=True)
        thread.start()

    def analyze_text(self, resume_text, jd_text):
        """The core NLP logic."""
        matching_keywords = []
        missing_keywords = []
        try:
            # 1. Extract top 100 1-word/2-word keywords from JD
            jd_vectorizer = CountVectorizer(
                stop_words='english', 
                ngram_range=(1, 2), # Find 1-word and 2-word phrases
                max_features=100    # Get top 100 keywords
            )
            jd_vectorizer.fit_transform([jd_text])
            jd_keywords = jd_vectorizer.get_feature_names_out()

            # 2. Create a new vectorizer whose *only* vocabulary is those JD keywords
            resume_vectorizer = CountVectorizer(
                stop_words='english',
                ngram_range=(1, 2),
                vocabulary=jd_keywords
            )
            
            # 3. Scan the resume for *only* those keywords
            resume_counts = resume_vectorizer.fit_transform([resume_text]).toarray()[0]
            
            # 4. Compare and sort
            for i, keyword in enumerate(jd_keywords):
                if resume_counts[i] > 0:
                    matching_keywords.append(keyword)
                else:
                    missing_keywords.append(keyword)
                    
        except Exception as e:
            messagebox.showerror("Analysis Error", f"An error occurred: {e}")
        
        # Send results back to the main thread
        self.root.after(0, self.populate_lists_threadsafe, matching_keywords, missing_keywords)

    def populate_lists_threadsafe(self, matching_keywords, missing_keywords):
        """Updates the GUI listboxes from the main thread."""
        self.match_list.delete(0, tk.END)
        self.missing_list.delete(0, tk.END)

        for keyword in sorted(matching_keywords):
            self.match_list.insert(tk.END, keyword)
            
        for keyword in sorted(missing_keywords):
            self.missing_list.insert(tk.END, keyword)
            
        self.analyze_button.config(state="normal", text="Analyze")


# --- Run the Application ---
if __name__ == "__main__":
    try:
        from sklearn.feature_extraction.text import CountVectorizer
    except ImportError:
        messagebox.showerror("Dependency Error", "Required library 'scikit-learn' is not installed.\n\nPlease run: pip install -r requirements.txt")
    else:
        root = tk.Tk()
        app = ResumeTailorApp(root)
        root.mainloop()