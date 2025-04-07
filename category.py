from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import sqlite3

class categoryClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1100x600+220+130")
        self.root.title("Inventory Management System | Developed by Nikhila")
        self.root.config(bg="#f0f0f0")
        self.root.focus_force()

        self.var_cat_id = StringVar()
        self.var_name = StringVar()

        lbl_title = Label(self.root, text="Manage Product Category", font=("goudy old style", 30), bg="#184a45", fg="white").pack(side=TOP, fill=X)
        lbl_name = Label(self.root, text="Enter Category Name", font=("goudy old style", 30), bg="white").place(x=50, y=100)
        lbl_name_entry = Entry(self.root, textvariable=self.var_name, font=("goudy old style", 18), bg="skyblue").place(x=50, y=170, width=300)

        btn_add = Button(self.root, text="ADD", font=("goudy old style", 15), bg="#4caf50", fg="white", cursor="hand2", command=self.add).place(x=360, y=170, width=150, height=30)
        btn_delete = Button(self.root, text="DELETE", font=("goudy old style", 15), bg="red", fg="white", cursor="hand2", command=self.delete).place(x=520, y=170, width=150, height=30)

        cat_frame = Frame(self.root, bd=3, relief=RIDGE)
        cat_frame.place(x=680, y=100, width=350, height=200)  # Reduced height

        scrolly = Scrollbar(cat_frame, orient=VERTICAL)
        scrollx = Scrollbar(cat_frame, orient=HORIZONTAL)

        self.CategoryTable = ttk.Treeview(cat_frame, columns=("cid", "name"), yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.config(command=self.CategoryTable.yview)
        scrollx.config(command=self.CategoryTable.xview)

        self.CategoryTable.heading("cid", text="C ID")
        self.CategoryTable.heading("name", text="Name")

        self.CategoryTable["show"] = "headings"

        self.CategoryTable.column("cid", width=90)
        self.CategoryTable.column("name", width=200)  # Increased width for "Name"
        self.CategoryTable.pack(fill=BOTH, expand=1)

        self.im1 = Image.open("images/category.jpg")
        self.im1 = self.im1.resize((500, 250), Image.LANCZOS)
        self.im1 = ImageTk.PhotoImage(self.im1)

        self.im2 = Image.open("images/cat2.jpg")
        self.im2 = self.im2.resize((500, 250), Image.LANCZOS)
        self.im2 = ImageTk.PhotoImage(self.im2)

        self.show()
        self.CategoryTable.bind("<ButtonRelease-1>", self.get_data)

        # Get the y coordinate of the bottom of cat_frame
        cat_frame_y_bottom = 100 + 200 + 20  # Reduced height value used.

        self.lbl_im1 = Label(self.root, image=self.im1, bd=2, relief=RAISED)
        self.lbl_im1.place(x=50, y=cat_frame_y_bottom)

        self.lbl_im2 = Label(self.root, image=self.im2, bd=2, relief=RAISED)
        self.lbl_im2.place(x=580, y=cat_frame_y_bottom)

    # Rest of the class remains the same (add, show, get_data, delete)
    def add(self):
        con = sqlite3.connect(r'new_ims.db')
        cur = con.cursor()
        try:
            if self.var_name.get() == "":
                messagebox.showerror("Error", "Category name is required", parent=self.root)
                return
            cur.execute("INSERT INTO category (name) VALUES (?)", (self.var_name.get(),))
            con.commit()
            messagebox.showinfo("Success", "Category Added Successfully", parent=self.root)
            self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)
        finally:
            con.close()

    def show(self):
        con = sqlite3.connect(r'new_ims.db')
        cur = con.cursor()
        try:
            cur.execute("SELECT * FROM category")
            rows = cur.fetchall()
            self.CategoryTable.delete(*self.CategoryTable.get_children())
            for row in rows:
                self.CategoryTable.insert('', END, values=row) # row is already a tuple (cid,name)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)
        finally:
            con.close()

    def get_data(self, ev):
        f = self.CategoryTable.focus()
        content = self.CategoryTable.item(f)
        row = content['values']
        self.var_cat_id.set(row[0])
        self.var_name.set(row[1])

    def delete(self):
        con = sqlite3.connect(r'new_ims.db')
        cur = con.cursor()
        try:
            if self.var_cat_id.get() == "":
                messagebox.showerror("Error", "Please select category from list", parent=self.root)
                return
            op = messagebox.askyesno("Confirm", "Do you really want to delete?", parent=self.root)
            if op == True:
                cur.execute("DELETE FROM category WHERE cid=?", (self.var_cat_id.get(),))
                con.commit()
                messagebox.showinfo("Success", "Category Deleted Successfully", parent=self.root)
                self.show()
                self.var_cat_id.set("")
                self.var_name.set("")

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)
        finally:
            con.close()

if __name__ == "__main__":
    root = Tk()
    obj = categoryClass(root)
    root.mainloop()