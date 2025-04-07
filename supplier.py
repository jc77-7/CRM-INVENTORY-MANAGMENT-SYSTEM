from tkinter import *
from tkinter import ttk, messagebox
import sqlite3

class SupplierClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1100x600+220+130")
        self.root.title("Inventory Management System | Developed by Nikhila")
        self.root.config(bg="#f0f0f0")  # Light gray background
        self.root.focus_force()

        # Variable declarations
        self.var_searchtxt = StringVar()
        self.var_invoice = StringVar()
        self.var_name = StringVar()
        self.var_contact = StringVar()
        self.var_desc = StringVar()

        # Search Frame
        SearchFrame = LabelFrame(self.root, text="Search Supplier", font=("times new roman", 12, "bold"), bd=2, relief=RIDGE, bg="#e0e0e0")  # Slightly darker background
        SearchFrame.place(x=250, y=20, width=600, height=70)

        lbl_search = Label(SearchFrame, text="Invoice No.", font=("times new roman", 15), bg="#e0e0e0").place(x=10, y=10)
        txt_search = Entry(SearchFrame, textvariable=self.var_searchtxt, font=("times new roman", 15), bg="lightyellow", highlightthickness=1, highlightbackground="#a0a0a0")  # Subtle border
        txt_search.place(x=120, y=10, width=200)

        btn_search = Button(SearchFrame, text="Search", command=self.search, font=("times new roman", 15), bg="#009688", fg="white", cursor="hand2")  # Teal button
        btn_search.place(x=330, y=10, width=180)

        # Supplier Details Section
        title = Label(self.root, text="Manage Supplier Details", font=("times new roman", 15), bg="#0f4d7d", fg="white").place(x=50, y=100, width=1000)

        lbl_invoice = Label(self.root, text="Invoice No.", font=("times new roman", 15), bg="#f0f0f0").place(x=50, y=150)
        txt_invoice = Entry(self.root, textvariable=self.var_invoice, font=("times new roman", 15), bg="lightblue", highlightthickness=1, highlightbackground="#a0a0a0").place(x=150, y=150, width=180)

        lbl_name = Label(self.root, text="Supplier Name", font=("times new roman", 15), bg="#f0f0f0").place(x=350, y=150)
        txt_name = Entry(self.root, textvariable=self.var_name, font=("times new roman", 15), bg="lightblue", highlightthickness=1, highlightbackground="#a0a0a0").place(x=500, y=150, width=180)

        lbl_contact = Label(self.root, text="Contact", font=("times new roman", 15), bg="#f0f0f0").place(x=50, y=190)
        txt_contact = Entry(self.root, textvariable=self.var_contact, font=("times new roman", 15), bg="lightblue", highlightthickness=1, highlightbackground="#a0a0a0").place(x=150, y=190, width=180)

        lbl_desc = Label(self.root, text="Description", font=("times new roman", 15), bg="#f0f0f0").place(x=350, y=190)
        self.txt_desc = Text(self.root, font=("times new roman", 15), bg="lightblue", height=3, highlightthickness=1, highlightbackground="#a0a0a0")
        self.txt_desc.place(x=500, y=190, width=300)

        # Buttons with Hover Effect
        x_start = 850
        button_width = 100
        button_height = 30
        x_padding = 10

        btn_add = Button(self.root, text="Save", command=self.add, font=("times new roman", 15), bg="#4caf50", fg="white", cursor="hand2")
        btn_add.place(x=x_start, y=190, width=button_width, height=button_height)
        btn_add.bind("<Enter>", lambda e: btn_add.config(bg="#28a745"))  # Darker green on hover
        btn_add.bind("<Leave>", lambda e: btn_add.config(bg="#4caf50"))

        x_start += button_width + x_padding
        btn_update = Button(self.root, text="Update", command=self.update, font=("times new roman", 15), bg="#ffc107", fg="white", cursor="hand2")  # Amber color
        btn_update.place(x=x_start, y=190, width=button_width, height=button_height)
        btn_update.bind("<Enter>", lambda e: btn_update.config(bg="#d39e00"))  # Darker amber on hover
        btn_update.bind("<Leave>", lambda e: btn_update.config(bg="#ffc107"))

        x_start += button_width + x_padding
        btn_delete = Button(self.root, text="Delete", command=self.delete, font=("times new roman", 15), bg="#dc3545", fg="white", cursor="hand2")  # Red color
        btn_delete.place(x=x_start, y=190, width=button_width, height=button_height)
        btn_delete.bind("<Enter>", lambda e: btn_delete.config(bg="#c82333"))  # Darker red on hover
        btn_delete.bind("<Leave>", lambda e: btn_delete.config(bg="#dc3545"))

        x_start += button_width + x_padding
        btn_clear = Button(self.root, text="Clear", command=self.clear, font=("times new roman", 15), bg="#007bff", fg="white", cursor="hand2")  # Blue color
        btn_clear.place(x=x_start, y=190, width=button_width, height=button_height)
        btn_clear.bind("<Enter>", lambda e: btn_clear.config(bg="#0069d9"))  # Darker blue on hover
        btn_clear.bind("<Leave>", lambda e: btn_clear.config(bg="#007bff"))

        # Supplier Table
        sup_frame = Frame(self.root, bd=3, relief=RIDGE)
        sup_frame.place(x=0, y=350, relwidth=1, height=150)

        scrolly = Scrollbar(sup_frame, orient=VERTICAL)
        scrollx = Scrollbar(sup_frame, orient=HORIZONTAL)

        self.SupplierTable = ttk.Treeview(sup_frame, columns=("invoice", "name", "contact"))
        self.SupplierTable.heading("invoice", text="Invoice No.")
        self.SupplierTable.heading("name", text="Name")
        self.SupplierTable.heading("contact", text="Contact")

        self.SupplierTable["show"] = "headings"

        self.SupplierTable.column("invoice", width=100)
        self.SupplierTable.column("name", width=100)
        self.SupplierTable.column("contact", width=100)
        self.SupplierTable.pack(fill=BOTH, expand=1)
        self.SupplierTable.bind("<ButtonRelease-1>", self.get_data)

        # Style for Treeview (Alternating Row Colors)
        style = ttk.Style()
        style.configure("Treeview",
                        background="#f5f5f5",  # Light background
                        fieldbackground="#f5f5f5",
                        rowheight=25)
        style.map("Treeview", background=[('selected', '#007bff')])  # Highlight selected row in blue

        self.show()


    def add(self):
        con = sqlite3.connect(r'new_ims.db')
        cur = con.cursor()
        try:
            if self.var_invoice.get() == "":
                messagebox.showerror("Error", "Invoice No. must be required", parent=self.root)
            else:
                cur.execute("Select * from supplier where invoice=?", (self.var_invoice.get(),))
                row = cur.fetchone()
                if row != None:
                    messagebox.showerror("Error", "This Invoice No. already assigned, try different one")
                else:
                    cur.execute("Insert into supplier(invoice,name,contact,description) values(?,?,?,?)", (
                        self.var_invoice.get(),
                        self.var_name.get(),
                        self.var_contact.get(),
                        self.txt_desc.get('1.0', END)
                    ))
                    con.commit()
                    messagebox.showinfo("Supplier added successfully", parent=self.root)
                    self.show()

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}", parent=self.root)

    def update(self):
        con = sqlite3.connect(r'new_ims.db')
        cur = con.cursor()
        try:
            if self.var_invoice.get() == "":
                messagebox.showerror("Error", "Invalid Invoice No.", parent=self.root)
            else:
                cur.execute("Select * from supplier where invoice=?", (self.var_invoice.get(),))
                row = cur.fetchone()
                if row == None:
                    messagebox.showerror("Error", "This Invoice No. is not assigned, try a different one")
                else:
                    cur.execute("update supplier set name=?, contact=?, description=? where invoice=?", (
                        self.var_name.get(),
                        self.var_contact.get(),
                        self.txt_desc.get('1.0', END),
                        self.var_invoice.get()
                    ))
                    con.commit()
                    messagebox.showinfo("Supplier updated successfully", parent=self.root)
                    self.show()

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}", parent=self.root)

    def delete(self):
        con = sqlite3.connect(r'new_ims.db')
        cur = con.cursor()
        try:
            if self.var_invoice.get() == "":
                messagebox.showerror("Error", "Invoice No. must be required", parent=self.root)
            else:
                cur.execute("Select * from supplier where invoice=?", (self.var_invoice.get(),))
                row = cur.fetchone()
                if row == None:
                    messagebox.showerror("Error", "Invalid Invoice No.", parent=self.root)
                else:
                    cur.execute("delete from supplier where invoice=?", (self.var_invoice.get(),))
                    con.commit()
                    messagebox.showinfo("Supplier deleted successfully", parent=self.root)
                    self.show()

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}", parent=self.root)

    def clear(self):
        self.var_invoice.set("")
        self.var_name.set("")
        self.var_contact.set("")
        self.txt_desc.delete('1.0', END)

    def show(self):
        con = sqlite3.connect(r'new_ims.db')
        cur = con.cursor()
        try:
            cur.execute("Select * from supplier")
            rows = cur.fetchall()
            self.SupplierTable.delete(*self.SupplierTable.get_children())
            for row in rows:
                self.SupplierTable.insert('', END, values=row)

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}", parent=self.root)

    def get_data(self, ev):
        f = self.SupplierTable.focus()
        content = (self.SupplierTable.item(f))
        row = content['values']
        self.var_invoice.set(row[0])
        self.var_name.set(row[1])
        self.var_contact.set(row[2])
        self.txt_desc.delete('1.0', END)
        self.txt_desc.insert(END, row[3])  # Assuming description is in the fourth column

    def search(self):
        con = sqlite3.connect(r'new_ims.db')
        cur = con.cursor()
        try:
            if self.var_searchtxt.get() == "":
                messagebox.showerror("Error", "Invoice No. is required for search", parent=self.root)
            else:
                cur.execute("SELECT * FROM supplier WHERE invoice=?", (self.var_searchtxt.get(),))
                rows = cur.fetchall()
                if not rows:
                    messagebox.showinfo("Search Result", "No matching records found.", parent=self.root)
                else:
                    self.SupplierTable.delete(*self.SupplierTable.get_children())
                    for row in rows:
                        self.SupplierTable.insert('', END, values=row)

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}", parent=self.root)

if __name__ == "__main__":
    root = Tk()
    obj = SupplierClass(root)
    root.mainloop()