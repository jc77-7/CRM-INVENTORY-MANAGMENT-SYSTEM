import tkinter as tk
from tkinter import ttk
import sqlite3
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class ProductDataVisualization:
    def __init__(self, root):
        self.root = root
        self.root.title("Product Data Visualization")
        self.root.geometry("800x600")

        self.create_widgets()
        self.load_data()

    def create_widgets(self):
        self.frame = ttk.Frame(self.root)
        self.frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.plot_type_var = tk.StringVar(value="Category Distribution")
        plot_options = ["Category Distribution", "Supplier Distribution", "Price Distribution", "Quantity Distribution", "Status Distribution"]
        self.plot_type_dropdown = ttk.Combobox(self.frame, textvariable=self.plot_type_var, values=plot_options, state="readonly")
        self.plot_type_dropdown.pack(pady=10)
        self.plot_type_dropdown.bind("<<ComboboxSelected>>", self.update_plot)

        self.canvas_frame = ttk.Frame(self.frame)
        self.canvas_frame.pack(fill=tk.BOTH, expand=True)

        self.fig, self.ax = plt.subplots(figsize=(8, 6))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.canvas_frame)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(fill=tk.BOTH, expand=True)

    def load_data(self):
        con = sqlite3.connect(r'new_ims.db')
        cur = con.cursor()
        try:
            cur.execute("SELECT * FROM product")
            self.data = cur.fetchall()
        except Exception as ex:
            tk.messagebox.showerror("Error", f"Error loading data: {str(ex)}")
            self.data = []
        finally:
            con.close()
        self.update_plot()

    def update_plot(self, event=None):
        self.ax.clear()
        plot_type = self.plot_type_var.get()
        if plot_type == "Category Distribution":
            self.plot_category_distribution()
        elif plot_type == "Supplier Distribution":
            self.plot_supplier_distribution()
        elif plot_type == "Price Distribution":
            self.plot_price_distribution()
        elif plot_type == "Quantity Distribution":
            self.plot_quantity_distribution()
        elif plot_type == "Status Distribution":
            self.plot_status_distribution()

        self.canvas.draw()

    def plot_category_distribution(self):
        categories = [row[0] for row in self.data]
        category_counts = {}
        for category in categories:
            category_counts[category] = category_counts.get(category, 0) + 1
        self.ax.bar(category_counts.keys(), category_counts.values())
        self.ax.set_title("Category Distribution")
        self.ax.set_xlabel("Category")
        self.ax.set_ylabel("Count")
        self.ax.tick_params(axis='x', rotation=45)

    def plot_supplier_distribution(self):
        suppliers = [row[1] for row in self.data]
        supplier_counts = {}
        for supplier in suppliers:
            supplier_counts[supplier] = supplier_counts.get(supplier, 0) + 1
        self.ax.bar(supplier_counts.keys(), supplier_counts.values())
        self.ax.set_title("Supplier Distribution")
        self.ax.set_xlabel("Supplier")
        self.ax.set_ylabel("Count")
        self.ax.tick_params(axis='x', rotation=45)

    def plot_price_distribution(self):
        prices = [float(row[3]) for row in self.data]
        self.ax.hist(prices, bins=10, edgecolor='black')
        self.ax.set_title("Price Distribution")
        self.ax.set_xlabel("Price")
        self.ax.set_ylabel("Frequency")

    def plot_quantity_distribution(self):
        quantities = [int(row[4]) for row in self.data]
        self.ax.hist(quantities, bins=10, edgecolor='black')
        self.ax.set_title("Quantity Distribution")
        self.ax.set_xlabel("Quantity")
        self.ax.set_ylabel("Frequency")

    def plot_status_distribution(self):
        statuses = [row[5] for row in self.data]
        status_counts = {}
        for status in statuses:
            status_counts[status] = status_counts.get(status, 0) + 1
        self.ax.bar(status_counts.keys(), status_counts.values())
        self.ax.set_title("Status Distribution")
        self.ax.set_xlabel("Status")
        self.ax.set_ylabel("Count")

if __name__ == "__main__":
    root = tk.Tk()
    app = ProductDataVisualization(root)
    root.mainloop()