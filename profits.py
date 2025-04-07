from tkinter import *
from PIL import Image, ImageTk
from employee import employeeClass
from supplier import SupplierClass
from category import categoryClass
from products import productClass
from sales import salesClass
from stocks import StockClass
from visual import ProductDataVisualization
import datetime
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class CustomerSatisfactionClass:
    def __init__(self, root):
        self.root = root
        self.root.title("Customer Satisfaction")
        self.root.geometry("800x600")

        self.load_and_visualize_data()

    def load_and_visualize_data(self):
        try:
            df = pd.read_csv("customer_satisfaction.csv") #replace with your data source.
            average_ratings = df.groupby("product_id")["rating"].mean()

            fig, ax = plt.subplots()
            average_ratings.plot(kind="bar", ax=ax)
            ax.set_title("Average Ratings by Product")
            ax.set_xlabel("Product ID")
            ax.set_ylabel("Average Rating")

            canvas = FigureCanvasTkAgg(fig, master=self.root)
            canvas.draw()
            canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)

        except FileNotFoundError:
            Label(self.root, text="Customer satisfaction data not found.").pack()

if __name__ == "__main__":
    root = Tk()
    obj = CustomerSatisfactionClass(root)
    root.mainloop()