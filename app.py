
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.lines import Line2D
import truss2D as tc
import numpy as np

class TrussSolverApp:
    def __init__(self, master):
        # Initialise the main window
        self.master = master
        self.master.title('2D Truss Problem Solver')
        self.master.geometry('960x720')

       # Style configuration for the widgets
        self.style = ttk.Style(self.master)
        self.style.configure('TButton', font=('Arial', 10), borderwidth=1)
        self.style.configure('TLabelFrame', font=('Arial', 12, 'bold'), borderwidth=2)
        self.style.configure('TCanvas', borderwidth=0)
        self.style.configure('TFrame', background='#F0F0F0')

        # Lists to store dynamic entry widgets for user input
        self.coords_entries = []
        self.elements_entries = []
        self.prescribed_entries = []
        self.point_load_entries = []

        # Setup notebook (tab control) for different sections of the application
        self.tab_control = ttk.Notebook(master)

        # Create tabs for input, calculation results, and figure display
        self.tab_input = ttk.Frame(self.tab_control)
        self.tab_calculation = ttk.Frame(self.tab_control)
        self.tab_figure = ttk.Frame(self.tab_control)

        # Add tabs to notebook
        self.tab_control.add(self.tab_input, text='Input')
        self.tab_control.add(self.tab_calculation, text='Calculation')
        self.tab_control.add(self.tab_figure, text='Figure')
        self.tab_control.pack(expand=1, fill='both')

        # Setup UI components for each tab
        self.setup_input_tab()
        self.setup_calculation_tab()
        self.setup_figure_tab()

# -----------------------------------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------------------------------       
        # This method configures the Input tab with widgets to receive user input for nodes, elements, etc.
        # Contains inner functions to handle dynamic addition of input fields based on user requirements.

    def setup_input_tab(self):

        def configure_scroll_region(event):
            self.elements_canvas.configure(scrollregion=self.elements_canvas.bbox("all"))
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))
            self.prescribed_canvas.configure(scrollregion=self.prescribed_canvas.bbox("all"))
            self.point_load_canvas.configure(scrollregion=self.point_load_canvas.bbox("all"))

        def add_node_entry():
            num_nodes_str = self.num_nodes_entry.get()

            if num_nodes_str.strip():
                try:
                    num_nodes = int(num_nodes_str)
                except ValueError:
                    messagebox.showerror("Error", "Please enter a valid number number of nodes.")
                    return

                for entry in self.coords_entries:
                    entry[0].destroy()
                    entry[1].destroy()
                    entry[2].destroy()
                self.coords_entries.clear()

                x_label = tk.Label(self.scrollable_frame, text="    X-axis    ", bg="#E0E0E0")
                x_label.grid(row=0, column=1, padx=5, pady=5, sticky="w")
                y_label = tk.Label(self.scrollable_frame, text="    Y-axis    ", bg="#E0E0E0")
                y_label.grid(row=0, column=2, padx=5, pady=5, sticky="w")

                for i in range(num_nodes):
                    label = tk.Label(self.scrollable_frame, text=f"Node {i + 1}: ", bg="#E0E0E0")
                    label.grid(row=i + 2, column=0, padx=5, pady=5, sticky="w")

                    x_entry = tk.Entry(self.scrollable_frame, width=5)
                    x_entry.grid(row=i + 2, column=1, padx=5, pady=5)

                    y_entry = tk.Entry(self.scrollable_frame, width=5)
                    y_entry.grid(row=i + 2, column=2, padx=5, pady=5)

                    button_node = tk.Button(self.scrollable_frame, text="Add", highlightbackground="#E0E0E0",
                                            highlightcolor="#E0E0E0", command=lambda i=i: store_node_entry(i))
                    button_node.grid(row=i + 2, column=3, padx=5, pady=5)

                    self.coords_entries.append((x_entry, y_entry, button_node))

        def store_node_entry(i):
            x_entry = self.coords_entries[i][0]
            y_entry = self.coords_entries[i][1]
            print(f"Node {i + 1}: x={x_entry.get()}, y={y_entry.get()}")
        
        def add_element_entry():
            num_elements_str = self.num_elements_entry.get()

            if num_elements_str.strip():
                try:
                    num_elements = int(num_elements_str)
                except ValueError:
                    messagebox.showerror("Error", "Please enter a valid number of elements.")
                    return

                for entry in self.elements_entries:
                    entry[0].destroy()
                    entry[1].destroy()
                    entry[2].destroy()
                self.elements_entries.clear()

                x_label = tk.Label(self.elements_scrollable_frame, text="  S. N", bg="#E0E0E0")
                x_label.grid(row=0, column=1, padx=5, pady=5, sticky="w")
                y_label = tk.Label(self.elements_scrollable_frame, text="  E. N", bg="#E0E0E0")
                y_label.grid(row=0, column=2, padx=5, pady=5, sticky="w")
                E_label = tk.Label(self.elements_scrollable_frame, text="   E  ", bg="#E0E0E0")
                E_label.grid(row=0, column=3, padx=5, pady=5, sticky="w")
                A_label = tk.Label(self.elements_scrollable_frame, text="   A  ", bg="#E0E0E0")
                A_label.grid(row=0, column=4, padx=5, pady=5, sticky="w")

                for i in range(num_elements):
                    label = tk.Label(self.elements_scrollable_frame, text=f"Elem {i + 1}: ", bg="#E0E0E0")
                    label.grid(row=i + 2, column=0, padx=2, pady=5, sticky="w")

                    x_entry = tk.Entry(self.elements_scrollable_frame, width=3)
                    x_entry.grid(row=i + 2, column=1, padx=2, pady=5)

                    y_entry = tk.Entry(self.elements_scrollable_frame, width=3)
                    y_entry.grid(row=i + 2, column=2, padx=2, pady=5)

                    E_entry = tk.Entry(self.elements_scrollable_frame, width=3)
                    E_entry.grid(row=i + 2, column=3, padx=2, pady=5)

                    A_entry = tk.Entry(self.elements_scrollable_frame, width=3)
                    A_entry.grid(row=i + 2, column=4, padx=2, pady=5)

                    button_element = tk.Button(self.elements_scrollable_frame, text="Add", highlightbackground="#E0E0E0",
                                            highlightcolor="#E0E0E0", command=lambda i=i: store_elements_entry(i))
                    button_element.grid(row=i + 2, column=5, padx=3, pady=5)

                    self.elements_entries.append((x_entry, y_entry, E_entry, A_entry, button_element))

        def store_elements_entry(i):
            x_entry = self.elements_entries[i][0]
            y_entry = self.elements_entries[i][1]
            E_entry = self.elements_entries[i][2]
            A_entry = self.elements_entries[i][3]
            print(f"Elem {i + 1}: x={x_entry.get()}, y={y_entry.get()}, E={A_entry.get()}, A={E_entry.get()}")


        def add_prescribed_entry():
            num_prescribed_str = self.num_prescribed_entry.get()

            if num_prescribed_str.strip():
                try:
                    num_prescribed = int(num_prescribed_str)
                except ValueError:
                    messagebox.showerror("Error", "Please enter a valid number of prescribed displacements nodes.")
                    return

                for entry in self.prescribed_entries:
                    entry[0].destroy()
                    entry[1].destroy()
                    entry[2].destroy()
                self.prescribed_entries.clear()

                n_label = tk.Label(self.prescribed_scrollable_frame, text="      Node #    ", bg="#E0E0E0")
                n_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
                x_label = tk.Label(self.prescribed_scrollable_frame, text="    X-axis    ", bg="#E0E0E0")
                x_label.grid(row=0, column=1, padx=5, pady=5, sticky="w")
                y_label = tk.Label(self.prescribed_scrollable_frame, text="    Y-axis    ", bg="#E0E0E0")
                y_label.grid(row=0, column=2, padx=5, pady=5, sticky="w")

                for i in range(num_prescribed):
                    n_entry = tk.Entry(self.prescribed_scrollable_frame, width=5)
                    n_entry.grid(row=i + 2, column=0, padx=5, pady=5)

                    x_entry = tk.Entry(self.prescribed_scrollable_frame, width=5)
                    x_entry.grid(row=i + 2, column=1, padx=5, pady=5)

                    y_entry = tk.Entry(self.prescribed_scrollable_frame, width=5)
                    y_entry.grid(row=i + 2, column=2, padx=5, pady=5)

                    button_element = tk.Button(self.prescribed_scrollable_frame, text="Add", highlightbackground="#E0E0E0",
                                            highlightcolor="#E0E0E0", command=lambda i=i: store_prescribed_entry(i))
                    button_element.grid(row=i + 2, column=3, padx=5, pady=5)

                    self.prescribed_entries.append((n_entry, x_entry, y_entry, button_element))

        def store_prescribed_entry(i):
            n_entry = self.prescribed_entries[i][0]
            x_entry = self.prescribed_entries[i][1]
            y_entry = self.prescribed_entries[i][2]
            print(f"Node {n_entry.get()}: x={x_entry.get()}, y={y_entry.get()}")

        def add_point_load_entry():
            num_point_load_str = self.num_point_load_entry.get()

            if num_point_load_str.strip():
                try:
                    num_point_load = int(num_point_load_str)
                except ValueError:
                    messagebox.showerror("Error", "Please enter a valid number of point load.")
                    return

                for entry in self.point_load_entries:
                    entry[0].destroy()
                    entry[1].destroy()
                    entry[2].destroy()
                self.point_load_entries.clear()

                n_label = tk.Label(self.point_load_scrollable_frame, text="      Node #    ", bg="#E0E0E0")
                n_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
                x_label = tk.Label(self.point_load_scrollable_frame, text="   X-axis    ", bg="#E0E0E0")
                x_label.grid(row=0, column=1, padx=5, pady=5, sticky="w")
                y_label = tk.Label(self.point_load_scrollable_frame, text="   Y-axis    ", bg="#E0E0E0")
                y_label.grid(row=0, column=2, padx=5, pady=5, sticky="w")

                for i in range(num_point_load):
                    n_entry = tk.Entry(self.point_load_scrollable_frame, width=5)
                    n_entry.grid(row=i + 2, column=0, padx=5, pady=5)

                    x_entry = tk.Entry(self.point_load_scrollable_frame, width=5)
                    x_entry.grid(row=i + 2, column=1, padx=5, pady=5)

                    y_entry = tk.Entry(self.point_load_scrollable_frame, width=5)
                    y_entry.grid(row=i + 2, column=2, padx=5, pady=5)

                    button_element = tk.Button(self.point_load_scrollable_frame, text="Add", highlightbackground="#E0E0E0",
                                            highlightcolor="#E0E0E0", command=lambda i=i: store_point_load_entry(i))
                    button_element.grid(row=i + 2, column=3, padx=5, pady=5)

                    self.point_load_entries.append((n_entry, x_entry, y_entry, button_element))

        def store_point_load_entry(i):
            n_entry = self.point_load_entries[i][0]
            x_entry = self.point_load_entries[i][1]
            y_entry = self.point_load_entries[i][2]
            print(f"Node {n_entry.get()}: x={x_entry.get()}, y={y_entry.get()}")

        self.frame_elements = tk.LabelFrame(self.tab_input, text="Elements", font="bold", bg="#E0E0E0")
        self.frame_elements.grid(row=0, column=0, padx=50, pady=10, sticky="nsew")
        self.frame_elements.config(bg="#E0E0E0")

        self.num_elements_label = tk.Label(self.frame_elements, text="Enter Total Number of Elements:", bg="#E0E0E0")
        self.num_elements_label.grid(row=0, column=0, padx=1, pady=5, sticky="w")
        self.num_elements_entry = tk.Entry(self.frame_elements, width=10)
        self.num_elements_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        self.elements_canvas = tk.Canvas(self.frame_elements, bg="#E0E0E0")
        self.elements_scrollbar = tk.Scrollbar(self.frame_elements, orient="vertical", command=self.elements_canvas.yview)
        self.elements_scrollable_frame = tk.Frame(self.elements_canvas, bg="#E0E0E0")
        self.elements_canvas.create_window((0, 0), window=self.elements_scrollable_frame, anchor="nw")
        self.elements_canvas.configure(yscrollcommand=self.elements_scrollbar.set)

        self.elements_scrollable_frame.bind("<Configure>", configure_scroll_region)

        self.elements_canvas.grid(row=1, column=0, columnspan=3, sticky="nsew")
        self.elements_scrollbar.grid(row=1, column=3, sticky="ns")

        self.num_elements_entry.bind('<Return>', lambda event=None: add_element_entry())    
        # =============================

        self.frame_nodes = tk.LabelFrame(self.tab_input, text="Nodes", font="bold", bg="#E0E0E0")
        self.frame_nodes.grid(row=1, column=0, padx=50, pady=10,  sticky="nsew")
        self.frame_nodes.config(bg="#E0E0E0")

        self.num_nodes_label = tk.Label(self.frame_nodes, text="Enter Total Number of Nodes:     ", bg="#E0E0E0")
        self.num_nodes_label.grid(row=0, column=0, padx=1, pady=5, sticky="w")
        self.num_nodes_entry = tk.Entry(self.frame_nodes, width=10)
        self.num_nodes_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        self.canvas = tk.Canvas(self.frame_nodes, bg="#E0E0E0")
        self.scrollbar = tk.Scrollbar(self.frame_nodes, orient="vertical", command=self.canvas.yview, bg="#E0E0E0")
        self.scrollable_frame = tk.Frame(self.canvas, bg="#E0E0E0")

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.scrollable_frame.bind("<Configure>", configure_scroll_region)

        self.canvas.grid(row=2, column=0, columnspan=3, sticky="nsew")
        self.scrollbar.grid(row=2, column=3, sticky="ns")

        self.num_nodes_entry.bind('<Return>', lambda event=None: add_node_entry())
        # =============================

        self.frame_prescribed = tk.LabelFrame(self.tab_input, text="Prescribed Displacements", font="bold", bg="#E0E0E0")
        self.frame_prescribed.grid(row=0, column=1, padx=50,  pady=10, sticky="nsew")
        self.frame_prescribed.config(bg="#E0E0E0")

        self.num_prescribed_label = tk.Label(self.frame_prescribed, text="Nodes with Prescribed Displacements:", bg="#E0E0E0")
        self.num_prescribed_label.grid(row=0, column=0, padx=1, pady=5, sticky="w")
        self.num_prescribed_entry = tk.Entry(self.frame_prescribed, width=9)
        self.num_prescribed_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        self.prescribed_canvas = tk.Canvas(self.frame_prescribed, bg="#E0E0E0")
        self.prescribed_scrollbar = tk.Scrollbar(self.frame_prescribed, orient="vertical", command=self.prescribed_canvas.yview, bg="#E0E0E0")
        self.prescribed_scrollable_frame = tk.Frame(self.prescribed_canvas, bg="#E0E0E0")

        self.prescribed_canvas.create_window((0, 0), window=self.prescribed_scrollable_frame, anchor="nw")
        self.prescribed_canvas.configure(yscrollcommand=self.prescribed_scrollbar.set)

        self.prescribed_scrollable_frame.bind("<Configure>", configure_scroll_region)

        self.prescribed_canvas.grid(row=1, column=0, columnspan=3, sticky="nsew")
        self.prescribed_scrollbar.grid(row=1, column=3, sticky="ns")

        self.num_prescribed_entry.bind('<Return>', lambda event=None: add_prescribed_entry())    
        # =============================

        self.frame_point_load = tk.LabelFrame(self.tab_input, text="Point Loads", font="bold", bg="#E0E0E0")
        self.frame_point_load.grid(row=1, column=1, padx=50,  pady=10, sticky="nsew")
        self.frame_point_load.config(bg="#E0E0E0")

        self.num_point_load_label = tk.Label(self.frame_point_load, text="Nodes with Point Load:         \t    ", bg="#E0E0E0")
        self.num_point_load_label.grid(row=0, column=0, padx=1, pady=5, sticky="w")
        self.num_point_load_entry = tk.Entry(self.frame_point_load, width=9)
        self.num_point_load_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        self.point_load_canvas = tk.Canvas(self.frame_point_load, bg="#E0E0E0")
        self.point_load_scrollbar = tk.Scrollbar(self.frame_point_load, orient="vertical", command=self.point_load_canvas.yview, bg="#E0E0E0")
        self.point_load_scrollable_frame = tk.Frame(self.point_load_canvas, bg="#E0E0E0")

        self.point_load_canvas.create_window((0, 0), window=self.point_load_scrollable_frame, anchor="nw")
        self.point_load_canvas.configure(yscrollcommand=self.point_load_scrollbar.set)

        self.point_load_scrollable_frame.bind("<Configure>", configure_scroll_region)

        self.point_load_canvas.grid(row=1, column=0, columnspan=3, sticky="nsew")
        self.point_load_scrollbar.grid(row=1, column=3, sticky="ns")

        self.num_point_load_entry.bind('<Return>', lambda event=None: add_point_load_entry())    
# -----------------------------------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------------------------------
        # This method prepares the Calculation tab with placeholders or widgets to display calculation results.
        # Will be populated with results from truss calculations upon user request.        
        
        calculate_button = tk.Button(self.tab_calculation, highlightbackground="#E0E0E0", highlightcolor="#E0E0E0", text="Perform Calculation", command=self.perform_calculation)
        calculate_button.grid(row=0, column=1, padx=40,  pady=10, sticky="nsew")
    
  
    def setup_calculation_tab(self):

        self.global_matrix_frame = ttk.LabelFrame(self.tab_calculation, text= "Global Stiffness Matrix", style='TLabel', width=758, height=200)
        self.global_matrix_frame.grid(row=1, column=1, padx=50, pady=10, sticky="nsew", columnspan=6)

        self.global_matrix_canvas = tk.Canvas(self.global_matrix_frame, bg="#F0F0F0", highlightbackground="#F0F0F0", highlightcolor="#F0F0F0", highlightthickness=0, borderwidth=0, width=758, height=200)
        self.global_matrix_canvas.grid(row=0, column=0, sticky="nsew")

        self.global_matrix_scrollbar = ttk.Scrollbar(self.global_matrix_frame, orient="vertical", command=self.global_matrix_canvas.yview)
        self.global_matrix_scrollbar.grid(row=0, column=1, sticky="ns")

        self.global_matrix_canvas.configure(yscrollcommand=self.global_matrix_scrollbar.set)

        self.global_matrix_scrollbar_frame = ttk.Frame(self.global_matrix_canvas)
        self.global_matrix_canvas.create_window((0, 0), window=self.global_matrix_scrollbar_frame, anchor="nw")

        self.global_matrix_scrollbar_frame.bind("<Configure>", lambda e: self.global_matrix_canvas.configure(scrollregion=self.global_matrix_canvas.bbox("all")))
        
        
        # ----------------
        self.displacement_frame = ttk.LabelFrame(self.tab_calculation, text= "Displacements", style='TLabel')
        self.displacement_frame.grid(row=2, column=1, padx=50, pady=10, sticky="nsew")

        self.displacement_canvas = tk.Canvas(self.displacement_frame, bg="#F0F0F0", highlightthickness=0, borderwidth=0, width=174, height=250)
        self.displacement_canvas.grid(row=2, column=0, sticky="nsew")

        self.displacement_scrollbar = ttk.Scrollbar(self.displacement_frame, orient="vertical", command=self.displacement_canvas.yview)
        self.displacement_scrollbar.grid(row=2, column=1, sticky="ns")

        self.displacement_canvas.configure(yscrollcommand=self.displacement_scrollbar.set)

        self.displacement_scrollbar_frame = ttk.Frame(self.displacement_canvas)
        self.displacement_canvas.create_window((0, 0), window=self.displacement_scrollbar_frame, anchor="nw")

        self.displacement_scrollbar_frame.bind("<Configure>", lambda e: self.displacement_canvas.configure(scrollregion=self.displacement_canvas.bbox("all")))
        
        # ----------------
        self.reaction_frame = ttk.LabelFrame(self.tab_calculation, text= "Reactions", style='TLabel')
        self.reaction_frame.grid(row=2, column=2, padx=50, pady=10, sticky="nsew")

        self.reaction_canvas = tk.Canvas(self.reaction_frame, bg="#F0F0F0", highlightthickness=0, borderwidth=0, width=174, height=250)
        self.reaction_canvas.grid(row=2, column=1, sticky="nsew")

        self.reaction_scrollbar = ttk.Scrollbar(self.reaction_frame, orient="vertical", command=self.reaction_canvas.yview)
        self.reaction_scrollbar.grid(row=2, column=2, sticky="ns")

        self.reaction_canvas.configure(yscrollcommand=self.reaction_scrollbar.set)

        self.reaction_scrollbar_frame = ttk.Frame(self.reaction_canvas)
        self.reaction_canvas.create_window((0, 0), window=self.reaction_scrollbar_frame, anchor="nw")

        self.reaction_scrollbar_frame.bind("<Configure>", lambda e: self.reaction_canvas.configure(scrollregion=self.reaction_canvas.bbox("all")))
        
        # ----------------
        self.stresse_frame = ttk.LabelFrame(self.tab_calculation, text= "Stresses", style='TLabel')
        self.stresse_frame.grid(row=2, column=3, padx=50, pady=10, sticky="nsew")

        self.stresse_canvas = tk.Canvas(self.stresse_frame, bg="#F0F0F0", highlightthickness=0, borderwidth=0, width=174, height=250)
        self.stresse_canvas.grid(row=2, column=2, sticky="nsew")

        self.stresse_scrollbar = ttk.Scrollbar(self.stresse_frame, orient="vertical", command=self.stresse_canvas.yview)
        self.stresse_scrollbar.grid(row=2, column=3, sticky="ns")

        self.stresse_canvas.configure(yscrollcommand=self.stresse_scrollbar.set)

        self.stresse_scrollbar_frame = ttk.Frame(self.stresse_canvas)
        self.stresse_canvas.create_window((0, 0), window=self.stresse_scrollbar_frame, anchor="nw")

        self.stresse_scrollbar_frame.bind("<Configure>", lambda e: self.stresse_canvas.configure(scrollregion=self.reaction_canvas.bbox("all")))
        
        # ----------------


    def perform_calculation(self):
       
        coords_entries     = [(float(x_entry.get()), float(y_entry.get())) for x_entry, y_entry, _ in self.coords_entries]
        elements_entries   = [(int(start_node.get()), int(end_node.get()), float(A_entry.get()), float(E_entry.get())) for start_node, end_node, A_entry, E_entry, _ in self.elements_entries]
        prescribed_entries = [(int(node.get()), float(x_disp.get()), float(y_disp.get())) for node, x_disp, y_disp, _ in self.prescribed_entries]
        point_load_entries = [(int(node.get()), float(x_force.get()), float(y_force.get())) for node, x_force, y_force, _ in self.point_load_entries]

        try:
            K, q, R, stresses = tc.truss2D(coords_entries, elements_entries, prescribed_entries, point_load_entries)

        except np.linalg.LinAlgError:
            messagebox.showerror("Error", "Calculation failed due to a singular matrix. Check inputs to ensure the truss is linear and properly configured.")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")


        for widget in self.global_matrix_scrollbar_frame.winfo_children():
            widget.destroy()

        for widget in self.displacement_scrollbar_frame.winfo_children():
            widget.destroy()

        for widget in self.reaction_scrollbar_frame.winfo_children():
            widget.destroy()

        for widget in self.stresse_scrollbar_frame.winfo_children():
            widget.destroy()

        self.display_matrix(self.global_matrix_scrollbar_frame, K, "K")
        self.display_vector(self.displacement_scrollbar_frame,  q, "q")
        self.display_vector(self.reaction_scrollbar_frame,  R, "R")
        self.display_vector(self.stresse_scrollbar_frame,  stresses, "stresses")

    def display_matrix(self, frame, matrix, label):
        if matrix is not None:
            formatted_matrix = ""
            num_rows, num_cols = matrix.shape
            max_widths = [max(len("{:.3f}".format(matrix[i, j])) for i in range(num_rows)) for j in range(num_cols)]   

            for i in range(num_rows):
                formatted_matrix += "   "
                for j in range(num_cols):
                    formatted_matrix += "{:{width}.3f}".format(matrix[i, j], width=max_widths[j]) + "   "

                formatted_matrix += "\n"

            formatted_matrix = "\n" + formatted_matrix
            matrix_text = tk.Text(frame, wrap='none', font=('Courier', 15),  bg="#f0f0f0", bd=0)
            matrix_text.insert('end', formatted_matrix)
            matrix_text.config(state='disabled') 
            matrix_text.grid(row=0, column=0, sticky="nw")

            matrix_text.bind("<Control-a>", lambda event: matrix_text.tag_add(tk.SEL, "1.0", tk.END))
            matrix_text.bind("<Control-c>", lambda event: matrix_text.event_generate("<<Copy>>"))

    def display_vector(self, frame, vector, label):
        if vector is not None:
            formatted_vector = ""
            num_rows = len(vector)
            max_width = max(len("{:.3f}".format(val)) for val in vector)

            for val in vector:
                formatted_vector += "      {:{width}.3f}".format(val, width=max_width) + "\n"

            formatted_vector = "\n" + formatted_vector
            vector_text = tk.Text(frame, wrap='none', font=('Courier', 15), bg="#f0f0f0", bd=0)
            vector_text.insert('end', formatted_vector)
            vector_text.config(state='disabled')
            vector_text.grid(row=0, column=0, sticky="nw")

            vector_text.bind("<Control-a>", lambda event: vector_text.tag_add(tk.SEL, "1.0", tk.END))
            vector_text.bind("<Control-c>", lambda event: vector_text.event_generate("<<Copy>>"))

# -----------------------------------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------------------------------
   # This method configures the Figure tab, setting up the matplotlib figure for displaying the truss diagram.
    # Allows for plotting of the truss based on input nodes and elements, including loads and supports.
            
    def setup_figure_tab(self):
        self.figure = Figure(figsize=(5, 4), dpi=100)
        self.plot = self.figure.add_subplot(1, 1, 1)
        self.figure_canvas = FigureCanvasTkAgg(self.figure, master=self.tab_figure) 
        self.canvas_widget = self.figure_canvas.get_tk_widget()
        self.canvas_widget.pack(fill=tk.BOTH, expand=True)

        self.plot_button = tk.Button(self.tab_figure, text="Plot Truss", command=self.plot_truss, highlightbackground="#E0E0E0", highlightcolor="#E0E0E0")
        self.plot_button.pack(side=tk.BOTTOM)

    def get_node_coordinates(self):
        node_coords = []
        for i, (x_entry, y_entry, _) in enumerate(self.coords_entries, start=1):
            try:
                x = float(x_entry.get())
                y = float(y_entry.get())
                node_coords.append((x, y))
            except ValueError:
                messagebox.showerror("Invalid Input", f"Error: Invalid coordinate at Node {i}. Please enter valid numbers.")
                return []
        return node_coords
  
    def get_elements(self):
        elements = []
        for i, entries in enumerate(self.elements_entries, start=1):
            try:
                start_node_entry, end_node_entry = entries[:2] 
                start_node = int(start_node_entry.get())
                end_node = int(end_node_entry.get())
                elements.append((start_node, end_node))
            except ValueError:
                messagebox.showerror("Invalid Input", f"Error: Invalid element configuration at Element {i}. Please enter valid node numbers.")
                return [] 
        return elements

        
    def plot_truss(self):
        self.plot.clear()
        node_coords = self.get_node_coordinates()
        elements = self.get_elements()

        if not node_coords or not elements:
            return

        for idx, (x, y) in enumerate(node_coords):
            self.plot.plot(x, y, 'ro', label='Nodes' if idx == 0 else "") 
            self.plot.text(x, y, f'N{idx+1}', color='blue')

        for i, (start_node, end_node) in enumerate(elements, start=1):
            start_coord = node_coords[start_node - 1]
            end_coord = node_coords[end_node - 1]
            self.plot.plot([start_coord[0], end_coord[0]], [start_coord[1], end_coord[1]], 'k-', label='Elements' if i == 1 else "")
            mid_point = [(start_coord[0] + end_coord[0]) / 2, (start_coord[1] + end_coord[1]) / 2]
            self.plot.text(mid_point[0], mid_point[1], f'E{i}', color='green')

        def draw_force_arrows(node_num, x_force, y_force, force_type):
            node_coord = node_coords[node_num - 1]
            node_coord_0 = node_coords[0]
            node_coord_1 = node_coords[1]
            scale_factor = np.abs(node_coord_0[0] - node_coord_1[0]) * 0.15
            if force_type == 'point load':
                if x_force != 0:
                    self.plot.arrow(node_coord[0], node_coord[1], scale_factor, 0, color='green',
                                    length_includes_head=True, head_width=scale_factor/5, head_length=scale_factor/5)
                if y_force != 0:
                    self.plot.arrow(node_coord[0], node_coord[1], 0, scale_factor, color='green',
                                    length_includes_head=True, head_width=scale_factor/5, head_length=scale_factor/5)
                    
            if force_type == 'prescribed':
                scale_factor = scale_factor / 2
                if x_force != 0:
                    self.plot.arrow(node_coord[0], node_coord[1], scale_factor, 0, color='blue',
                                    length_includes_head=True, head_width=scale_factor/10, head_length=scale_factor/10)
                if y_force != 0:
                    self.plot.arrow(node_coord[0], node_coord[1], 0, scale_factor, color='blue',
                                    length_includes_head=True, head_width=scale_factor/10, head_length=scale_factor/10)

        for entry in self.prescribed_entries + self.point_load_entries:
            n_entry, x_entry, y_entry, _ = entry
            try:
                node_num = int(n_entry.get())
                x_force = float(x_entry.get())
                y_force = float(y_entry.get())
                force_type = 'prescribed' if entry in self.prescribed_entries else 'point load'
                draw_force_arrows(node_num, x_force, y_force, force_type)
            except ValueError:
                pass 

        self.plot.axis('equal')
        self.plot.set_xlabel('X axis')
        self.plot.set_ylabel('Y axis')
        self.plot.set_title('Truss Structure')

        legend_elements = [Line2D([0], [0], color='red', marker='o', linestyle='', label='Nodes'),
                        Line2D([0], [0], color='black', linestyle='-', label='Elements'),
                        Line2D([0], [0], color='blue', linestyle='', marker='>', label='Prescribed Displacements'),
                        Line2D([0], [0], color='green', linestyle='', marker='>', label='Point Loads')]
        self.plot.legend(handles=legend_elements, loc='upper center', bbox_to_anchor=(0.85, 1.13), ncol=2, fontsize='small', markerscale=0.75)


        self.figure_canvas.draw()


if __name__ == "__main__":
    root = tk.Tk()
    app = TrussSolverApp(root)
    root.mainloop()

