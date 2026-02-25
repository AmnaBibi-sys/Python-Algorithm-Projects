import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import sys
import os
import webbrowser

class AlgorithmLauncher:
    def __init__(self, root):
        self.root = root
        self.root.title("Algorithm Visualization Suite")
        self.root.geometry("800x700")
        self.root.configure(bg='#2c3e50')
        
        # Center the window
        self.center_window()
        
        # Make window resizable
        self.root.minsize(700, 600)
        
        self.create_widgets()
    
    def center_window(self):
        self.root.update_idletasks()
        width = 800
        height = 700
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def create_widgets(self):
        # Main container with scrollbar
        main_container = tk.Frame(self.root, bg='#2c3e50')
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Create canvas and scrollbar
        canvas = tk.Canvas(main_container, bg='#2c3e50', highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_container, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#2c3e50')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Bind mouse wheel for scrolling
        def _on_mouse_wheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        canvas.bind_all("<MouseWheel>", _on_mouse_wheel)
        
        # Header
        header_frame = tk.Frame(scrollable_frame, bg='#2c3e50')
        header_frame.pack(pady=(0, 30))
        
        # Logo/Title
        title_frame = tk.Frame(header_frame, bg='#2c3e50')
        title_frame.pack()
        
        # Emoji or icon labels
        tk.Label(title_frame, text="📊", font=('Arial', 40), 
                bg='#2c3e50', fg='#3498db').pack(side=tk.LEFT, padx=(0, 10))
        
        title_text = tk.Label(title_frame, text="Algorithm\nVisualization Suite", 
                             font=('Arial', 28, 'bold'), bg='#2c3e50', fg='#ecf0f1',
                             justify=tk.LEFT)
        title_text.pack(side=tk.LEFT)
        
        tk.Label(header_frame, text="Interactive Algorithm Demonstrations", 
                font=('Arial', 14), bg='#2c3e50', fg='#bdc3c7').pack(pady=(5, 20))
        
        # Stats frame
        stats_frame = tk.Frame(header_frame, bg='#34495e', relief=tk.RAISED, borderwidth=2)
        stats_frame.pack(fill=tk.X, pady=10)
        
        stats_data = [
            ("4", "Projects"),
            ("10+", "Algorithms"),
            ("🎯", "Interactive"),
            ("📈", "Visual")
        ]
        
        for value, label in stats_data:
            stat_frame = tk.Frame(stats_frame, bg='#34495e')
            stat_frame.pack(side=tk.LEFT, expand=True, padx=10, pady=10)
            tk.Label(stat_frame, text=value, font=('Arial', 18, 'bold'), 
                    bg='#34495e', fg='#3498db').pack()
            tk.Label(stat_frame, text=label, font=('Arial', 10), 
                    bg='#34495e', fg='#bdc3c7').pack()
        
        # Projects Frame
        projects_frame = tk.LabelFrame(scrollable_frame, text="📂 Available Projects", 
                                      bg='#34495e', fg='white', font=('Arial', 16, 'bold'),
                                      relief=tk.RAISED, borderwidth=3)
        projects_frame.pack(fill=tk.BOTH, expand=True, pady=20)
        
        # Project cards
        projects = [
            {
                "icon": "📊",
                "title": "Linear Sorting",
                "description": "Visualize sorting algorithms with interactive animations",
                "algorithms": ["Bubble Sort", "Selection Sort", "Insertion Sort", "Quick Sort", "Merge Sort"],
                "file": "linear_sorting.py",
                "color": "#3498db"
            },
            {
                "icon": "🧮",
                "title": "Matrix Multiplication",
                "description": "Step-by-step matrix multiplication visualization",
                "algorithms": ["Standard Algorithm", "Strassen's Algorithm"],
                "file": "matrix_multiplication.py",
                "color": "#9b59b6"
            },
            {
                "icon": "🌳",
                "title": "Minimum Spanning Tree",
                "description": "Find MST using Prim's or Kruskal's algorithm",
                "algorithms": ["Prim's Algorithm", "Kruskal's Algorithm"],
                "file": "minimum_spanning_tree.py",
                "color": "#2ecc71"
            },
            {
                "icon": "⚡",
                "title": "Heap Sort",
                "description": "Visualize Heap Sort with dual array and tree views",
                "algorithms": ["Heap Sort", "Max-Heap Building", "Heapify Process"],
                "file": "heap_sort.py",
                "color": "#e74c3c"
            }
        ]
        
        # Create project cards in a grid
        for i, project in enumerate(projects):
            project_frame = tk.Frame(projects_frame, bg='#2c3e50', relief=tk.RAISED, borderwidth=1)
            
            if i % 2 == 0:
                project_frame.grid(row=i//2, column=0, padx=10, pady=10, sticky="nsew")
            else:
                project_frame.grid(row=i//2, column=1, padx=10, pady=10, sticky="nsew")
            
            # Make the grid cells expand
            projects_frame.grid_columnconfigure(0, weight=1)
            projects_frame.grid_columnconfigure(1, weight=1)
            projects_frame.grid_rowconfigure(i//2, weight=1)
            
            # Project icon and title
            header_frame = tk.Frame(project_frame, bg=project["color"])
            header_frame.pack(fill=tk.X)
            
            tk.Label(header_frame, text=project["icon"], font=('Arial', 24),
                    bg=project["color"], fg='white').pack(side=tk.LEFT, padx=10, pady=10)
            
            title_frame = tk.Frame(header_frame, bg=project["color"])
            title_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
            
            tk.Label(title_frame, text=project["title"], font=('Arial', 16, 'bold'),
                    bg=project["color"], fg='white', justify=tk.LEFT).pack(anchor='w')
            
            # Content area
            content_frame = tk.Frame(project_frame, bg='#2c3e50')
            content_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
            
            # Description
            tk.Label(content_frame, text=project["description"], 
                    font=('Arial', 10), bg='#2c3e50', fg='#bdc3c7',
                    wraplength=250, justify=tk.LEFT).pack(anchor='w', pady=(0, 10))
            
            # Algorithms included
            algo_frame = tk.Frame(content_frame, bg='#34495e')
            algo_frame.pack(fill=tk.X, pady=(0, 10))
            
            tk.Label(algo_frame, text="Algorithms:", font=('Arial', 10, 'bold'),
                    bg='#34495e', fg='white').pack(anchor='w', padx=5, pady=5)
            
            for algo in project["algorithms"]:
                algo_item = tk.Frame(algo_frame, bg='#34495e')
                algo_item.pack(anchor='w', padx=10)
                tk.Label(algo_item, text="•", bg='#34495e', fg=project["color"],
                        font=('Arial', 10)).pack(side=tk.LEFT)
                tk.Label(algo_item, text=algo, bg='#34495e', fg='#ecf0f7',
                        font=('Arial', 9)).pack(side=tk.LEFT, padx=5)
            
            # Run button
            btn_frame = tk.Frame(content_frame, bg='#2c3e50')
            btn_frame.pack(fill=tk.X, pady=(10, 0))
            
            tk.Button(btn_frame, text="▶ Run Project", 
                     command=lambda p=project: self.run_project(p["file"]),
                     bg=project["color"], fg='white', font=('Arial', 10, 'bold'),
                     padx=20, pady=8, relief=tk.RAISED, borderwidth=2,
                     cursor="hand2").pack()
        
        # Control Buttons Frame
        control_frame = tk.Frame(scrollable_frame, bg='#2c3e50')
        control_frame.pack(fill=tk.X, pady=20)
        
        # Run All button
        run_all_btn = tk.Button(control_frame, text="🚀 Run All Projects", 
                               command=self.run_all_projects,
                               font=('Arial', 12, 'bold'), bg='#2ecc71', fg='white',
                               padx=30, pady=12, relief=tk.RAISED, borderwidth=3,
                               cursor="hand2")
        run_all_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Check Files button
        check_btn = tk.Button(control_frame, text="🔍 Check Files", 
                             command=self.check_files,
                             font=('Arial', 11), bg='#f39c12', fg='white',
                             padx=20, pady=10, relief=tk.RAISED, borderwidth=2,
                             cursor="hand2")
        check_btn.pack(side=tk.LEFT, padx=10)
        
        # Documentation button
        docs_btn = tk.Button(control_frame, text="📚 Documentation", 
                            command=self.open_documentation,
                            font=('Arial', 11), bg='#3498db', fg='white',
                            padx=20, pady=10, relief=tk.RAISED, borderwidth=2,
                            cursor="hand2")
        docs_btn.pack(side=tk.LEFT, padx=10)
        
        # About button
        about_btn = tk.Button(control_frame, text="ℹ️ About", 
                             command=self.show_about,
                             font=('Arial', 11), bg='#9b59b6', fg='white',
                             padx=20, pady=10, relief=tk.RAISED, borderwidth=2,
                             cursor="hand2")
        about_btn.pack(side=tk.LEFT, padx=10)
        
        # Footer
        footer_frame = tk.Frame(scrollable_frame, bg='#2c3e50')
        footer_frame.pack(fill=tk.X, pady=20)
        
        # Separator
        tk.Frame(footer_frame, height=2, bg='#34495e').pack(fill=tk.X, pady=(0, 20))
        
        # Footer content
        footer_content = tk.Frame(footer_frame, bg='#2c3e50')
        footer_content.pack()
        
        tk.Label(footer_content, text="Algorithm Visualization Suite v2.0", 
                font=('Arial', 10, 'bold'), bg='#2c3e50', fg='#7f8c8d').pack(side=tk.LEFT, padx=10)
        
        tk.Label(footer_content, text="•", 
                font=('Arial', 10), bg='#2c3e50', fg='#34495e').pack(side=tk.LEFT, padx=5)
        
        tk.Label(footer_content, text="Created with Python & Tkinter", 
                font=('Arial', 10), bg='#2c3e50', fg='#7f8c8d').pack(side=tk.LEFT, padx=10)
        
        tk.Label(footer_content, text="•", 
                font=('Arial', 10), bg='#2c3e50', fg='#34495e').pack(side=tk.LEFT, padx=5)
        
        # Status label
        self.status_label = tk.Label(footer_content, text="✅ Ready", 
                                    font=('Arial', 10), bg='#2c3e50', fg='#2ecc71')
        self.status_label.pack(side=tk.LEFT, padx=10)
    
    def run_project(self, filename):
        try:
            if os.path.exists(filename):
                self.status_label.config(text=f"🚀 Launching {filename}...", fg='#f39c12')
                self.root.update()
                
                # Run the project in a separate process
                subprocess.Popen([sys.executable, filename])
                
                self.status_label.config(text=f"✅ {filename} launched", fg='#2ecc71')
                
                # Log to console
                print(f"[INFO] Launched: {filename}")
            else:
                messagebox.showerror("Error", f"File '{filename}' not found!\n\nMake sure all project files are in the same directory:\n• linear_sorting.py\n• matrix_multiplication.py\n• minimum_spanning_tree.py\n• heap_sort.py")
                self.status_label.config(text="❌ File not found", fg='#e74c3c')
        except Exception as e:
            messagebox.showerror("Error", f"Failed to run {filename}:\n\n{str(e)}")
            self.status_label.config(text="❌ Launch failed", fg='#e74c3c')
            print(f"[ERROR] Failed to launch {filename}: {e}")
    
    def run_all_projects(self):
        projects = ["linear_sorting.py", "matrix_multiplication.py", 
                   "minimum_spanning_tree.py", "heap_sort.py"]
        
        self.status_label.config(text="🚀 Launching all projects...", fg='#f39c12')
        self.root.update()
        
        launched_count = 0
        for project in projects:
            if os.path.exists(project):
                try:
                    subprocess.Popen([sys.executable, project])
                    launched_count += 1
                    print(f"[INFO] Launched: {project}")
                except Exception as e:
                    print(f"[ERROR] Failed to launch {project}: {e}")
        
        if launched_count > 0:
            self.status_label.config(text=f"✅ {launched_count} projects launched", fg='#2ecc71')
            messagebox.showinfo("Success", f"Launched {launched_count} out of {len(projects)} projects!")
        else:
            self.status_label.config(text="❌ No projects found", fg='#e74c3c')
            messagebox.showwarning("Warning", "No project files found in the current directory!")
    
    def check_files(self):
        files = ["linear_sorting.py", "matrix_multiplication.py", 
                "minimum_spanning_tree.py", "heap_sort.py"]
        
        missing_files = []
        existing_files = []
        
        for file in files:
            if os.path.exists(file):
                existing_files.append(f"✅ {file}")
            else:
                missing_files.append(f"❌ {file}")
        
        result = "File Status Check:\n\n"
        result += "Found:\n" + "\n".join(existing_files) + "\n\n"
        
        if missing_files:
            result += "Missing:\n" + "\n".join(missing_files) + "\n\n"
            result += "Please make sure all files are in the same directory."
        else:
            result += "🎉 All files are present! Ready to run."
        
        messagebox.showinfo("File Check", result)
        self.status_label.config(text="🔍 File check completed", fg='#3498db')
    
    def open_documentation(self):
        docs = """
        📚 Algorithm Visualization Suite - Documentation
        
        1. LINEAR SORTING
           • Bubble Sort: O(n²) - Compare and swap adjacent elements
           • Selection Sort: O(n²) - Find minimum and swap
           • Insertion Sort: O(n²) - Build sorted array one element at a time
           • Quick Sort: O(n log n) - Divide and conquer with pivot
           • Merge Sort: O(n log n) - Divide and merge sorted halves
        
        2. MATRIX MULTIPLICATION
           • Standard Algorithm: O(n³) - Triple nested loops
           • Step-by-step visualization of dot products
           • Interactive matrix editing
        
        3. MINIMUM SPANNING TREE
           • Prim's Algorithm: Greedy approach from a start node
           • Kruskal's Algorithm: Sort edges and avoid cycles
           • Interactive graph creation
        
        4. HEAP SORT
           • Max-Heap Building: O(n)
           • Heap Sort: O(n log n)
           • Dual visualization: Array + Tree structure
        
        CONTROLS:
        • Adjust array size and speed sliders
        • Use step-by-step mode for learning
        • Generate random inputs
        • Manual input available
        
        TIPS:
        • Start with smaller arrays to understand algorithms
        • Use slow speed for complex algorithms
        • Watch both array and tree visualizations for Heap Sort
        """
        
        # Create a documentation window
        doc_window = tk.Toplevel(self.root)
        doc_window.title("Documentation")
        doc_window.geometry("600x500")
        doc_window.configure(bg='#2c3e50')
        
        # Add scrollable text
        text_frame = tk.Frame(doc_window, bg='#2c3e50')
        text_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        text_widget = tk.Text(text_frame, bg='#2c3e50', fg='white', 
                             font=('Consolas', 10), wrap=tk.WORD)
        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar = tk.Scrollbar(text_frame, command=text_widget.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        text_widget.config(yscrollcommand=scrollbar.set)
        
        text_widget.insert(tk.END, docs)
        text_widget.config(state=tk.DISABLED)
        
        self.status_label.config(text="📚 Documentation opened", fg='#3498db')
    
    def show_about(self):
        about_text = """
        🎓 Algorithm Visualization Suite v2.0
        
        An educational tool for understanding computer science algorithms
        through interactive visualizations.
        
        FEATURES:
        • 4 different algorithm projects
        • 10+ algorithm implementations
        • Professional Tkinter UI
        • Real-time visualizations
        • Educational step-by-step mode
        • No external dependencies required
        
        INCLUDED PROJECTS:
        1. Linear Sorting Algorithms
        2. Matrix Multiplication
        3. Minimum Spanning Tree
        4. Heap Sort Algorithm
        
        TECHNOLOGIES:
        • Python 3.x
        • Tkinter GUI Toolkit
        • Standard Python Libraries
        
        PURPOSE:
        This suite is designed to help students and developers
        understand how algorithms work through visualization.
        
        Created for educational purposes.
        All visualizations are interactive and real-time.
        
        🚀 Happy Learning!
        """
        
        messagebox.showinfo("About", about_text)
        self.status_label.config(text="ℹ️ About shown", fg='#9b59b6')

if __name__ == "__main__":
    root = tk.Tk()
    app = AlgorithmLauncher(root)
    root.mainloop()