import tkinter as tk
from tkinter import ttk, messagebox
import random
import time
from threading import Thread

class MatrixMultiplicationVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Matrix Multiplication Visualizer")
        self.root.geometry("1200x800")
        self.root.configure(bg='#2c3e50')
        
        self.matrix_a = []
        self.matrix_b = []
        self.result_matrix = []
        self.steps = []
        self.current_step = 0
        
        self.create_widgets()
        self.create_default_matrices()
    
    def create_widgets(self):
        # Title
        title_label = tk.Label(self.root, text="Matrix Multiplication Visualizer", 
                              font=('Arial', 24, 'bold'), bg='#2c3e50', fg='#ecf0f1')
        title_label.pack(pady=20)
        
        # Main frame
        main_frame = tk.Frame(self.root, bg='#2c3e50')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Left panel for controls
        control_frame = tk.Frame(main_frame, bg='#34495e', relief=tk.RAISED, borderwidth=2)
        control_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        
        # Matrix size controls
        size_frame = tk.LabelFrame(control_frame, text="Matrix Dimensions", 
                                  bg='#34495e', fg='white', font=('Arial', 12, 'bold'))
        size_frame.pack(pady=10, padx=10, fill=tk.X)
        
        # Matrix A dimensions
        tk.Label(size_frame, text="Matrix A (m x n):", bg='#34495e', fg='white').grid(row=0, column=0, pady=5)
        self.m_entry = tk.Entry(size_frame, width=5)
        self.m_entry.insert(0, "3")
        self.m_entry.grid(row=0, column=1, pady=5)
        
        tk.Label(size_frame, text="x", bg='#34495e', fg='white').grid(row=0, column=2)
        self.n_entry = tk.Entry(size_frame, width=5)
        self.n_entry.insert(0, "3")
        self.n_entry.grid(row=0, column=3, pady=5)
        
        # Matrix B dimensions
        tk.Label(size_frame, text="Matrix B (n x p):", bg='#34495e', fg='white').grid(row=1, column=0, pady=5)
        self.p_entry = tk.Entry(size_frame, width=5)
        self.p_entry.insert(0, "3")
        self.p_entry.grid(row=1, column=1, pady=5)
        
        # Buttons
        btn_frame = tk.Frame(control_frame, bg='#34495e')
        btn_frame.pack(pady=10)
        
        buttons = [
            ("Generate Matrices", self.generate_matrices),
            ("Manual Input", self.manual_input),
            ("Multiply", self.start_multiplication),
            ("Step Forward", self.step_forward),
            ("Step Backward", self.step_backward),
            ("Reset", self.reset_visualization)
        ]
        
        for text, command in buttons:
            btn = tk.Button(btn_frame, text=text, command=command,
                          bg='#3498db', fg='white', font=('Arial', 10, 'bold'),
                          padx=15, pady=8, relief=tk.RAISED, borderwidth=2)
            btn.pack(pady=5, fill=tk.X)
        
        # Algorithm selection
        algo_frame = tk.LabelFrame(control_frame, text="Algorithm", 
                                  bg='#34495e', fg='white', font=('Arial', 12, 'bold'))
        algo_frame.pack(pady=10, padx=10, fill=tk.X)
        
        self.algo_var = tk.StringVar(value="standard")
        algorithms = [("Standard O(n³)", "standard"),
                     ("Strassen (Power of 2)", "strassen")]
        
        for text, value in algorithms:
            rb = tk.Radiobutton(algo_frame, text=text, variable=self.algo_var,
                              value=value, bg='#34495e', fg='white',
                              selectcolor='#2c3e50', activebackground='#34495e')
            rb.pack(anchor=tk.W, pady=2)
        
        # Info panel
        info_frame = tk.LabelFrame(control_frame, text="Information", 
                                  bg='#34495e', fg='white', font=('Arial', 12, 'bold'))
        info_frame.pack(pady=10, padx=10, fill=tk.X)
        
        self.info_text = tk.Text(info_frame, height=8, width=25, bg='#2c3e50',
                                fg='white', font=('Consolas', 10), relief=tk.FLAT)
        self.info_text.pack(pady=5, padx=5)
        self.info_text.insert(tk.END, "Ready to multiply matrices!\n\n")
        self.info_text.config(state=tk.DISABLED)
        
        # Right panel for matrices visualization
        self.visualization_frame = tk.Frame(main_frame, bg='#2c3e50')
        self.visualization_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Create matrix display areas
        self.create_matrix_displays()
    
    def create_matrix_displays(self):
        # Clear existing displays
        for widget in self.visualization_frame.winfo_children():
            widget.destroy()
        
        # Matrix A display
        matrix_a_frame = tk.Frame(self.visualization_frame, bg='#2c3e50')
        matrix_a_frame.pack(side=tk.LEFT, padx=10)
        
        tk.Label(matrix_a_frame, text="Matrix A", font=('Arial', 14, 'bold'),
                bg='#2c3e50', fg='#3498db').pack()
        
        self.matrix_a_canvas = tk.Canvas(matrix_a_frame, width=200, height=200, 
                                        bg='#1a1a2e', highlightthickness=1,
                                        highlightbackground='#3498db')
        self.matrix_a_canvas.pack(pady=10)
        
        # Multiplication symbol
        symbol_frame = tk.Frame(self.visualization_frame, bg='#2c3e50')
        symbol_frame.pack(side=tk.LEFT, padx=10)
        tk.Label(symbol_frame, text="×", font=('Arial', 40, 'bold'),
                bg='#2c3e50', fg='white').pack(expand=True)
        
        # Matrix B display
        matrix_b_frame = tk.Frame(self.visualization_frame, bg='#2c3e50')
        matrix_b_frame.pack(side=tk.LEFT, padx=10)
        
        tk.Label(matrix_b_frame, text="Matrix B", font=('Arial', 14, 'bold'),
                bg='#2c3e50', fg='#3498db').pack()
        
        self.matrix_b_canvas = tk.Canvas(matrix_b_frame, width=200, height=200,
                                        bg='#1a1a2e', highlightthickness=1,
                                        highlightbackground='#3498db')
        self.matrix_b_canvas.pack(pady=10)
        
        # Equals symbol
        equals_frame = tk.Frame(self.visualization_frame, bg='#2c3e50')
        equals_frame.pack(side=tk.LEFT, padx=10)
        tk.Label(equals_frame, text="=", font=('Arial', 40, 'bold'),
                bg='#2c3e50', fg='white').pack(expand=True)
        
        # Result matrix display
        result_frame = tk.Frame(self.visualization_frame, bg='#2c3e50')
        result_frame.pack(side=tk.LEFT, padx=10)
        
        tk.Label(result_frame, text="Result Matrix", font=('Arial', 14, 'bold'),
                bg='#2c3e50', fg='#2ecc71').pack()
        
        self.result_canvas = tk.Canvas(result_frame, width=200, height=200,
                                      bg='#1a1a2e', highlightthickness=1,
                                      highlightbackground='#2ecc71')
        self.result_canvas.pack(pady=10)
    
    def create_default_matrices(self):
        try:
            self.matrix_a = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
            self.matrix_b = [[9, 8, 7], [6, 5, 4], [3, 2, 1]]
            self.display_matrices()
        except:
            pass
    
    def generate_matrices(self):
        try:
            m = int(self.m_entry.get())
            n = int(self.n_entry.get())
            p = int(self.p_entry.get())
            
            # Generate random matrices without numpy
            self.matrix_a = [[random.randint(1, 10) for _ in range(n)] for _ in range(m)]
            self.matrix_b = [[random.randint(1, 10) for _ in range(p)] for _ in range(n)]
            
            self.display_matrices()
            self.update_info("Matrices generated successfully!")
        except ValueError:
            messagebox.showerror("Error", "Please enter valid dimensions")
    
    def manual_input(self):
        input_window = tk.Toplevel(self.root)
        input_window.title("Manual Matrix Input")
        input_window.geometry("800x600")
        input_window.configure(bg='#2c3e50')
        
        tk.Label(input_window, text="Enter Matrix Values", 
                font=('Arial', 16, 'bold'), bg='#2c3e50', fg='white').pack(pady=10)
        
        # Matrix A input
        matrix_a_frame = tk.Frame(input_window, bg='#34495e')
        matrix_a_frame.pack(side=tk.LEFT, padx=20, pady=10)
        
        tk.Label(matrix_a_frame, text="Matrix A", bg='#34495e', 
                fg='white', font=('Arial', 12, 'bold')).pack()
        
        self.a_entries = []
        for i in range(len(self.matrix_a)):
            row_entries = []
            row_frame = tk.Frame(matrix_a_frame, bg='#34495e')
            row_frame.pack()
            for j in range(len(self.matrix_a[0])):
                entry = tk.Entry(row_frame, width=5)
                entry.insert(0, str(self.matrix_a[i][j]))
                entry.pack(side=tk.LEFT, padx=2)
                row_entries.append(entry)
            self.a_entries.append(row_entries)
        
        # Matrix B input
        matrix_b_frame = tk.Frame(input_window, bg='#34495e')
        matrix_b_frame.pack(side=tk.RIGHT, padx=20, pady=10)
        
        tk.Label(matrix_b_frame, text="Matrix B", bg='#34495e', 
                fg='white', font=('Arial', 12, 'bold')).pack()
        
        self.b_entries = []
        for i in range(len(self.matrix_b)):
            row_entries = []
            row_frame = tk.Frame(matrix_b_frame, bg='#34495e')
            row_frame.pack()
            for j in range(len(self.matrix_b[0])):
                entry = tk.Entry(row_frame, width=5)
                entry.insert(0, str(self.matrix_b[i][j]))
                entry.pack(side=tk.LEFT, padx=2)
                row_entries.append(entry)
            self.b_entries.append(row_entries)
        
        # Buttons
        btn_frame = tk.Frame(input_window, bg='#2c3e50')
        btn_frame.pack(pady=20)
        
        tk.Button(btn_frame, text="Apply", command=lambda: self.apply_manual_input(input_window),
                 bg='#3498db', fg='white', font=('Arial', 10, 'bold'),
                 padx=20, pady=10).pack(side=tk.LEFT, padx=10)
        
        tk.Button(btn_frame, text="Cancel", command=input_window.destroy,
                 bg='#e74c3c', fg='white', font=('Arial', 10, 'bold'),
                 padx=20, pady=10).pack(side=tk.LEFT, padx=10)
    
    def apply_manual_input(self, window):
        try:
            # Read Matrix A
            for i in range(len(self.matrix_a)):
                for j in range(len(self.matrix_a[0])):
                    self.matrix_a[i][j] = int(self.a_entries[i][j].get())
            
            # Read Matrix B
            for i in range(len(self.matrix_b)):
                for j in range(len(self.matrix_b[0])):
                    self.matrix_b[i][j] = int(self.b_entries[i][j].get())
            
            self.display_matrices()
            window.destroy()
            self.update_info("Matrices updated successfully!")
        except ValueError:
            messagebox.showerror("Error", "Please enter valid integers")
    
    def display_matrices(self):
        self.display_matrix(self.matrix_a_canvas, self.matrix_a, '#3498db')
        self.display_matrix(self.matrix_b_canvas, self.matrix_b, '#3498db')
        self.result_canvas.delete("all")
    
    def display_matrix(self, canvas, matrix, color):
        canvas.delete("all")
        if not matrix:
            return
        
        rows = len(matrix)
        cols = len(matrix[0])
        
        cell_width = min(180 // cols, 50)
        cell_height = min(180 // rows, 50)
        
        start_x = (200 - cols * cell_width) // 2
        start_y = (200 - rows * cell_height) // 2
        
        for i in range(rows):
            for j in range(cols):
                x0 = start_x + j * cell_width
                y0 = start_y + i * cell_height
                x1 = x0 + cell_width
                y1 = y0 + cell_height
                
                canvas.create_rectangle(x0, y0, x1, y1, fill='#2c3e50', outline=color)
                canvas.create_text((x0 + x1)//2, (y0 + y1)//2, 
                                 text=str(matrix[i][j]), fill='white',
                                 font=('Arial', 10, 'bold'))
    
    def display_result_matrix(self, matrix, highlighted_cell=None):
        self.result_canvas.delete("all")
        if not matrix:
            return
        
        rows = len(matrix)
        cols = len(matrix[0])
        
        cell_width = min(180 // cols, 50)
        cell_height = min(180 // rows, 50)
        
        start_x = (200 - cols * cell_width) // 2
        start_y = (200 - rows * cell_height) // 2
        
        for i in range(rows):
            for j in range(cols):
                x0 = start_x + j * cell_width
                y0 = start_y + i * cell_height
                x1 = x0 + cell_width
                y1 = y0 + cell_height
                
                color = '#2ecc71' if (i, j) == highlighted_cell else '#2c3e50'
                canvas_color = '#27ae60' if (i, j) == highlighted_cell else '#2ecc71'
                
                self.result_canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline=canvas_color)
                self.result_canvas.create_text((x0 + x1)//2, (y0 + y1)//2,
                                             text=str(matrix[i][j]), fill='white',
                                             font=('Arial', 10, 'bold'))
    
    def start_multiplication(self):
        if not self.matrix_a or not self.matrix_b:
            messagebox.showerror("Error", "Please generate matrices first")
            return
        
        if len(self.matrix_a[0]) != len(self.matrix_b):
            messagebox.showerror("Error", "Matrix dimensions are incompatible for multiplication")
            return
        
        self.steps = []
        self.current_step = 0
        
        thread = Thread(target=self.perform_multiplication)
        thread.daemon = True
        thread.start()
    
    def perform_multiplication(self):
        m = len(self.matrix_a)
        n = len(self.matrix_a[0])
        p = len(self.matrix_b[0])
        
        result = [[0] * p for _ in range(m)]
        
        # Standard matrix multiplication
        for i in range(m):
            for j in range(p):
                cell_sum = 0
                for k in range(n):
                    cell_sum += self.matrix_a[i][k] * self.matrix_b[k][j]
                    
                    # Record step
                    step = {
                        'i': i, 'j': j, 'k': k,
                        'a_val': self.matrix_a[i][k],
                        'b_val': self.matrix_b[k][j],
                        'partial_sum': cell_sum,
                        'result': [row[:] for row in result]
                    }
                    step['result'][i][j] = cell_sum
                    self.steps.append(step)
                
                result[i][j] = cell_sum
        
        self.result_matrix = result
        
        # Display final result
        self.display_result_matrix(result)
        self.update_info(f"Multiplication completed!\nResult matrix: {m}x{p}\nTotal operations: {m*p*n}")
    
    def step_forward(self):
        if self.current_step < len(self.steps):
            step = self.steps[self.current_step]
            
            # Update info
            info = f"Step {self.current_step + 1}/{len(self.steps)}\n"
            info += f"Calculating cell [{step['i']+1},{step['j']+1}]\n"
            info += f"Multiplying: A[{step['i']+1},{step['k']+1}] = {step['a_val']} × "
            info += f"B[{step['k']+1},{step['j']+1}] = {step['b_val']}\n"
            info += f"Partial sum: {step['partial_sum']}"
            self.update_info(info)
            
            # Display result with highlighted cell
            self.display_result_matrix(step['result'], (step['i'], step['j']))
            
            self.current_step += 1
    
    def step_backward(self):
        if self.current_step > 0:
            self.current_step -= 1
            if self.current_step > 0:
                step = self.steps[self.current_step - 1]
                self.display_result_matrix(step['result'], (step['i'], step['j']))
            else:
                self.result_canvas.delete("all")
            
            self.update_info(f"Step {self.current_step}/{len(self.steps)}")
    
    def reset_visualization(self):
        self.steps = []
        self.current_step = 0
        self.result_canvas.delete("all")
        self.update_info("Visualization reset")
    
    def update_info(self, message):
        self.info_text.config(state=tk.NORMAL)
        self.info_text.delete(1.0, tk.END)
        self.info_text.insert(tk.END, message + "\n")
        self.info_text.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    app = MatrixMultiplicationVisualizer(root)
    root.mainloop()