import tkinter as tk
from tkinter import ttk, messagebox
import random
import math
import time
from threading import Thread
import heapq

class MSTVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Minimum Spanning Tree Visualizer")
        self.root.geometry("1200x800")
        self.root.configure(bg='#2c3e50')
        
        self.nodes = []
        self.edges = []
        self.selected_algorithm = "prim"
        self.node_radius = 20
        self.node_counter = 0
        self.is_drawing = False
        self.start_node = None
        
        self.create_widgets()
    
    def create_widgets(self):
        # Title
        title_label = tk.Label(self.root, text="Minimum Spanning Tree Visualizer", 
                              font=('Arial', 24, 'bold'), bg='#2c3e50', fg='#ecf0f1')
        title_label.pack(pady=20)
        
        # Main frame
        main_frame = tk.Frame(self.root, bg='#2c3e50')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Control panel
        control_frame = tk.Frame(main_frame, bg='#34495e', relief=tk.RAISED, borderwidth=2)
        control_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        
        # Graph controls
        graph_frame = tk.LabelFrame(control_frame, text="Graph Controls", 
                                   bg='#34495e', fg='white', font=('Arial', 12, 'bold'))
        graph_frame.pack(pady=10, padx=10, fill=tk.X)
        
        control_buttons = [
            ("Add Node Mode", self.enable_add_node_mode),
            ("Add Edge Mode", self.enable_add_edge_mode),
            ("Generate Random Graph", self.generate_random_graph),
            ("Clear Graph", self.clear_graph)
        ]
        
        for text, command in control_buttons:
            btn = tk.Button(graph_frame, text=text, command=command,
                          bg='#3498db', fg='white', font=('Arial', 10),
                          padx=10, pady=8, relief=tk.RAISED, borderwidth=2)
            btn.pack(pady=5, fill=tk.X)
        
        # Node count
        count_frame = tk.Frame(graph_frame, bg='#34495e')
        count_frame.pack(pady=5)
        tk.Label(count_frame, text="Node Count:", bg='#34495e', fg='white').pack(side=tk.LEFT)
        self.node_count_label = tk.Label(count_frame, text="0", bg='#34495e', 
                                        fg='#3498db', font=('Arial', 10, 'bold'))
        self.node_count_label.pack(side=tk.LEFT, padx=5)
        
        # Algorithm selection
        algo_frame = tk.LabelFrame(control_frame, text="MST Algorithm", 
                                  bg='#34495e', fg='white', font=('Arial', 12, 'bold'))
        algo_frame.pack(pady=10, padx=10, fill=tk.X)
        
        self.algo_var = tk.StringVar(value="prim")
        
        algorithms = [
            ("Prim's Algorithm", "prim"),
            ("Kruskal's Algorithm", "kruskal")
        ]
        
        for text, value in algorithms:
            rb = tk.Radiobutton(algo_frame, text=text, variable=self.algo_var,
                              value=value, bg='#34495e', fg='white',
                              selectcolor='#2c3e50', activebackground='#34495e')
            rb.pack(anchor=tk.W, pady=2)
        
        # Run buttons
        run_frame = tk.Frame(control_frame, bg='#34495e')
        run_frame.pack(pady=10, padx=10, fill=tk.X)
        
        tk.Button(run_frame, text="Find MST", command=self.find_mst,
                 bg='#2ecc71', fg='white', font=('Arial', 12, 'bold'),
                 padx=20, pady=10).pack(fill=tk.X)
        
        tk.Button(run_frame, text="Step by Step", command=self.step_mst,
                 bg='#f39c12', fg='white', font=('Arial', 12, 'bold'),
                 padx=20, pady=10).pack(fill=tk.X, pady=5)
        
        tk.Button(run_frame, text="Reset MST", command=self.reset_mst,
                 bg='#e74c3c', fg='white', font=('Arial', 12, 'bold'),
                 padx=20, pady=10).pack(fill=tk.X)
        
        # Statistics
        stats_frame = tk.LabelFrame(control_frame, text="Statistics", 
                                   bg='#34495e', fg='white', font=('Arial', 12, 'bold'))
        stats_frame.pack(pady=10, padx=10, fill=tk.X)
        
        self.stats_text = tk.Text(stats_frame, height=8, width=25, bg='#2c3e50',
                                 fg='white', font=('Consolas', 10), relief=tk.FLAT)
        self.stats_text.pack(pady=5, padx=5)
        self.update_stats()
        
        # Canvas for graph
        self.canvas = tk.Canvas(main_frame, bg='#1a1a2e', highlightthickness=1,
                               highlightbackground='#34495e')
        self.canvas.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Bind canvas events
        self.canvas.bind("<Button-1>", self.canvas_click)
        self.canvas.bind("<Motion>", self.canvas_motion)
        
        # Status bar
        self.status_bar = tk.Label(self.root, text="Ready - Click 'Add Node Mode' to start", 
                                  bg='#34495e', fg='white', font=('Arial', 10),
                                  relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Set initial mode
        self.current_mode = None
        self.enable_add_node_mode()
    
    def enable_add_node_mode(self):
        self.current_mode = "add_node"
        self.status_bar.config(text="Mode: Add Node - Click on canvas to add nodes")
    
    def enable_add_edge_mode(self):
        if len(self.nodes) < 2:
            messagebox.showwarning("Warning", "Need at least 2 nodes to add edges")
            self.enable_add_node_mode()
            return
        
        self.current_mode = "add_edge"
        self.start_node = None
        self.status_bar.config(text="Mode: Add Edge - Click first node, then second node")
    
    def canvas_click(self, event):
        x, y = event.x, event.y
        
        if self.current_mode == "add_node":
            # Check if too close to existing node
            for node in self.nodes:
                dist = math.sqrt((node['x'] - x)**2 + (node['y'] - y)**2)
                if dist < self.node_radius * 2:
                    messagebox.showwarning("Warning", "Nodes are too close together")
                    return
            
            node_id = len(self.nodes)
            self.nodes.append({
                'id': node_id,
                'x': x,
                'y': y,
                'label': chr(65 + node_id) if node_id < 26 else f"N{node_id}",
                'color': '#3498db'
            })
            self.draw_graph()
            self.update_stats()
            
        elif self.current_mode == "add_edge":
            clicked_node = self.get_node_at_position(x, y)
            
            if clicked_node is not None:
                if self.start_node is None:
                    self.start_node = clicked_node
                    self.status_bar.config(text=f"Adding Edge: Selected node {clicked_node['label']}. Click destination node.")
                else:
                    if clicked_node == self.start_node:
                        messagebox.showwarning("Warning", "Cannot create edge to the same node")
                        self.start_node = None
                        return
                    
                    # Check if edge already exists
                    for edge in self.edges:
                        if (edge['from'] == self.start_node['id'] and edge['to'] == clicked_node['id']) or \
                           (edge['from'] == clicked_node['id'] and edge['to'] == self.start_node['id']):
                            messagebox.showwarning("Warning", "Edge already exists")
                            self.start_node = None
                            return
                    
                    # Get weight
                    weight = self.get_edge_weight_dialog()
                    if weight is not None:
                        self.edges.append({
                            'from': self.start_node['id'],
                            'to': clicked_node['id'],
                            'weight': weight,
                            'color': '#95a5a6',
                            'mst': False
                        })
                        self.draw_graph()
                        self.update_stats()
                    
                    self.start_node = None
                    self.status_bar.config(text="Mode: Add Edge - Click first node, then second node")
    
    def get_edge_weight_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Edge Weight")
        dialog.geometry("300x150")
        dialog.configure(bg='#2c3e50')
        dialog.transient(self.root)
        dialog.grab_set()
        
        tk.Label(dialog, text="Enter edge weight:", 
                font=('Arial', 12, 'bold'), bg='#2c3e50', fg='white').pack(pady=20)
        
        weight_var = tk.StringVar(value=str(random.randint(1, 20)))
        entry = tk.Entry(dialog, textvariable=weight_var, font=('Arial', 12),
                        justify='center')
        entry.pack(pady=10)
        entry.select_range(0, tk.END)
        entry.focus_set()
        
        result = []
        
        def on_ok():
            try:
                weight = int(weight_var.get())
                if weight <= 0:
                    raise ValueError
                result.append(weight)
                dialog.destroy()
            except ValueError:
                messagebox.showerror("Error", "Please enter a positive integer")
        
        def on_random():
            weight_var.set(str(random.randint(1, 20)))
        
        button_frame = tk.Frame(dialog, bg='#2c3e50')
        button_frame.pack(pady=10)
        
        tk.Button(button_frame, text="Random", command=on_random,
                 bg='#3498db', fg='white').pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="OK", command=on_ok,
                 bg='#2ecc71', fg='white').pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Cancel", command=dialog.destroy,
                 bg='#e74c3c', fg='white').pack(side=tk.LEFT, padx=5)
        
        dialog.wait_window()
        return result[0] if result else None
    
    def canvas_motion(self, event):
        if self.current_mode == "add_edge" and self.start_node:
            self.draw_graph()
            self.canvas.create_line(self.start_node['x'], self.start_node['y'],
                                   event.x, event.y, fill='#e74c3c', width=2,
                                   dash=(5, 2))
    
    def get_node_at_position(self, x, y):
        for node in self.nodes:
            dist = math.sqrt((node['x'] - x)**2 + (node['y'] - y)**2)
            if dist <= self.node_radius:
                return node
        return None
    
    def generate_random_graph(self):
        self.clear_graph()
        
        num_nodes = random.randint(6, 12)
        canvas_width = self.canvas.winfo_width() or 800
        canvas_height = self.canvas.winfo_height() or 600
        
        # Generate nodes
        for i in range(num_nodes):
            attempts = 0
            while attempts < 100:
                x = random.randint(self.node_radius, canvas_width - self.node_radius)
                y = random.randint(self.node_radius, canvas_height - self.node_radius)
                
                # Check minimum distance
                too_close = False
                for node in self.nodes:
                    dist = math.sqrt((node['x'] - x)**2 + (node['y'] - y)**2)
                    if dist < self.node_radius * 3:
                        too_close = True
                        break
                
                if not too_close:
                    self.nodes.append({
                        'id': i,
                        'x': x,
                        'y': y,
                        'label': chr(65 + i) if i < 26 else f"N{i}",
                        'color': '#3498db'
                    })
                    break
                attempts += 1
        
        # Generate edges (create a connected graph)
        for i in range(num_nodes):
            # Connect to random other nodes
            num_edges = random.randint(1, 3)
            connections = random.sample([j for j in range(num_nodes) if j != i], 
                                       min(num_edges, num_nodes-1))
            
            for j in connections:
                if i < j:  # Avoid duplicate edges
                    weight = random.randint(1, 20)
                    
                    # Check if edge already exists
                    exists = False
                    for edge in self.edges:
                        if (edge['from'] == i and edge['to'] == j) or \
                           (edge['from'] == j and edge['to'] == i):
                            exists = True
                            break
                    
                    if not exists:
                        self.edges.append({
                            'from': i,
                            'to': j,
                            'weight': weight,
                            'color': '#95a5a6',
                            'mst': False
                        })
        
        self.draw_graph()
        self.update_stats()
        self.status_bar.config(text=f"Generated random graph with {num_nodes} nodes")
    
    def clear_graph(self):
        self.nodes = []
        self.edges = []
        self.canvas.delete("all")
        self.update_stats()
        self.status_bar.config(text="Graph cleared")
    
    def draw_graph(self):
        self.canvas.delete("all")
        
        # Draw edges
        for edge in self.edges:
            from_node = self.nodes[edge['from']]
            to_node = self.nodes[edge['to']]
            
            # Calculate line position
            dx = to_node['x'] - from_node['x']
            dy = to_node['y'] - from_node['y']
            dist = math.sqrt(dx*dx + dy*dy)
            
            if dist > 0:
                # Adjust start and end points to node boundaries
                start_x = from_node['x'] + (dx * self.node_radius / dist)
                start_y = from_node['y'] + (dy * self.node_radius / dist)
                end_x = to_node['x'] - (dx * self.node_radius / dist)
                end_y = to_node['y'] - (dy * self.node_radius / dist)
                
                # Draw edge line
                line_width = 3 if edge['mst'] else 2
                line_color = '#2ecc71' if edge['mst'] else edge['color']
                self.canvas.create_line(start_x, start_y, end_x, end_y,
                                       fill=line_color, width=line_width)
                
                # Draw weight
                mid_x = (start_x + end_x) / 2
                mid_y = (start_y + end_y) / 2
                
                # Offset weight label perpendicular to edge
                offset = 15
                perp_x = -dy / dist * offset
                perp_y = dx / dist * offset
                
                weight_color = '#2ecc71' if edge['mst'] else 'white'
                self.canvas.create_text(mid_x + perp_x, mid_y + perp_y,
                                       text=str(edge['weight']),
                                       fill=weight_color,
                                       font=('Arial', 10, 'bold'))
        
        # Draw nodes
        for node in self.nodes:
            # Draw node circle
            self.canvas.create_oval(node['x'] - self.node_radius,
                                   node['y'] - self.node_radius,
                                   node['x'] + self.node_radius,
                                   node['y'] + self.node_radius,
                                   fill=node['color'], outline='white', width=2)
            
            # Draw node label
            self.canvas.create_text(node['x'], node['y'],
                                   text=node['label'],
                                   fill='white',
                                   font=('Arial', 12, 'bold'))
    
    def find_mst(self):
        if len(self.nodes) == 0:
            messagebox.showwarning("Warning", "No nodes in graph")
            return
        
        if len(self.edges) == 0:
            messagebox.showwarning("Warning", "No edges in graph")
            return
        
        # Reset all edges to non-MST
        for edge in self.edges:
            edge['mst'] = False
        
        if self.selected_algorithm == "prim":
            self.prim_algorithm()
        else:
            self.kruskal_algorithm()
        
        self.draw_graph()
        self.update_stats()
    
    def prim_algorithm(self):
        if not self.nodes:
            return
        
        visited = set()
        mst_edges = []
        total_weight = 0
        
        # Start with first node
        start_node = 0
        visited.add(start_node)
        
        # Priority queue for edges: (weight, from, to)
        edges_heap = []
        
        # Add edges from start node to heap
        for edge in self.edges:
            if edge['from'] == start_node:
                heapq.heappush(edges_heap, (edge['weight'], edge['from'], edge['to']))
            elif edge['to'] == start_node:
                heapq.heappush(edges_heap, (edge['weight'], edge['to'], edge['from']))
        
        while edges_heap and len(visited) < len(self.nodes):
            weight, u, v = heapq.heappop(edges_heap)
            
            if v not in visited:
                visited.add(v)
                mst_edges.append((u, v, weight))
                total_weight += weight
                
                # Add edges from v to heap
                for edge in self.edges:
                    if edge['from'] == v and edge['to'] not in visited:
                        heapq.heappush(edges_heap, (edge['weight'], edge['from'], edge['to']))
                    elif edge['to'] == v and edge['from'] not in visited:
                        heapq.heappush(edges_heap, (edge['weight'], edge['to'], edge['from']))
        
        # Mark MST edges
        for u, v, weight in mst_edges:
            for edge in self.edges:
                if (edge['from'] == u and edge['to'] == v) or (edge['from'] == v and edge['to'] == u):
                    edge['mst'] = True
                    break
        
        return total_weight
    
    def kruskal_algorithm(self):
        if not self.nodes:
            return 0
        
        # Initialize union-find
        parent = list(range(len(self.nodes)))
        rank = [0] * len(self.nodes)
        
        def find(x):
            if parent[x] != x:
                parent[x] = find(parent[x])
            return parent[x]
        
        def union(x, y):
            root_x = find(x)
            root_y = find(y)
            
            if root_x != root_y:
                if rank[root_x] < rank[root_y]:
                    parent[root_x] = root_y
                elif rank[root_x] > rank[root_y]:
                    parent[root_y] = root_x
                else:
                    parent[root_y] = root_x
                    rank[root_x] += 1
                return True
            return False
        
        # Sort edges by weight
        sorted_edges = sorted(self.edges, key=lambda e: e['weight'])
        
        mst_edges = []
        total_weight = 0
        
        for edge in sorted_edges:
            if union(edge['from'], edge['to']):
                mst_edges.append(edge)
                total_weight += edge['weight']
                
                if len(mst_edges) == len(self.nodes) - 1:
                    break
        
        # Mark MST edges
        for edge in mst_edges:
            edge['mst'] = True
        
        return total_weight
    
    def step_mst(self):
        # Simple step-through visualization
        messagebox.showinfo("Step by Step", 
                          "Step-by-step visualization would show each iteration.\n"
                          "For full visualization, run the complete algorithm.")
    
    def reset_mst(self):
        for edge in self.edges:
            edge['mst'] = False
            edge['color'] = '#95a5a6'
        
        for node in self.nodes:
            node['color'] = '#3498db'
        
        self.draw_graph()
        self.update_stats()
        self.status_bar.config(text="MST reset")
    
    def update_stats(self):
        self.node_count_label.config(text=str(len(self.nodes)))
        
        stats = f"Graph Statistics:\n"
        stats += f"Nodes: {len(self.nodes)}\n"
        stats += f"Edges: {len(self.edges)}\n\n"
        
        mst_edges = sum(1 for edge in self.edges if edge['mst'])
        if mst_edges > 0:
            total_weight = sum(edge['weight'] for edge in self.edges if edge['mst'])
            stats += f"MST Found:\n"
            stats += f"MST Edges: {mst_edges}\n"
            stats += f"Total Weight: {total_weight}\n"
        
        self.stats_text.config(state=tk.NORMAL)
        self.stats_text.delete(1.0, tk.END)
        self.stats_text.insert(tk.END, stats)
        self.stats_text.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    app = MSTVisualizer(root)
    root.mainloop()