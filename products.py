from tkinter import *
from tkinter import ttk, messagebox
import sqlite3

class productClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1100x600+220+130")
        self.root.title("Inventory Management System | Developed by Nikhila")
        self.root.config(bg="white")
        self.root.focus_force()

        self.var_searchby = StringVar()
        self.var_searchtxt = StringVar()

        self.var_cat = StringVar()
        self.var_sup = StringVar()
        self.var_name = StringVar()
        self.var_price = StringVar()
        self.var_qty = StringVar()
        self.var_status = StringVar()

        product_frame = Frame(self.root, bd=3, relief=RIDGE)
        product_frame.place(x=10, y=10, width=450, height=570)

        title = Label(product_frame, text="Product Details", font=("goudy old style", 22), bg="#0f4d7d", fg="white").pack(side=TOP, fill=X)

        lbl_category = Label(product_frame, text="Category", font=("goudy old style", 22), bg="white").place(x=30, y=60)
        lbl_supplier = Label(product_frame, text="Supplier", font=("goudy old style", 22), bg="white").place(x=30, y=110)
        lbl_product_name = Label(product_frame, text=" Name", font=("goudy old style", 22), bg="white").place(x=30, y=160)
        lbl_price = Label(product_frame, text="Price", font=("goudy old style", 22), bg="white").place(x=30, y=210)
        lbl_qty = Label(product_frame, text="Quantity", font=("goudy old style", 22), bg="white").place(x=30, y=260)
        lbl_status = Label(product_frame, text="Status", font=("goudy old style", 22), bg="white").place(x=30, y=310)

        self.categories = self.fetch_categories()
        self.suppliers = self.fetch_suppliers()

        cmb_cat = ttk.Combobox(product_frame, textvariable=self.var_cat, values=self.categories, state='readonly', justify=CENTER, font=("times new roman", 15))
        cmb_cat.place(x=150, y=60, width=200)
        if self.categories:
            cmb_cat.current(0)

        cmb_sup = ttk.Combobox(product_frame, textvariable=self.var_sup, values=self.suppliers, state='readonly', justify=CENTER, font=("times new roman", 15))
        cmb_sup.place(x=150, y=110, width=200)
        if self.suppliers:
            cmb_sup.current(0)

        txt_name = Entry(product_frame, textvariable=self.var_name, font=("times new roman", 15), bg='lightyellow')
        txt_name.place(x=150, y=160, width=200)
        txt_price = Entry(product_frame, textvariable=self.var_price, font=("times new roman", 15), bg='lightyellow')
        txt_price.place(x=150, y=210, width=200)
        txt_qty = Entry(product_frame, textvariable=self.var_qty, font=("times new roman", 15), bg='lightyellow')
        txt_qty.place(x=150, y=260, width=200)

        cmb_status = ttk.Combobox(product_frame, textvariable=self.var_status, values=("Active", "Inactive"), state='readonly', justify=CENTER, font=("times new roman", 15))
        cmb_status.place(x=150, y=310, width=200)
        cmb_status.current(0)

        btn_add = Button(product_frame, text="Save", command=self.add_product, font=("times new roman", 15), bg='lightgreen', fg="black", cursor="hand2")
        btn_add.place(x=10, y=400, width=100, height=35)
        btn_update = Button(product_frame, text="Update", command=self.update_product, font=("times new roman", 15), bg='lightblue', fg="black", cursor="hand2")
        btn_update.place(x=120, y=400, width=110, height=35)
        btn_delete = Button(product_frame, text="Delete", command=self.delete_product, font=("times new roman", 15), bg='red', fg="white", cursor="hand2")
        btn_delete.place(x=230, y=400, width=110, height=35)
        btn_clear = Button(product_frame, text="Clear", command=self.clear_fields, font=("times new roman", 15), bg='lightyellow', fg="black", cursor="hand2")
        btn_clear.place(x=340, y=400, width=110, height=35)

        SearchFrame = LabelFrame(self.root, text="Search Product", font=("times new roman", 12, "bold"), bd=2, relief=RIDGE, bg="white")
        SearchFrame.place(x=480, y=10, width=600, height=80)

        cmb_search = ttk.Combobox(SearchFrame, textvariable=self.var_searchby, values=("Select", "Category", "Name", "Supplier"), state='readonly', justify=CENTER, font=("times new roman", 15))
        cmb_search.place(x=10, y=10, width=180)
        cmb_search.current(0)

        txt_search = Entry(SearchFrame, textvariable=self.var_searchtxt, font=("times new roman", 15), bg="lightyellow")
        txt_search.place(x=200, y=10, width=200)

        btn_search = Button(SearchFrame, text="Search", command=self.search, font=("times new roman", 15), bg="#4caf50", fg="white", cursor="hand2")
        btn_search.place(x=410, y=10, width=180)

        # Product Table
        self.productTable = ttk.Treeview(self.root, columns=("category", "supplier", "name", "price", "qty", "status"))
        self.productTable.heading("category", text="CATEGORY")
        self.productTable.heading("supplier", text="SUPPLIER")
        self.productTable.heading("name", text="NAME")
        self.productTable.heading("price", text="PRICE")
        self.productTable.heading("qty", text="QTY")
        self.productTable.heading("status", text="STATUS")
        self.productTable["show"] = "headings"

        for col in self.productTable["columns"]:
            self.productTable.column(col, width=100)

        self.productTable.place(x=480, y=100, width=600, height=470)
        self.productTable.bind("<ButtonRelease-1>", self.get_data)

        self.show()

    def fetch_categories(self):
        con = sqlite3.connect(r'new_ims.db')
        cur = con.cursor()
        try:
            cur.execute("SELECT name FROM category")
            categories = [row[0] for row in cur.fetchall()]
            return categories
        except Exception as ex:
            messagebox.showerror("Error", f"Error fetching categories: {str(ex)}", parent=self.root)
            return []
        finally:
            con.close()

    def fetch_suppliers(self):
        con = sqlite3.connect(r'new_ims.db')
        cur = con.cursor()
        try:
            cur.execute("SELECT name FROM supplier")
            suppliers = [row[0] for row in cur.fetchall()]  # Corrected line
            return suppliers
        except Exception as ex:
            messagebox.showerror("Error", f"Error fetching suppliers: {str(ex)}", parent=self.root)
            return []
        finally:
            con.close()


    def show(self):
        con = sqlite3.connect(r'new_ims.db')
        cur = con.cursor()
        try:
            cur.execute("SELECT * FROM product")
            rows = cur.fetchall()
            self.productTable.delete(*self.productTable.get_children())
            for row in rows:
                self.productTable.insert('', END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}", parent=self.root)
        finally:
            con.close()

    def get_data(self, event):
        selected_row = self.productTable.focus()
        row_values = self.productTable.item(selected_row, 'values')

        if row_values:
            self.var_cat.set(row_values[0])
            self.var_sup.set(row_values[1])
            self.var_name.set(row_values[2])
            self.var_price.set(row_values[3])
            self.var_qty.set(row_values[4])
            self.var_status.set(row_values[5])

    def add_product(self):
        con = sqlite3.connect(r'new_ims.db')
        cur = con.cursor()
        try:
            if self.var_name.get() == "":
                messagebox.showerror("Error", "Product Name must be required", parent=self.root)
            else:
                cur.execute("Insert into product (category, supplier, name, price, qty, status) values (?,?,?,?,?,?)",
                            (self.var_cat.get(), self.var_sup.get(), self.var_name.get(), self.var_price.get(), self.var_qty.get(), self.var_status.get()))
                con.commit()
                messagebox.showinfo("Success", "Product Added Successfully", parent=self.root)
                self.clear_fields()
                self.show() #refresh the table
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}", parent=self.root)
        finally:
            con.close()

    def update_product(self):
        con = sqlite3.connect(r'new_ims.db')
        cur = con.cursor()
        try:
            if self.var_name.get() == "":
                messagebox.showerror("Error", "Product Name must be required", parent=self.root)
            else:
                cur.execute("Update product set category=?, supplier=?, price=?, qty=?, status=? where name=?",
                            (self.var_cat.get(), self.var_sup.get(), self.var_price.get(), self.var_qty.get(), self.var_status.get(), self.var_name.get()))
                con.commit()
                messagebox.showinfo("Success", "Product Updated Successfully", parent=self.root)
                self.clear_fields()
                self.show() #refresh the table
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}", parent=self.root)
        finally:
            con.close()

    def delete_product(self):
        con = sqlite3.connect(r'new_ims.db')
        cur = con.cursor()
        try:
            if self.var_name.get() == "":
                messagebox.showerror("Error", "Product Name must be required", parent=self.root)
            else:
                confirm = messagebox.askyesno("Confirm", "Do you really want to delete?", parent=self.root)
                if confirm:
                    cur.execute("Delete from product where name=?", (self.var_name.get(),))
                    con.commit()
                    messagebox.showinfo("Success", "Product Deleted Successfully", parent=self.root)
                    self.clear_fields()
                    self.show() #refresh the table
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}", parent=self.root)
        finally:
            con.close()

    def clear_fields(self):
        if self.categories:
            self.var_cat.set(self.categories[0])
        else:
            self.var_cat.set("")
        if self.suppliers:
            self.var_sup.set(self.suppliers[0])
        else:
            self.var_sup.set("")
        self.var_name.set("")
        self.var_price.set("")
        self.var_qty.set("")
        self.var_status.set("Active")

    def search(self):
        con = sqlite3.connect(r'new_ims.db')
        cur = con.cursor()
        try:
            if self.var_searchby.get() == "Select":
                messagebox.showerror("Error", "Select a search criteria", parent=self.root)
            elif self.var_searchtxt.get() == "":
                messagebox.showerror("Error", "Search input is required", parent=self.root)
            else:
                cur.execute(f"SELECT * FROM product WHERE {self.var_searchby.get().lower()} LIKE ?", ('%' + self.var_searchtxt.get() + '%',))
            rows = cur.fetchall()
            if len(rows) > 0:
                self.productTable.delete(*self.productTable.get_children())
                for row in rows:
                    self.productTable.insert('', END, values=row)
            else:
                messagebox.showinfo("Result", "No matching product found", parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}", parent=self.root)
        finally:
            con.close()

if __name__ == "__main__":
    root = Tk()
    obj = productClass(root)
    root.mainloop()