import tkinter as tk
from tkinter import ttk, messagebox
import random
import time
from threading import Thread

class LinearSortingVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Linear Sorting Algorithms Visualizer")
        self.root.geometry("1000x700")
        self.root.configure(bg='#2c3e50')
        
        self.array = []
        self.speed = 50
        self.array_size = 30
        self.create_widgets()
        self.generate_new_array()
    
    def create_widgets(self):
        # Title
        title_label = tk.Label(self.root, text="Linear Sorting Algorithms", 
                              font=('Arial', 24, 'bold'), bg='#2c3e50', fg='#ecf0f1')
        title_label.pack(pady=20)
        
        # Control Frame
        control_frame = tk.Frame(self.root, bg='#34495e')
        control_frame.pack(pady=10)
        
        # Array controls
        tk.Label(control_frame, text="Array Size:", bg='#34495e', fg='white').grid(row=0, column=0, padx=5)
        self.size_slider = tk.Scale(control_frame, from_=10, to=100, orient=tk.HORIZONTAL,
                                   bg='#34495e', fg='white', highlightthickness=0)
        self.size_slider.set(30)
        self.size_slider.grid(row=0, column=1, padx=5)
        
        tk.Label(control_frame, text="Speed:", bg='#34495e', fg='white').grid(row=0, column=2, padx=5)
        self.speed_slider = tk.Scale(control_frame, from_=10, to=200, orient=tk.HORIZONTAL,
                                    bg='#34495e', fg='white', highlightthickness=0)
        self.speed_slider.set(50)
        self.speed_slider.grid(row=0, column=3, padx=5)
        
        # Buttons
        button_frame = tk.Frame(self.root, bg='#2c3e50')
        button_frame.pack(pady=10)
        
        buttons = [
            ("Generate New Array", self.generate_new_array),
            ("Bubble Sort", lambda: self.start_sorting("bubble")),
            ("Selection Sort", lambda: self.start_sorting("selection")),
            ("Insertion Sort", lambda: self.start_sorting("insertion")),
            ("Quick Sort", lambda: self.start_sorting("quick")),
            ("Merge Sort", lambda: self.start_sorting("merge"))
        ]
        
        for text, command in buttons:
            btn = tk.Button(button_frame, text=text, command=command,
                          bg='#3498db', fg='white', font=('Arial', 10, 'bold'),
                          padx=20, pady=10, relief=tk.RAISED, borderwidth=3)
            btn.pack(side=tk.LEFT, padx=5)
        
        # Canvas for visualization
        self.canvas = tk.Canvas(self.root, width=950, height=400, bg='#1a1a2e')
        self.canvas.pack(pady=20)
        
        # Status bar
        self.status_label = tk.Label(self.root, text="Ready", bg='#2c3e50', 
                                    fg='#bdc3c7', font=('Arial', 12))
        self.status_label.pack(pady=10)
        
        # Time complexity info
        info_frame = tk.Frame(self.root, bg='#34495e')
        info_frame.pack(pady=10)
        
        complexities = [
            "Bubble Sort: O(n²)",
            "Selection Sort: O(n²)", 
            "Insertion Sort: O(n²)",
            "Quick Sort: O(n log n)",
            "Merge Sort: O(n log n)"
        ]
        
        for i, text in enumerate(complexities):
            tk.Label(info_frame, text=text, bg='#34495e', fg='#ecf0f1', 
                    font=('Arial', 10)).grid(row=0, column=i, padx=10)
    
    def generate_new_array(self):
        self.array_size = self.size_slider.get()
        self.array = [random.randint(10, 350) for _ in range(self.array_size)]
        self.draw_array()
        self.status_label.config(text="New array generated")
    
    def draw_array(self, color_array=None):
        self.canvas.delete("all")
        canvas_width = 950
        canvas_height = 400
        bar_width = canvas_width / len(self.array)
        
        max_val = max(self.array)
        
        for i, height in enumerate(self.array):
            x0 = i * bar_width
            y0 = canvas_height - (height / max_val * 350)
            x1 = (i + 1) * bar_width - 2
            y1 = canvas_height
            
            color = '#3498db'
            if color_array:
                color = color_array[i]
            
            self.canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline='')
        
        self.root.update()
    
    def start_sorting(self, algorithm):
        self.speed = 200 - self.speed_slider.get()
        self.status_label.config(text=f"Running {algorithm.replace('_', ' ').title()}...")
        
        thread = Thread(target=lambda: self.sort_array(algorithm))
        thread.daemon = True
        thread.start()
    
    def sort_array(self, algorithm):
        if algorithm == "bubble":
            self.bubble_sort()
        elif algorithm == "selection":
            self.selection_sort()
        elif algorithm == "insertion":
            self.insertion_sort()
        elif algorithm == "quick":
            self.quick_sort(0, len(self.array)-1)
        elif algorithm == "merge":
            self.merge_sort(0, len(self.array)-1)
        
        self.status_label.config(text="Sorting completed!")
        self.draw_array(['#2ecc71'] * len(self.array))
    
    def bubble_sort(self):
        n = len(self.array)
        for i in range(n):
            for j in range(0, n-i-1):
                if self.array[j] > self.array[j+1]:
                    self.array[j], self.array[j+1] = self.array[j+1], self.array[j]
                    colors = ['#e74c3c' if x == j or x == j+1 else '#3498db' for x in range(n)]
                    self.draw_array(colors)
                    time.sleep(self.speed / 1000)
    
    def selection_sort(self):
        n = len(self.array)
        for i in range(n):
            min_idx = i
            for j in range(i+1, n):
                if self.array[j] < self.array[min_idx]:
                    min_idx = j
            
            self.array[i], self.array[min_idx] = self.array[min_idx], self.array[i]
            colors = ['#e74c3c' if x == i or x == min_idx else '#3498db' for x in range(n)]
            self.draw_array(colors)
            time.sleep(self.speed / 1000)
    
    def insertion_sort(self):
        n = len(self.array)
        for i in range(1, n):
            key = self.array[i]
            j = i-1
            while j >= 0 and key < self.array[j]:
                self.array[j+1] = self.array[j]
                j -= 1
            self.array[j+1] = key
            
            colors = ['#e74c3c' if x == i or x == j+1 else '#3498db' for x in range(n)]
            self.draw_array(colors)
            time.sleep(self.speed / 1000)
    
    def quick_sort(self, low, high):
        if low < high:
            pi = self.partition(low, high)
            self.quick_sort(low, pi-1)
            self.quick_sort(pi+1, high)
    
    def partition(self, low, high):
        pivot = self.array[high]
        i = low - 1
        
        for j in range(low, high):
            if self.array[j] <= pivot:
                i += 1
                self.array[i], self.array[j] = self.array[j], self.array[i]
        
        self.array[i+1], self.array[high] = self.array[high], self.array[i+1]
        
        colors = ['#e74c3c' if x == i+1 or x == high else '#3498db' for x in range(len(self.array))]
        self.draw_array(colors)
        time.sleep(self.speed / 1000)
        
        return i + 1
    
    def merge_sort(self, l, r):
        if l < r:
            m = (l + r) // 2
            self.merge_sort(l, m)
            self.merge_sort(m+1, r)
            self.merge(l, m, r)
    
    def merge(self, l, m, r):
        n1 = m - l + 1
        n2 = r - m
        
        L = self.array[l:m+1]
        R = self.array[m+1:r+1]
        
        i = j = 0
        k = l
        
        while i < n1 and j < n2:
            if L[i] <= R[j]:
                self.array[k] = L[i]
                i += 1
            else:
                self.array[k] = R[j]
                j += 1
            
            colors = ['#e74c3c' if x == k else '#3498db' for x in range(len(self.array))]
            self.draw_array(colors)
            time.sleep(self.speed / 2000)
            k += 1
        
        while i < n1:
            self.array[k] = L[i]
            colors = ['#e74c3c' if x == k else '#3498db' for x in range(len(self.array))]
            self.draw_array(colors)
            time.sleep(self.speed / 2000)
            i += 1
            k += 1
        
        while j < n2:
            self.array[k] = R[j]
            colors = ['#e74c3c' if x == k else '#3498db' for x in range(len(self.array))]
            self.draw_array(colors)
            time.sleep(self.speed / 2000)
            j += 1
            k += 1

if __name__ == "__main__":
    root = tk.Tk()
    app = LinearSortingVisualizer(root)
    root.mainloop()