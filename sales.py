import tkinter as tk
from tkinter import BOTH, CENTER, END, RIDGE, TOP, X, Button, Entry, Frame, Label, Text, ttk, messagebox
import sqlite3
from datetime import datetime
from PIL import Image, ImageTk
import os

class salesClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1366x768")
        self.root.title("Inventory Management System | Sales")
        self.root.config(bg="#f0f0f0")
        self.root.focus_force()

        lbl_title = tk.Label(self.root, text="SALES BILLING", font=("goudy old style", 30), bg="#184a45", fg="white")
        lbl_title.pack(side=tk.TOP, fill=tk.X)

        # Variables
        self.var_invoice = tk.StringVar()
        self.var_name = tk.StringVar()
        self.var_contact = tk.StringVar()
        self.cart_list = []
        self.total_amount = tk.DoubleVar()
        self.discount = tk.DoubleVar()
        self.net_pay = tk.DoubleVar()

        # Customer Details Frame
        customer_frame = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        customer_frame.place(x=10, y=70, width=400, height=100)

        c_title = Label(customer_frame, text="Customer Details", font=("goudy old style", 15), bg="lightgray").pack(side=TOP, fill=X)

        lbl_invoice = Label(customer_frame, text="Invoice No.", font=("goudy old style", 15), bg="white").place(x=5, y=35)
        txt_invoice = Entry(customer_frame, textvariable=self.var_invoice, font=("goudy old style", 15), bg="lightyellow").place(x=100, y=35, width=150)

        lbl_name = Label(customer_frame, text="Name", font=("goudy old style", 15), bg="white").place(x=270, y=35)
        txt_name = Entry(customer_frame, textvariable=self.var_name, font=("goudy old style", 15), bg="lightyellow").place(x=330, y=35, width=150)

        lbl_contact = Label(customer_frame, text="Contact No.", font=("goudy old style", 15), bg="white").place(x=5, y=65)
        txt_contact = Entry(customer_frame, textvariable=self.var_contact, font=("goudy old style", 15), bg="lightyellow").place(x=100, y=65, width=150)

# Product Details Frame
        product_frame = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        product_frame.place(x=10, y=180, width=400, height=300)

        p_title = Label(product_frame, text="Product Details", font=("goudy old style", 15), bg="lightgray").pack(side=TOP, fill=X)

        self.lbl_product_name = Label(product_frame, text="Product Name", font=("goudy old style", 15), bg="white")
        self.lbl_product_name.place(x=5, y=35)

        self.cmb_product = ttk.Combobox(product_frame, values=self.fetch_products(), state='readonly', justify=CENTER, font=("goudy old style", 15))
        self.cmb_product.place(x=150, y=35, width=200)
        self.cmb_product.bind("<<ComboboxSelected>>", self.get_product_details)

        self.lbl_price = Label(product_frame, text="Price", font=("goudy old style", 15), bg="white").place(x=5, y=70)
        self.txt_price = Entry(product_frame, font=("goudy old style", 15), bg="lightyellow", state="readonly")
        self.txt_price.place(x=150, y=70, width=100)

        self.lbl_qty = Label(product_frame, text="Quantity", font=("goudy old style", 15), bg="white").place(x=260, y=70)
        self.txt_qty = Entry(product_frame, font=("goudy old style", 15), bg="lightyellow")
        self.txt_qty.place(x=350, y=70, width=100)

        self.btn_add_cart = Button(product_frame, text="Add to Cart", font=("goudy old style", 15), bg="#2196f3", fg="white", command=self.add_to_cart)
        self.btn_add_cart.place(x=150, y=110, width=150)

        # Cart Frame
        cart_frame = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        cart_frame.place(x=420, y=70, width=400, height=400)

        cart_title = Label(cart_frame, text="Cart", font=("goudy old style", 15), bg="lightgray").pack(side=TOP, fill=X)

        self.cart_table = ttk.Treeview(cart_frame, columns=("pid", "name", "price", "qty", "total"))
        self.cart_table.heading("pid", text="PID")
        self.cart_table.heading("name", text="Name")
        self.cart_table.heading("price", text="Price")
        self.cart_table.heading("qty", text="Qty")
        self.cart_table.heading("total", text="Total")
        self.cart_table["show"] = "headings"
        self.cart_table.pack(fill=BOTH, expand=1)

        # Billing Frame (Right Side)
        billing_frame = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        billing_frame.place(x=830, y=70, width=520, height=500)

        bill_title = Label(billing_frame, text="Customer Bill Area", font=("goudy old style", 15), bg="lightgray").pack(side=TOP, fill=X)

        # Bill Content (Labels and Text)
        self.bill_content = Text(billing_frame, font=("goudy old style", 12), bg="lightyellow", state="disabled")
        self.bill_content.pack(fill=BOTH, expand=1)

        # Billing Summary (Bottom)
        billing_summary_frame = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        billing_summary_frame.place(x=830, y=570, width=520, height=80)

        lbl_total = Label(billing_summary_frame, text="Total Amount", font=("goudy old style", 15), bg="white").place(x=5, y=10)
        txt_total = Entry(billing_summary_frame, textvariable=self.total_amount, font=("goudy old style", 15), bg="lightyellow", state="readonly").place(x=150, y=10, width=150)

        lbl_discount = Label(billing_summary_frame, text="Discount (%)", font=("goudy old style", 15), bg="white").place(x=310, y=10)
        txt_discount = Entry(billing_summary_frame, textvariable=self.discount, font=("goudy old style", 15), bg="lightyellow").place(x=450, y=10, width=100)

        lbl_net_pay = Label(billing_summary_frame, text="Net Pay", font=("goudy old style", 15), bg="white").place(x=5, y=40)
        txt_net_pay = Entry(billing_summary_frame, textvariable=self.net_pay, font=("goudy old style", 15), bg="lightyellow", state="readonly").place(x=150, y=40, width=150)

        self.btn_generate_bill = Button(billing_summary_frame, text="Generate Bill", font=("goudy old style", 15), bg="#4caf50", fg="white", command=self.generate_bill)
        self.btn_generate_bill.place(x=350, y=40, width=150)
        self.setup_bill_header()

    def setup_bill_header(self):
        self.bill_content.config(state="normal")
        self.bill_content.delete("1.0", END)
        self.bill_content.insert(END, "XYZ-Inventory\n")
        self.bill_content.insert(END, "Phone No. 8019377288\n")
        self.bill_content.insert(END, "Kakinada-533004\n\n")
        self.bill_content.config(state="disabled")

    def fetch_products(self):
        con = sqlite3.connect(r'new_ims.db')
        cur = con.cursor()
        try:
            cur.execute("SELECT name FROM product")
            products = [row[0] for row in cur.fetchall()]
            return products
        except Exception as ex:
            messagebox.showerror("Error", f"Error fetching products: {str(ex)}", parent=self.root)
            return []
        finally:
            con.close()

    def get_product_details(self, event):
        con = sqlite3.connect(r'new_ims.db')
        cur = con.cursor()
        try:
            cur.execute("SELECT price FROM product WHERE name=?", (self.cmb_product.get(),))
            price = cur.fetchone()[0]
            self.txt_price.config(state="normal")
            self.txt_price.delete(0, END)
            self.txt_price.insert(0, price)
            self.txt_price.config(state="readonly")
        except Exception as ex:
            messagebox.showerror("Error", f"Error fetching product price: {str(ex)}", parent=self.root)
        finally:
            con.close()

    def add_to_cart(self):
        if self.cmb_product.get() == "":
            messagebox.showerror("Error", "Please select a product.", parent=self.root)
            return
        if self.txt_qty.get() == "":
            messagebox.showerror("Error", "Please enter quantity.", parent=self.root)
            return
        try:
            qty = int(self.txt_qty.get())
            price = float(self.txt_price.get())
            total = qty * price
            pid = self.get_product_id(self.cmb_product.get())
            self.cart_list.append((pid, self.cmb_product.get(), price, qty, total))
            self.update_cart_table()
            self.calculate_total()
        except ValueError:
            messagebox.showerror("Error", "Invalid quantity or price.", parent=self.root)

    def get_product_id(self, product_name):
        con = sqlite3.connect(r'new_ims.db')
        cur = con.cursor()
        try:
            cur.execute("SELECT rowid FROM product WHERE name=?", (product_name,))
            pid = cur.fetchone()[0]
            return pid
        except Exception as ex:
            messagebox.showerror("Error", f"Error fetching product ID: {str(ex)}", parent=self.root)
            return None
        finally:
            con.close()

    def update_cart_table(self):
        self.cart_table.delete(*self.cart_table.get_children())
        for item in self.cart_list:
            self.cart_table.insert('', END, values=item)

    def calculate_total(self):
        total = sum(item[4] for item in self.cart_list)
        self.total_amount.set(total)
        discount = float(self.discount.get() if self.discount.get() else 0)
        net_pay = total - (total * discount / 100)
        self.net_pay.set(net_pay)

    def generate_bill(self):
        if not self.cart_list:
            messagebox.showerror("Error", "Cart is empty.", parent=self.root)
            return
        if self.var_invoice.get() == "":
            messagebox.showerror("Error", "Invoice number is required.", parent=self.root)
            return

        con = sqlite3.connect(r'new_ims.db')
        cur = con.cursor()
        try:
            cur.execute("CREATE TABLE IF NOT EXISTS sales (invoice TEXT PRIMARY KEY, name TEXT, contact TEXT, date TEXT, total REAL, discount REAL, net_pay REAL)")
            cur.execute("INSERT INTO sales (invoice, name, contact, date, total, discount, net_pay) VALUES (?,?,?,?,?,?,?)",
                        (self.var_invoice.get(), self.var_name.get(), self.var_contact.get(), datetime.now().strftime("%Y-%m-%d %H:%M:%S"), self.total_amount.get(), float(self.discount.get() if self.discount.get() else 0), self.net_pay.get()))
            for item in self.cart_list:
                cur.execute("CREATE TABLE IF NOT EXISTS sales_details (invoice TEXT, pid INTEGER, name TEXT, price REAL, qty INTEGER, total REAL)")
                cur.execute("INSERT INTO sales_details (invoice, pid, name, price, qty, total) VALUES (?,?,?,?,?,?)",
                            (self.var_invoice.get(), item[0], item[1], item[2], item[3], item[4]))
            con.commit()
            messagebox.showinfo("Success", "Bill generated successfully.", parent=self.root)
            self.display_bill()
            self.clear_cart()
        except Exception as ex:
            messagebox.showerror("Error", f"Error generating bill: {str(ex)}", parent=self.root)
        finally:
            con.close()

    def display_bill(self):
        self.bill_content.config(state="normal")
        self.bill_content.delete("5.0", END) # Clear existing bill details
        self.bill_content.insert(END, f"Customer Name: {self.var_name.get()}\n")
        self.bill_content.insert(END, f"Ph no. {self.var_contact.get()}\n")
        self.bill_content.insert(END, f"Bill No. {self.var_invoice.get()}\n")
        self.bill_content.insert(END, f"Date: {datetime.now().strftime('%d/%m/%Y')}\n\n")
        self.bill_content.insert(END, "Product Name\tQTY\tPrice\n")
        self.bill_content.insert(END, "-------------------------\n")
        for item in self.cart_list:
            self.bill_content.insert(END, f"{item[1]}\t{item[3]}\tRs.{item[2]}\n")
        self.bill_content.insert(END, "\n")
        self.bill_content.insert(END, f"Bill Amount\t\tRs.{self.total_amount.get()}\n")
        self.bill_content.insert(END, f"Discount\t\tRs.{self.total_amount.get() * float(self.discount.get() if self.discount.get() else 0) / 100}\n")
        self.bill_content.insert(END, f"Net Pay\t\tRs.{self.net_pay.get()}\n")
        self.bill_content.config(state="disabled")

    def clear_cart(self):
        self.cart_list.clear()
        self.update_cart_table()
        self.total_amount.set(0)
        self.discount.set(0)
        self.net_pay.set(0)
        self.var_invoice.set("")
        self.var_name.set("")
        self.var_contact.set("")
        self.txt_qty.delete(0, END)
        self.txt_price.delete(0, END)
        if self.fetch_products():
            self.cmb_product.current(0)

class InventoryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Inventory Management System | Developed By Rangesh")
        self.root.geometry("1366x768")

        # --- Header ---
        header_frame = tk.Frame(root, bg="#f0f0f0")
        header_frame.pack(fill=tk.X)

        title_label = tk.Label(header_frame, text="Inventory Management System", font=("goudy old style", 20, "bold"), bg="#f0f0f0")
        title_label.pack(side=tk.LEFT, padx=10, pady=10)

        logout_button = ttk.Button(header_frame, text="Logout")
        logout_button.pack(side=tk.RIGHT, padx=10, pady=10)

        welcome_label = tk.Label(header_frame, text="Welcome to Inventory Management System", bg="#f0f0f0")
        welcome_label.pack(side=tk.LEFT, padx=10, pady=10)

        date_time_label = tk.Label(header_frame, text=f"Date: {datetime.now().strftime('%d-%m-%Y')}  Time: {datetime.now().strftime('%H:%M:%S')}", bg="#f0f0f0")
        date_time_label.pack(side=tk.RIGHT, padx=10, pady=10)

        # --- Main Content ---
        main_frame = tk.Frame(root)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # --- Product Section ---
        product_frame = tk.Frame(main_frame, bd=2, relief=tk.RIDGE)
        product_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        product_title = tk.Label(product_frame, text="All Products", font=("goudy old style", 15, "bold"))
        product_title.pack(fill=tk.X)

        search_frame = tk.Frame(product_frame)
        search_frame.pack(fill=tk.X)

        search_label = tk.Label(search_frame, text="Search Product | By Name")
        search_label.pack(side=tk.LEFT)

        search_entry = tk.Entry(search_frame)
        search_entry.pack(side=tk.LEFT)

        show_all_button = ttk.Button(search_frame, text="Show All")
        show_all_button.pack(side=tk.LEFT)

        self.product_list = ttk.Treeview(product_frame, columns=("pid", "name", "price", "qty", "status"))
        self.product_list.heading("pid", text="PID")
        self.product_list.heading("name", text="Name")
        self.product_list.heading("price", text="Price")
        self.product_list.heading("qty", text="QTY")
        self.product_list.heading("status", text="Status")
        self.product_list.pack(fill=tk.BOTH, expand=True)

        self.product_list.insert("", tk.END, values=(3, "Poco X3", 21000, 100, "Active"))
        self.product_list.insert("", tk.END, values=("new", 12, 21, "Active"))

        # --- Customer Details ---
        customer_frame = tk.Frame(main_frame, bd=2, relief=tk.RIDGE)
        customer_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        customer_title = tk.Label(customer_frame, text="Customer Details", font=("goudy old style", 15, "bold"))
        customer_title.pack(fill=tk.X)

        name_label = tk.Label(customer_frame, text="Name")
        name_label.pack()
        name_entry = tk.Entry(customer_frame)
        name_entry.insert(0, "Rangesh")
        name_entry.pack()

        contact_label = tk.Label(customer_frame, text="Contact No.")
        contact_label.pack()
        contact_entry = tk.Entry(customer_frame)
        contact_entry.insert(0, "9876543210")
        contact_entry.pack()

        keypad_frame = tk.Frame(customer_frame)
        keypad_frame.pack()

        buttons = [
            '7', '8', '9', '+',
            '4', '5', '6', '',
            '1', '2', '3', '',
            '0', 'C', '=', '/'
        ]
        r = 0
        c = 0
        for button_text in buttons:
            if button_text:
                button = ttk.Button(keypad_frame, text=button_text)
                button.grid(row=r, column=c, padx=5, pady=5)
            c += 1
            if c > 3:
                c = 0
                r += 1

        cart_frame = tk.Frame(customer_frame)
        cart_frame.pack(fill=tk.BOTH, expand=True)

        cart_title = tk.Label(cart_frame, text="Cart", font=("goudy old style", 12))
        cart_title.pack(fill=tk.X)

        self.cart_list = ttk.Treeview(cart_frame, columns=("name", "price", "qty"))
        self.cart_list.heading("name", text="Name")
        self.cart_list.heading("price", text="Price")
        self.cart_list.heading("qty", text="QTY")
        self.cart_list.pack(fill=tk.BOTH, expand=True)

        self.cart_list.insert("", tk.END, values=("Poco X3", 21000, 4))
        self.cart_list.insert("", tk.END, values=("new", 12, 12))

        total_products_label = tk.Label(customer_frame, text="Total Product: [2]")
        total_products_label.pack()

        # --- Bill Area ---
        bill_frame = tk.Frame(main_frame, bd=2, relief=tk.RIDGE)
        bill_frame.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")

        bill_title = tk.Label(bill_frame, text="Customer Bill Area", font=("goudy old style", 15, "bold"))
        bill_title.pack(fill=tk.X)

        bill_content = tk.Text(bill_frame, height=15, width=40)
        bill_content.pack(fill=tk.BOTH, expand=True)

        bill_content.insert(tk.END, "XYZ-Inventory\n")
        bill_content.insert(tk.END, "Phone No.801937788 \n")
        bill_content.insert(tk.END, "Kakinada-125001\n\n")
        bill_content.insert(tk.END, "Customer Name: Mukesh\n")
        bill_content.insert(tk.END, "Ph no. 19876543210\n")
        bill_content.insert(tk.END, "Bill No. 4236444\n")
        bill_content.insert(tk.END, "Date: 04/06/2024\n\n")
        bill_content.insert(tk.END, "Product Name\tQTY\tPrice\n")
        bill_content.insert(tk.END, "Poco X3\t1\tRs.21000.0\n")
        bill_content.insert(tk.END, "new\t4\tRs.48.0\n\n")
        bill_content.insert(tk.END, "Bill Amount\tRs.21048.0\n")
        bill_content.insert(tk.END, "Discount\tRs.1052.4\n")
        bill_content.insert(tk.END, "Net Pay\tRs.19995.6\n")

        # --- Bottom Section ---
        bottom_frame =tk.Frame(root)
        bottom_frame.pack(fill=tk.X)

        note_label = tk.Label(bottom_frame, text="Note: Enter 0 Qunatity to remove product from the Cart")
        note_label.pack(side=tk.LEFT, padx=10, pady=5)

        product_details_frame = tk.Frame(bottom_frame)
        product_details_frame.pack(side=tk.LEFT, padx=10, pady=5)

        product_name_label = tk.Label(product_details_frame, text="Product Name")
        product_name_label.grid(row=0, column=0, padx=5, pady=5)
        product_name_entry = tk.Entry(product_details_frame)
        product_name_entry.grid(row=0, column=1, padx=5, pady=5)

        price_label = tk.Label(product_details_frame, text="Price Per Qty")
        price_label.grid(row=0, column=2, padx=5, pady=5)
        price_entry = tk.Entry(product_details_frame)
        price_entry.grid(row=0, column=3, padx=5, pady=5)

        qty_label = tk.Label(product_details_frame, text="Quantity")
        qty_label.grid(row=0, column=4, padx=5, pady=5)
        qty_entry = tk.Entry(product_details_frame)
        qty_entry.grid(row=0, column=5, padx=5, pady=5)

        in_stock_label = tk.Label(product_details_frame, text="In Stock [100]")
        in_stock_label.grid(row=0, column=6, padx=5, pady=5)

        clear_button = ttk.Button(product_details_frame, text="Clear")
        clear_button.grid(row=0, column=7, padx=5, pady=5)

        add_update_button = ttk.Button(product_details_frame, text="Add Update Cart")
        add_update_button.grid(row=0, column=8, padx=5, pady=5)

        buttons_frame = tk.Frame(bottom_frame)
        buttons_frame.pack(side=tk.RIGHT, padx=10, pady=5)

        print_button = ttk.Button(buttons_frame, text="Print")
        print_button.pack(side=tk.LEFT, padx=5, pady=5)

        clear_all_button = ttk.Button(buttons_frame, text="Clear All")
        clear_all_button.pack(side=tk.LEFT, padx=5, pady=5)

        generate_save_button = ttk.Button(buttons_frame, text="Generate/Save Bill")
        generate_save_button.pack(side=tk.LEFT, padx=5, pady=5)

        # --- Billing Summary (Bottom) ---
        billing_summary_frame = tk.Frame(root, bd=2, relief=tk.RIDGE, bg="white")
        billing_summary_frame.pack(fill=tk.X)

        total_amount_label = tk.Label(billing_summary_frame, text="Bill Amnt 21048.0", font=("goudy old style", 15), bg="white")
        total_amount_label.pack(side=tk.LEFT, padx=10, pady=5)

        discount_label = tk.Label(billing_summary_frame, text="Discount [5%]", font=("goudy old style", 15), bg="white")
        discount_label.pack(side=tk.LEFT, padx=10, pady=5)

        net_pay_label = tk.Label(billing_summary_frame, text="Net Pay 19995.6", font=("goudy old style", 15), bg="white")
        net_pay_label.pack(side=tk.RIGHT, padx=10, pady=5)

if __name__ == "__main__":
    root = tk.Tk()
    app = salesClass(root)  # Or app = SalesClass(root) if you want to use that
    root.mainloop()