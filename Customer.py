import sqlite3
from tkinter import *
from tkinter import ttk, messagebox

class CustomerSegmentationClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1100x600+220+130")
        self.root.title("Customer Segmentation Management")
        self.root.config(bg="#f0f0f0")
        self.root.focus_force()

        self.var_segment_id = StringVar()
        self.var_segment_name = StringVar()
        self.var_description = StringVar()
        self.var_customer_name = StringVar()

        lbl_title = Label(self.root, text="Manage Customer Segments", font=("goudy old style", 30), bg="#184a45", fg="white").pack(side=TOP, fill=X)

        lbl_name = Label(self.root, text="Segment Name", font=("goudy old style", 20), bg="white").place(x=50, y=100)
        lbl_name_entry = Entry(self.root, textvariable=self.var_segment_name, font=("goudy old style", 18), bg="skyblue").place(x=50, y=140, width=300)

        lbl_desc = Label(self.root, text="Description", font=("goudy old style", 20), bg="white").place(x=50, y=180)
        lbl_desc_entry = Entry(self.root, textvariable=self.var_description, font=("goudy old style", 18), bg="skyblue").place(x=50, y=220, width=300)

        lbl_cust_name = Label(self.root, text="Customer Name", font=("goudy old style", 20), bg="white").place(x=50, y=260)
        lbl_cust_name_entry = Entry(self.root, textvariable=self.var_customer_name, font=("goudy old style", 18), bg="skyblue").place(x=50, y=300, width=300)

        btn_add = Button(self.root, text="ADD", font=("goudy old style", 15), bg="#4caf50", fg="white", cursor="hand2", command=self.add).place(x=360, y=140, width=150, height=30)
        btn_update = Button(self.root, text="UPDATE", font=("goudy old style", 15), bg="blue", fg="white", cursor="hand2", command=self.update).place(x=360, y=220, width=150, height=30)
        btn_delete = Button(self.root, text="DELETE", font=("goudy old style", 15), bg="red", fg="white", cursor="hand2", command=self.delete).place(x=360, y=300, width=150, height=30)

        segment_frame = Frame(self.root, bd=3, relief=RIDGE)
        segment_frame.place(x=550, y=100, width=600, height=400)

        scrolly = Scrollbar(segment_frame, orient=VERTICAL)
        scrollx = Scrollbar(segment_frame, orient=HORIZONTAL)

        self.SegmentTable = ttk.Treeview(segment_frame, columns=("sid", "name", "description", "customer_name"), yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.config(command=self.SegmentTable.yview)
        scrollx.config(command=self.SegmentTable.xview)

        self.SegmentTable.heading("sid", text="Segment ID")
        self.SegmentTable.heading("name", text="Segment Name")
        self.SegmentTable.heading("description", text="Description")
        self.SegmentTable.heading("customer_name", text="Customer Name")

        self.SegmentTable["show"] = "headings"

        self.SegmentTable.column("sid", width=80)
        self.SegmentTable.column("name", width=150)
        self.SegmentTable.column("description", width=200)
        self.SegmentTable.column("customer_name", width=150)

        self.SegmentTable.pack(fill=BOTH, expand=1)

        self.show()
        self.SegmentTable.bind("<ButtonRelease-1>", self.get_data)

    def add(self):
        con = sqlite3.connect(r'new_ims.db')
        cur = con.cursor()
        try:
            if self.var_segment_name.get() == "":
                messagebox.showerror("Error", "Segment name is required", parent=self.root)
                return
            cur.execute("INSERT INTO customer_segments (name, description, customer_name) VALUES (?, ?, ?)", (self.var_segment_name.get(), self.var_description.get(), self.var_customer_name.get()))
            con.commit()
            messagebox.showinfo("Success", "Segment Added Successfully", parent=self.root)
            self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)
        finally:
            con.close()

    def show(self):
        con = sqlite3.connect(r'new_ims.db')
        cur = con.cursor()
        try:
            cur.execute("SELECT * FROM customer_segments")
            rows = cur.fetchall()
            self.SegmentTable.delete(*self.SegmentTable.get_children())
            for row in rows:
                self.SegmentTable.insert('', END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)
        finally:
            con.close()

    def get_data(self, ev):
        f = self.SegmentTable.focus()
        content = self.SegmentTable.item(f)
        row = content['values']
        self.var_segment_id.set(row[0])
        self.var_segment_name.set(row[1])
        self.var_description.set(row[2])
        self.var_customer_name.set(row[3])

    def update(self):
        con = sqlite3.connect(r'new_ims.db')
        cur = con.cursor()
        try:
            if self.var_segment_id.get() == "":
                messagebox.showerror("Error", "Please select segment from list", parent=self.root)
                return
            cur.execute("UPDATE customer_segments SET name=?, description=?, customer_name=? WHERE sid=?", (self.var_segment_name.get(), self.var_description.get(), self.var_customer_name.get(), self.var_segment_id.get()))
            con.commit()
            messagebox.showinfo("Success", "Segment Updated Successfully", parent=self.root)
            self.show()
            self.var_segment_id.set("")
            self.var_segment_name.set("")
            self.var_description.set("")
            self.var_customer_name.set("")
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)
        finally:
            con.close()

    def delete(self):
        con = sqlite3.connect(r'new_ims.db')
        cur = con.cursor()
        try:
            if self.var_segment_id.get() == "":
                messagebox.showerror("Error", "Please select segment from list", parent=self.root)
                return
            op = messagebox.askyesno("Confirm", "Do you really want to delete?", parent=self.root)
            if op == True:
                cur.execute("DELETE FROM customer_segments WHERE sid=?", (self.var_segment_id.get(),))
                con.commit()
                messagebox.showinfo("Success", "Segment Deleted Successfully", parent=self.root)
                self.show()
                self.var_segment_id.set("")
                self.var_segment_name.set("")
                self.var_description.set("")
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)
        finally:
            con.close()

if __name__ == "__main__":
    root = Tk()
    obj = CustomerSegmentationClass(root)
    root.mainloop()