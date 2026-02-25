import tkinter as tk
from tkinter import ttk, messagebox
import random
import math
import time
from threading import Thread

class HeapSortVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Heap Sort Algorithm Visualizer")
        self.root.geometry("1200x800")
        self.root.configure(bg='#2c3e50')
        
        self.array = []
        self.heap_array = []
        self.speed = 50
        self.array_size = 15  # Smaller for heap visualization
        self.comparisons = 0
        self.swaps = 0
        self.steps = []
        self.current_step = 0
        self.is_heapified = False
        
        self.create_widgets()
        self.generate_new_array()
    
    def create_widgets(self):
        # Title
        title_label = tk.Label(self.root, text="Heap Sort Algorithm Visualizer", 
                              font=('Arial', 24, 'bold'), bg='#2c3e50', fg='#ecf0f1')
        title_label.pack(pady=20)
        
        # Control Panel
        control_frame = tk.Frame(self.root, bg='#34495e', relief=tk.RAISED, borderwidth=2)
        control_frame.pack(pady=10, padx=20, fill=tk.X)
        
        # Top control row
        top_control = tk.Frame(control_frame, bg='#34495e')
        top_control.pack(pady=10)
        
        # Array size control
        tk.Label(top_control, text="Array Size:", bg='#34495e', fg='white',
                font=('Arial', 10)).grid(row=0, column=0, padx=5)
        self.size_slider = tk.Scale(top_control, from_=5, to=20, orient=tk.HORIZONTAL,
                                   length=150, bg='#34495e', fg='white', 
                                   highlightthickness=0, troughcolor='#2c3e50')
        self.size_slider.set(15)
        self.size_slider.grid(row=0, column=1, padx=5)
        
        # Speed control
        tk.Label(top_control, text="Speed:", bg='#34495e', fg='white',
                font=('Arial', 10)).grid(row=0, column=2, padx=5)
        self.speed_slider = tk.Scale(top_control, from_=10, to=200, orient=tk.HORIZONTAL,
                                    length=150, bg='#34495e', fg='white',
                                    highlightthickness=0, troughcolor='#2c3e50')
        self.speed_slider.set(50)
        self.speed_slider.grid(row=0, column=3, padx=5)
        
        # Buttons Frame
        button_frame = tk.Frame(control_frame, bg='#34495e')
        button_frame.pack(pady=10)
        
        # Create buttons with different colors for different actions
        buttons = [
            ("🔢 New Array", self.generate_new_array, '#3498db'),
            ("⚡ Build Max Heap", self.build_max_heap, '#9b59b6'),
            ("📊 Heap Sort", self.start_heap_sort, '#2ecc71'),
            ("⏭ Next Step", self.next_step, '#f39c12'),
            ("🔄 Reset", self.reset_visualization, '#e74c3c'),
            ("📝 Manual Input", self.manual_input, '#1abc9c')
        ]
        
        for i, (text, command, color) in enumerate(buttons):
            btn = tk.Button(button_frame, text=text, command=command,
                          bg=color, fg='white', font=('Arial', 10, 'bold'),
                          padx=15, pady=8, relief=tk.RAISED, borderwidth=2)
            btn.grid(row=0, column=i, padx=5)
        
        # Statistics Frame
        stats_frame = tk.Frame(control_frame, bg='#2c3e50')
        stats_frame.pack(pady=10)
        
        self.stats_labels = {}
        stats = [
            ("Comparisons:", "comparisons"),
            ("Swaps:", "swaps"),
            ("Array Size:", "size"),
            ("Time Complexity:", "complexity"),
            ("Space Complexity:", "space_complexity")
        ]
        
        for i, (label_text, key) in enumerate(stats):
            tk.Label(stats_frame, text=label_text, bg='#2c3e50', fg='#bdc3c7',
                    font=('Arial', 10)).grid(row=0, column=i*2, padx=5)
            
            self.stats_labels[key] = tk.Label(stats_frame, text="0", bg='#2c3e50',
                                             fg='#ecf0f1', font=('Arial', 10, 'bold'))
            self.stats_labels[key].grid(row=0, column=i*2+1, padx=5)
        
        # Main Visualization Area
        vis_frame = tk.Frame(self.root, bg='#2c3e50')
        vis_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Array Visualization (left)
        array_frame = tk.LabelFrame(vis_frame, text="Array Visualization", 
                                   bg='#34495e', fg='white', font=('Arial', 12, 'bold'))
        array_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        self.array_canvas = tk.Canvas(array_frame, bg='#1a1a2e', highlightthickness=0)
        self.array_canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Heap Tree Visualization (right)
        heap_frame = tk.LabelFrame(vis_frame, text="Heap Tree Visualization", 
                                  bg='#34495e', fg='white', font=('Arial', 12, 'bold'))
        heap_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        self.heap_canvas = tk.Canvas(heap_frame, bg='#1a1a2e', highlightthickness=0)
        self.heap_canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Info Panel
        info_frame = tk.Frame(self.root, bg='#34495e')
        info_frame.pack(fill=tk.X, padx=20, pady=10)
        
        self.info_text = tk.Text(info_frame, height=4, bg='#2c3e50', fg='white',
                                font=('Consolas', 10), relief=tk.FLAT)
        self.info_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.info_text.insert(tk.END, "Welcome to Heap Sort Visualizer!\n")
        self.info_text.insert(tk.END, "1. Generate a new array or input manually\n")
        self.info_text.insert(tk.END, "2. Click 'Build Max Heap' to create heap structure\n")
        self.info_text.insert(tk.END, "3. Click 'Heap Sort' to sort the array\n")
        self.info_text.config(state=tk.DISABLED)
        
        # Status Bar
        self.status_bar = tk.Label(self.root, text="Ready", bg='#34495e', fg='white',
                                  font=('Arial', 10), relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Color Legend
        legend_frame = tk.Frame(self.root, bg='#2c3e50')
        legend_frame.pack(pady=5)
        
        colors = [
            ("#3498db", "Normal Element"),
            ("#9b59b6", "Heapify Operation"),
            ("#2ecc71", "Sorted/Correct Position"),
            ("#e74c3c", "Swapping/Active"),
            ("#f39c12", "Comparing"),
            ("#1abc9c", "Root Node")
        ]
        
        for color, text in colors:
            frame = tk.Frame(legend_frame, bg='#2c3e50')
            frame.pack(side=tk.LEFT, padx=10)
            tk.Canvas(frame, width=20, height=20, bg=color, highlightthickness=0).pack(side=tk.LEFT, padx=2)
            tk.Label(frame, text=text, bg='#2c3e50', fg='white', font=('Arial', 8)).pack(side=tk.LEFT)
    
    def update_stats(self):
        self.stats_labels['comparisons'].config(text=str(self.comparisons))
        self.stats_labels['swaps'].config(text=str(self.swaps))
        self.stats_labels['size'].config(text=str(len(self.array)))
        self.stats_labels['complexity'].config(text="O(n log n)")
        self.stats_labels['space_complexity'].config(text="O(1)")
    
    def update_info(self, message):
        self.info_text.config(state=tk.NORMAL)
        self.info_text.delete(1.0, tk.END)
        self.info_text.insert(tk.END, message)
        self.info_text.config(state=tk.DISABLED)
    
    def generate_new_array(self):
        self.array_size = self.size_slider.get()
        self.array = [random.randint(10, 100) for _ in range(self.array_size)]
        self.heap_array = self.array.copy()
        self.comparisons = 0
        self.swaps = 0
        self.steps = []
        self.current_step = 0
        self.is_heapified = False
        
        self.draw_array()
        self.draw_heap()
        self.update_stats()
        self.update_info(f"Generated new array with {self.array_size} random elements")
        self.status_bar.config(text="New array generated")
    
    def manual_input(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Manual Array Input")
        dialog.geometry("500x400")
        dialog.configure(bg='#2c3e50')
        dialog.transient(self.root)
        dialog.grab_set()
        
        tk.Label(dialog, text="Enter array elements (comma-separated):", 
                font=('Arial', 12, 'bold'), bg='#2c3e50', fg='white').pack(pady=20)
        
        # Default value
        default_text = ", ".join(map(str, self.array))
        entry_text = tk.Text(dialog, height=3, width=50, font=('Arial', 10))
        entry_text.pack(pady=10, padx=20)
        entry_text.insert(1.0, default_text)
        
        # Example label
        tk.Label(dialog, text="Example: 45, 12, 67, 23, 89, 34", 
                bg='#2c3e50', fg='#bdc3c7', font=('Arial', 9)).pack()
        
        def apply_input():
            try:
                text = entry_text.get(1.0, tk.END).strip()
                elements = [int(x.strip()) for x in text.split(',') if x.strip()]
                
                if len(elements) < 3:
                    messagebox.showerror("Error", "Array must have at least 3 elements")
                    return
                
                if len(elements) > 20:
                    messagebox.showerror("Error", "Array cannot exceed 20 elements")
                    return
                
                self.array = elements
                self.array_size = len(elements)
                self.size_slider.set(self.array_size)
                self.heap_array = self.array.copy()
                self.comparisons = 0
                self.swaps = 0
                self.steps = []
                self.current_step = 0
                self.is_heapified = False
                
                self.draw_array()
                self.draw_heap()
                self.update_stats()
                self.update_info(f"Manual input: {len(self.array)} elements")
                self.status_bar.config(text="Array updated from manual input")
                
                dialog.destroy()
                
            except ValueError:
                messagebox.showerror("Error", "Please enter valid integers separated by commas")
        
        button_frame = tk.Frame(dialog, bg='#2c3e50')
        button_frame.pack(pady=20)
        
        tk.Button(button_frame, text="Apply", command=apply_input,
                 bg='#2ecc71', fg='white', font=('Arial', 10, 'bold'),
                 padx=20, pady=8).pack(side=tk.LEFT, padx=10)
        
        tk.Button(button_frame, text="Cancel", command=dialog.destroy,
                 bg='#e74c3c', fg='white', font=('Arial', 10, 'bold'),
                 padx=20, pady=8).pack(side=tk.LEFT, padx=10)
    
    def draw_array(self, highlight_indices=None, highlight_color=None):
        self.array_canvas.delete("all")
        
        if not self.array:
            return
        
        canvas_width = self.array_canvas.winfo_width() or 500
        canvas_height = self.array_canvas.winfo_height() or 300
        
        bar_width = (canvas_width - 40) / len(self.array)
        max_val = max(self.array)
        
        for i, value in enumerate(self.array):
            x0 = 20 + i * bar_width
            y0 = canvas_height - 20 - (value / max_val * (canvas_height - 100))
            x1 = x0 + bar_width - 2
            y1 = canvas_height - 20
            
            # Determine color
            color = '#3498db'  # Default blue
            
            if highlight_indices and i in highlight_indices:
                color = highlight_color if highlight_color else '#e74c3c'
            elif self.is_heapified and i < len(self.heap_array):
                # Check if element is in sorted position
                if i >= len(self.array) - self.current_step:
                    color = '#2ecc71'  # Green for sorted
            
            # Draw bar
            self.array_canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline='white', width=1)
            
            # Draw value text
            self.array_canvas.create_text(x0 + bar_width/2, y0 - 15,
                                         text=str(value), fill='white',
                                         font=('Arial', 10, 'bold'))
            
            # Draw index
            self.array_canvas.create_text(x0 + bar_width/2, y1 + 15,
                                         text=str(i), fill='#bdc3c7',
                                         font=('Arial', 9))
        
        # Draw title
        self.array_canvas.create_text(canvas_width/2, 20,
                                     text="Array Elements",
                                     fill='white', font=('Arial', 14, 'bold'))
    
    def draw_heap(self, highlight_nodes=None, highlight_color=None):
        self.heap_canvas.delete("all")
        
        if not self.heap_array:
            return
        
        canvas_width = self.heap_canvas.winfo_width() or 500
        canvas_height = self.heap_canvas.winfo_height() or 300
        
        # Tree drawing parameters
        level_height = 80
        node_radius = 25
        
        # Calculate tree levels
        n = len(self.heap_array)
        levels = math.floor(math.log2(n)) + 1
        
        # Draw tree
        for i, value in enumerate(self.heap_array):
            level = math.floor(math.log2(i + 1))
            nodes_in_level = 2 ** level
            position_in_level = i + 1 - 2 ** level
            
            # Calculate position
            x = (canvas_width / (nodes_in_level + 1)) * (position_in_level + 1)
            y = 50 + level * level_height
            
            # Determine color
            color = '#3498db'  # Default blue
            
            if i == 0:  # Root
                color = '#1abc9c'
            
            if highlight_nodes and i in highlight_nodes:
                color = highlight_color if highlight_color else '#e74c3c'
            
            # Draw connecting lines to children
            left_child = 2 * i + 1
            right_child = 2 * i + 2
            
            if left_child < len(self.heap_array):
                child_level = math.floor(math.log2(left_child + 1))
                child_nodes_in_level = 2 ** child_level
                child_position_in_level = left_child + 1 - 2 ** child_level
                
                child_x = (canvas_width / (child_nodes_in_level + 1)) * (child_position_in_level + 1)
                child_y = 50 + child_level * level_height
                
                self.heap_canvas.create_line(x, y + node_radius, child_x, child_y - node_radius,
                                            fill='#7f8c8d', width=2)
            
            if right_child < len(self.heap_array):
                child_level = math.floor(math.log2(right_child + 1))
                child_nodes_in_level = 2 ** child_level
                child_position_in_level = right_child + 1 - 2 ** child_level
                
                child_x = (canvas_width / (child_nodes_in_level + 1)) * (child_position_in_level + 1)
                child_y = 50 + child_level * level_height
                
                self.heap_canvas.create_line(x, y + node_radius, child_x, child_y - node_radius,
                                            fill='#7f8c8d', width=2)
            
            # Draw node circle
            self.heap_canvas.create_oval(x - node_radius, y - node_radius,
                                        x + node_radius, y + node_radius,
                                        fill=color, outline='white', width=2)
            
            # Draw value
            self.heap_canvas.create_text(x, y, text=str(value),
                                        fill='white', font=('Arial', 10, 'bold'))
            
            # Draw index
            self.heap_canvas.create_text(x, y + node_radius + 10, text=f"i={i}",
                                        fill='#bdc3c7', font=('Arial', 8))
        
        # Draw title
        self.heap_canvas.create_text(canvas_width/2, 20,
                                    text="Heap Tree Structure",
                                    fill='white', font=('Arial', 14, 'bold'))
        
        # Draw heap properties
        props_y = 50 + levels * level_height + 20
        props_text = f"Max-Heap Property: {self.check_max_heap()}"
        self.heap_canvas.create_text(canvas_width/2, props_y,
                                    text=props_text,
                                    fill='#2ecc71' if self.is_heapified else '#e74c3c',
                                    font=('Arial', 10, 'bold'))
    
    def check_max_heap(self):
        n = len(self.heap_array)
        for i in range(n):
            left = 2 * i + 1
            right = 2 * i + 2
            
            if left < n and self.heap_array[i] < self.heap_array[left]:
                return False
            if right < n and self.heap_array[i] < self.heap_array[right]:
                return False
        return True
    
    def build_max_heap(self):
        if not self.array:
            messagebox.showwarning("Warning", "Please generate an array first")
            return
        
        self.heap_array = self.array.copy()
        self.steps = []
        self.current_step = 0
        self.comparisons = 0
        self.swaps = 0
        
        thread = Thread(target=self._build_max_heap)
        thread.daemon = True
        thread.start()
    
    def _build_max_heap(self):
        n = len(self.heap_array)
        
        # Build max heap
        for i in range(n // 2 - 1, -1, -1):
            self.heapify(n, i)
            self.root.after(self.speed_slider.get() * 10)
        
        self.is_heapified = True
        self.update_info("Max Heap built successfully!\nParent nodes are always greater than or equal to child nodes.")
        self.status_bar.config(text="Max Heap construction completed")
        self.draw_array()
        self.draw_heap()
        self.update_stats()
    
    def heapify(self, n, i):
        largest = i
        left = 2 * i + 1
        right = 2 * i + 2
        
        # Highlight comparison
        self.comparisons += 1
        self.update_stats()
        
        self.draw_array(highlight_indices=[i, left if left < n else None, right if right < n else None],
                       highlight_color='#f39c12')
        self.draw_heap(highlight_nodes=[i, left if left < n else None, right if right < n else None],
                      highlight_color='#f39c12')
        self.update_info(f"Heapifying node {i} (value: {self.heap_array[i]})\n"
                        f"Comparing with children...")
        self.status_bar.config(text=f"Heapifying node {i}")
        time.sleep(self.speed_slider.get() / 1000)
        
        if left < n and self.heap_array[left] > self.heap_array[largest]:
            largest = left
        
        if right < n and self.heap_array[right] > self.heap_array[largest]:
            largest = right
        
        if largest != i:
            # Highlight swap
            self.swaps += 1
            self.update_stats()
            
            self.draw_array(highlight_indices=[i, largest], highlight_color='#e74c3c')
            self.draw_heap(highlight_nodes=[i, largest], highlight_color='#e74c3c')
            self.update_info(f"Swapping {self.heap_array[i]} (index {i}) with "
                           f"{self.heap_array[largest]} (index {largest})")
            self.status_bar.config(text=f"Swapping elements {i} and {largest}")
            time.sleep(self.speed_slider.get() / 1000)
            
            # Perform swap
            self.heap_array[i], self.heap_array[largest] = self.heap_array[largest], self.heap_array[i]
            
            # Update array to match heap
            if i < len(self.array):
                self.array[i] = self.heap_array[i]
            if largest < len(self.array):
                self.array[largest] = self.heap_array[largest]
            
            # Recursively heapify the affected sub-tree
            self.heapify(n, largest)
        
        # Show heapified node
        self.draw_array(highlight_indices=[i], highlight_color='#9b59b6')
        self.draw_heap(highlight_nodes=[i], highlight_color='#9b59b6')
        self.update_info(f"Node {i} heapified")
        time.sleep(self.speed_slider.get() / 500)
    
    def start_heap_sort(self):
        if not self.is_heapified:
            messagebox.showinfo("Info", "Building Max Heap first...")
            self.build_max_heap()
            # Wait a bit for heap to build
            self.root.after(1000, self._start_heap_sort_delayed)
        else:
            self._start_heap_sort()
    
    def _start_heap_sort_delayed(self):
        self._start_heap_sort()
    
    def _start_heap_sort(self):
        self.comparisons = 0
        self.swaps = 0
        self.steps = []
        self.current_step = 0
        
        thread = Thread(target=self._perform_heap_sort)
        thread.daemon = True
        thread.start()
    
    def _perform_heap_sort(self):
        n = len(self.heap_array)
        
        # Extract elements from heap one by one
        for i in range(n - 1, 0, -1):
            # Move current root to end
            self.swaps += 1
            self.update_stats()
            
            # Highlight swap
            self.draw_array(highlight_indices=[0, i], highlight_color='#e74c3c')
            self.draw_heap(highlight_nodes=[0, i], highlight_color='#e74c3c')
            self.update_info(f"Moving root ({self.heap_array[0]}) to sorted position {i}")
            self.status_bar.config(text=f"Swapping root with element {i}")
            time.sleep(self.speed_slider.get() / 500)
            
            # Perform swap
            self.heap_array[0], self.heap_array[i] = self.heap_array[i], self.heap_array[0]
            
            # Update array
            self.array[0] = self.heap_array[0]
            self.array[i] = self.heap_array[i]
            
            # Mark sorted element
            self.array[i] = self.heap_array[i]
            self.draw_array(highlight_indices=[i], highlight_color='#2ecc71')
            self.update_info(f"Element {self.heap_array[i]} now in sorted position {i}")
            time.sleep(self.speed_slider.get() / 500)
            
            # Call max heapify on the reduced heap
            self.heapify(i, 0)
        
        # Mark first element as sorted
        self.draw_array(highlight_indices=[0], highlight_color='#2ecc71')
        self.update_info("Heap Sort completed!\nArray is now fully sorted.")
        self.status_bar.config(text="Heap Sort completed - Array is sorted")
        
        # Final visualization
        for i in range(len(self.array)):
            self.draw_array(highlight_indices=list(range(i+1)), highlight_color='#2ecc71')
            time.sleep(self.speed_slider.get() / 1000)
        
        self.update_stats()
    
    def next_step(self):
        if not self.steps:
            messagebox.showinfo("Info", "No steps recorded. Run an operation first.")
            return
        
        if self.current_step < len(self.steps):
            step = self.steps[self.current_step]
            # Execute step visualization
            self.current_step += 1
        else:
            messagebox.showinfo("Info", "All steps completed")
    
    def reset_visualization(self):
        self.array = [random.randint(10, 100) for _ in range(self.array_size)]
        self.heap_array = self.array.copy()
        self.comparisons = 0
        self.swaps = 0
        self.steps = []
        self.current_step = 0
        self.is_heapified = False
        
        self.draw_array()
        self.draw_heap()
        self.update_stats()
        self.update_info("Visualization reset to initial state")
        self.status_bar.config(text="Reset - Ready for new operations")

if __name__ == "__main__":
    root = tk.Tk()
    app = HeapSortVisualizer(root)
    root.mainloop()