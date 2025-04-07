from tkinter import *
from tkinter import ttk, messagebox
import sqlite3

class StockClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1200x600+200+100")
        self.root.title("Stock Management System | Developed by [Your Name]")
        self.root.config(bg="#f0f0f0")
        self.root.focus_force()

        self.var_item_id = StringVar()
        self.var_item_name = StringVar()
        self.var_stock_in = IntVar()
        self.var_stock_out = IntVar()
        self.var_overstock = IntVar()
        self.var_total_items = IntVar()

        lbl_title = Label(self.root, text="Stock Management", font=("goudy old style", 30), bg="#184a45", fg="white").pack(side=TOP, fill=X)

        # Item Details Frame
        item_frame = Frame(self.root, bd=3, relief=RIDGE, bg="white")
        item_frame.place(x=20, y=100, width=580, height=250)

        lbl_item_name = Label(item_frame, text="Item Name", font=("goudy old style", 18), bg="white").place(x=20, y=20)
        entry_item_name = Entry(item_frame, textvariable=self.var_item_name, font=("goudy old style", 18), bg="skyblue").place(x=180, y=20, width=350)

        lbl_stock_in = Label(item_frame, text="Stock In", font=("goudy old style", 18), bg="white").place(x=20, y=70)
        entry_stock_in = Entry(item_frame, textvariable=self.var_stock_in, font=("goudy old style", 18), bg="skyblue").place(x=180, y=70, width=150)

        lbl_stock_out = Label(item_frame, text="Stock Out", font=("goudy old style", 18), bg="white").place(x=350, y=70)
        entry_stock_out = Entry(item_frame, textvariable=self.var_stock_out, font=("goudy old style", 18), bg="skyblue").place(x=450, y=70, width=100)

        lbl_overstock = Label(item_frame, text="Overstock", font=("goudy old style", 18), bg="white").place(x=20, y=120)
        entry_overstock = Entry(item_frame, textvariable=self.var_overstock, font=("goudy old style", 18), bg="skyblue").place(x=180, y=120, width=150)

        lbl_total_items = Label(item_frame, text="Total Items", font=("goudy old style", 18), bg="white").place(x=350, y=120)
        entry_total_items = Entry(item_frame, textvariable=self.var_total_items, font=("goudy old style", 18), bg="skyblue").place(x=450, y=120, width=100)

        btn_add = Button(item_frame, text="ADD", font=("goudy old style", 15), bg="#4caf50", fg="white", cursor="hand2", command=self.add).place(x=180, y=180, width=120, height=30)
        btn_update = Button(item_frame, text="UPDATE", font=("goudy old style", 15), bg="#2196f3", fg="white", cursor="hand2", command=self.update).place(x=320, y=180, width=120, height=30)
        btn_delete = Button(item_frame, text="DELETE", font=("goudy old style", 15), bg="red", fg="white", cursor="hand2", command=self.delete).place(x=460, y=180, width=120, height=30)

        # Stock Details Frame
        stock_frame = Frame(self.root, bd=3, relief=RIDGE, bg="white")
        stock_frame.place(x=620, y=100, width=560, height=480)

        scrolly = Scrollbar(stock_frame, orient=VERTICAL)
        scrollx = Scrollbar(stock_frame, orient=HORIZONTAL)

        self.StockTable = ttk.Treeview(stock_frame, columns=("iid", "name", "stock_in", "stock_out", "overstock", "total"), yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.config(command=self.StockTable.yview)
        scrollx.config(command=self.StockTable.xview)

        self.StockTable.heading("iid", text="Item ID")
        self.StockTable.heading("name", text="Item Name")
        self.StockTable.heading("stock_in", text="Stock In")
        self.StockTable.heading("stock_out", text="Stock Out")
        self.StockTable.heading("overstock", text="Overstock")
        self.StockTable.heading("total", text="Total Items")

        self.StockTable["show"] = "headings"

        self.StockTable.column("iid", width=50)
        self.StockTable.column("name", width=150)
        self.StockTable.column("stock_in", width=80)
        self.StockTable.column("stock_out", width=80)
        self.StockTable.column("overstock", width=80)
        self.StockTable.column("total", width=80)

        self.StockTable.pack(fill=BOTH, expand=1)

        self.show()
        self.StockTable.bind("<ButtonRelease-1>", self.get_data)

    def add(self):
        con = sqlite3.connect(r'new_ims.db')
        cur = con.cursor()
        try:
            if self.var_item_name.get() == "":
                messagebox.showerror("Error", "Item name is required", parent=self.root)
                return
            cur.execute("INSERT INTO stocks (name, stock_in, stock_out, overstock, total) VALUES (?, ?, ?, ?, ?)",
                        (self.var_item_name.get(), self.var_stock_in.get(), self.var_stock_out.get(), self.var_overstock.get(), self.var_total_items.get()))
            con.commit()
            messagebox.showinfo("Success", "Item Added Successfully", parent=self.root)
            self.show()
            self.clear()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)
        finally:
            con.close()

    def show(self):
        con = sqlite3.connect(r'new_ims.db')
        cur = con.cursor()
        try:
            cur.execute("SELECT * FROM stocks")
            rows = cur.fetchall()
            self.StockTable.delete(*self.StockTable.get_children())
            for row in rows:
                self.StockTable.insert('', END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)
        finally:
            con.close()

    def get_data(self, ev):
        f = self.StockTable.focus()
        content = self.StockTable.item(f)
        row = content['values']
        self.var_item_id.set(row[0])
        self.var_item_name.set(row[1])
        self.var_stock_in.set(row[2])
        self.var_stock_out.set(row[3])
        self.var_overstock.set(row[4])
        self.var_total_items.set(row[5])

    def update(self):
        con = sqlite3.connect(r'new_ims.db')
        cur = con.cursor()
        try:
            if self.var_item_id.get() == "":
                messagebox.showerror("Error", "Please select item from list", parent=self.root)
                return
            cur.execute("UPDATE stocks SET name=?, stock_in=?, stock_out=?, overstock=?, total=? WHERE iid=?",
                        (self.var_item_name.get(), self.var_stock_in.get(), self.var_stock_out.get(), self.var_overstock.get(), self.var_total_items.get(), self.var_item_id.get()))
            con.commit()
            messagebox.showinfo("Success", "Item Updated Successfully", parent=self.root)
            self.show()
            self.clear()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)
        finally:
            con.close()

    def delete(self):
        con = sqlite3.connect(r'new_ims.db')
        cur = con.cursor()
        try:
            if self.var_item_id.get() == "":
                messagebox.showerror("Error", "Please select item from list", parent=self.root)
                return
            op = messagebox.askyesno("Confirm", "Do you really want to delete?", parent=self.root)
            if op == True:
                cur.execute("DELETE FROM stocks WHERE iid=?", (self.var_item_id.get(),))
                con.commit()
                messagebox.showinfo("Success", "Item Deleted Successfully", parent=self.root)
                self.show()
                self.clear()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)
        finally:
            con.close()

    def clear(self):
      self.var_item_id.set("")
      self.var_item_name.set("")
      self.var_stock_in.set(0)
      self.var_stock_out.set(0)
      self.var_overstock.set(0)
      self.var_total_items.set(0)


if __name__ == "__main__":
    root = Tk()
    obj = StockClass(root)
    root.mainloop()