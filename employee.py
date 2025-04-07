from tkinter import *
from tkinter import ttk,messagebox
import sqlite3
import datetime

class employeeClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1100x600+220+130")  # Increased height
        self.root.title("Inventory Management System | Developed by Nikhila")
        self.root.config(bg="white")
        self.root.focus_force()

        # Variable declarations
        self.var_searchby = StringVar()
        self.var_searchtxt = StringVar()

        self.var_emp_id = StringVar()
        self.var_name_id = StringVar()
        self.var_email_id = StringVar()
        self.var_contact_id = StringVar()
        self.var_gender_id = StringVar()
        self.var_pass_id = StringVar()
        self.var_dob_id = StringVar()
        self.var_doj_id = StringVar()
        self.var_utype_id = StringVar()
        self.var_salary = StringVar()
        self.var_address = StringVar()


        # Search Frame
        SearchFrame = LabelFrame(self.root, text="Search Employee", font=("times new roman", 12, "bold"), bd=2, relief=RIDGE, bg="white")
        SearchFrame.place(x=250, y=20, width=600, height=70)

        cmb_search = ttk.Combobox(SearchFrame, textvariable=self.var_searchby, values=("Select", "Email", "Name", "Contact"), state='readonly', justify=CENTER, font=("times new roman", 15))
        cmb_search.place(x=10, y=10, width=180)
        cmb_search.current(0)

        txt_search = Entry(SearchFrame, textvariable=self.var_searchtxt, font=("times new roman", 15), bg="lightyellow")
        txt_search.place(x=200, y=10, width=200)

        btn_search = Button(SearchFrame, text="Search", font=("times new roman", 15), bg="#4caf50", fg="white", cursor="hand2")  # Add command here later
        btn_search.place(x=410, y=10, width=180)


        # Employee Details Section
        title = Label(self.root, text="Employee Details", font=("times new roman", 15), bg="#0f4d7d", fg="white", cursor="hand2").place(x=50, y=100, width=1000)

        lbl_empid = Label(self.root, text="Emp ID", font=("times new roman", 15), bg="white").place(x=50, y=150)
        txt_empid = Entry(self.root, textvariable=self.var_emp_id, font=("times new roman", 15), bg="lightblue").place(x=120, y=150, width=180)

        lbl_name = Label(self.root, text="Name", font=("times new roman", 15), bg="white").place(x=350, y=150)
        txt_name = Entry(self.root, textvariable=self.var_name_id, font=("times new roman", 15), bg="lightblue")
        txt_name.place(x=440, y=150, width=180)

        lbl_email = Label(self.root, text="Email", font=("times new roman", 15), bg="white").place(x=650, y=150)
        txt_email = Entry(self.root, textvariable=self.var_email_id, font=("times new roman", 15), bg="lightblue").place(x=750, y=150, width=180)

        lbl_contact = Label(self.root, text="Contact", font=("times new roman", 15), bg="white").place(x=50, y=190)
        txt_contact = Entry(self.root, textvariable=self.var_contact_id, font=("times new roman", 15), bg="lightblue").place(x=120, y=190, width=180)

        lbl_gender = Label(self.root, text="Gender", font=("times new roman", 15), bg="white").place(x=350, y=190)
        cmb_gender = ttk.Combobox(self.root, textvariable=self.var_gender_id, values=("Select", "Male", "Female", "Others"), state='readonly', justify=CENTER, font=("times new roman", 15))
        cmb_gender.place(x=440, y=190, width=180)
        cmb_gender.current(0)

        lbl_dob = Label(self.root, text="D.O.B", font=("times new roman", 15), bg="white").place(x=650, y=190)
        txt_dob = Entry(self.root, textvariable=self.var_dob_id, font=("times new roman", 15), bg="lightblue").place(x=750, y=190, width=180)

        lbl_doj = Label(self.root, text="D.O.J", font=("times new roman", 15), bg="white").place(x=50, y=230)
        txt_doj = Entry(self.root, textvariable=self.var_doj_id, font=("times new roman", 15), bg="lightblue").place(x=120, y=230, width=180)

        lbl_utype = Label(self.root, text="User Type", font=("times new roman", 15), bg="white").place(x=350, y=230)
        cmb_utype = ttk.Combobox(self.root, textvariable=self.var_utype_id, values=("Select", "Admin", "Employee"), state='readonly', justify=CENTER, font=("times new roman", 15))
        cmb_utype.place(x=440, y=230, width=180)
        cmb_utype.current(0)

        lbl_salary = Label(self.root, text="Salary", font=("times new roman", 15), bg="white").place(x=650, y=230)
        txt_salary = Entry(self.root, textvariable=self.var_salary, font=("times new roman", 15), bg="lightblue").place(x=750, y=230, width=180)

        lbl_address = Label(self.root, text="Address", font=("times new roman", 15), bg="white").place(x=50, y=270)  # New Label
        self.txt_address = Text(self.root, font=("times new roman", 15), bg="lightblue", height=3)  # Use Text widget for multiline
        self.txt_address.place(x=120, y=270, width=500)  # Wider for address


        x_start = 650  # Starting x-coordinate for the buttons
        button_width = 100  # Width of each button
        button_height = 30 #height of each button
        x_padding = 10   # Padding between buttons

        btn_add = Button(self.root, text="Save",command=self.add,font=("times new roman", 15), bg="#4caf50", fg="white", cursor="hand2")
        btn_add.place(x=x_start, y=270, width=button_width, height=button_height)

        x_start += button_width + x_padding  # Update x for the next button
        btn_update = Button(self.root, text="Update", command=self.update, font=("times new roman", 15), bg="#4caf50", fg="white", cursor="hand2")
        btn_update.place(x=x_start, y=270, width=button_width, height=button_height)

        x_start += button_width + x_padding  # Update x for the next button
        btn_clear = Button(self.root, text="Clear", font=("times new roman", 15), bg="#4caf50", fg="white", cursor="hand2")
        btn_clear.place(x=x_start, y=270, width=button_width, height=button_height)

        x_start += button_width + x_padding  # Update x for the next button
        btn_delete = Button(self.root, text="Delete", font=("times new roman", 15), bg="#4caf50", fg="white", cursor="hand2")
        btn_delete.place(x=x_start, y=270, width=button_width, height=button_height)

        emp_frame=Frame(self.root,bd=3,relief=RIDGE)
        emp_frame.place(x=0,y=350,relwidth=1,height=150)

        scrolly=Scrollbar(emp_frame,orient=VERTICAL)
        scrollx=Scrollbar(emp_frame,orient=HORIZONTAL)

        self.EmployeeTable=ttk.Treeview(emp_frame,columns=("emp_id","name","gender","dob","doj","pass","utype"))
        self.EmployeeTable.heading("emp_id",text="EMP ID")
        self.EmployeeTable.heading("name",text="NAME")
        self.EmployeeTable.heading("gender",text="GENDER")
        self.EmployeeTable.heading("dob",text="DOB")
        self.EmployeeTable.heading("doj",text="DOJ")
        self.EmployeeTable.heading("pass",text="PASS")
        self.EmployeeTable.heading("utype",text="UTYPE")

        self.EmployeeTable["show"]="headings"

        self.EmployeeTable.column("emp_id",width=90)
        self.EmployeeTable.column("name",width=100)
        self.EmployeeTable.column("gender",width=100)
        self.EmployeeTable.column("dob",width=100)
        self.EmployeeTable.column("doj",width=100)
        self.EmployeeTable.column("pass",width=100)
        self.EmployeeTable.column("utype",width=100)
        self.EmployeeTable.pack(fill=BOTH,expand=1)
        self.EmployeeTable.bind("<ButtonRelease-1>",self.get_data)
        self.show()



    def add(self):
        con = sqlite3.connect(r'new_ims.db')
        cur = con.cursor()
        try:
            if self.var_emp_id.get() == "":
                messagebox.showerror("Error", "Employee ID must be required", parent=self.root)
            else:
                cur.execute("Select * from employee where emp_id=?", (self.var_emp_id.get(),))
                row = cur.fetchone()
                if row != None:
                    messagebox.showerror("Error", "This employee ID already assigned, try different one")
                else:
                    cur.execute("Insert into employee(emp_id,name,gender,dob,doj,pass,utype,address)values(?,?,?,?,?,?,?,?)", (
                        self.var_emp_id.get(),
                        self.var_name_id.get(), #you still need to change this to var_name
                        self.var_gender_id.get(),
                        self.var_dob_id.get(),
                        self.var_doj_id.get(),
                        self.var_pass_id.get(),
                        self.var_utype_id.get(),
                        self.txt_address.get('1.0', END)
                    ))
                    con.commit()
                    messagebox.showinfo("Employee added successfully", parent=self.root)
                    self.show()

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}", parent=self.root)


    def show(self):
        con = sqlite3.connect(r'new_ims.db')
        cur = con.cursor()
        try:
            cur.execute("Select * from employee")
            rows = cur.fetchall()
            self.EmployeeTable.delete(*self.EmployeeTable.get_children())
            for row in rows:
                self.EmployeeTable.insert('',END,values=row)

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}", parent=self.root)

    def get_data(self,ev):
        f=self.EmployeeTable.focus()
        content = (self.EmployeeTable.item(f))
        row = content['values']
        #print(row)
        self.var_emp_id.set(row[0])
        self.var_name_id.set(row[1]) 
        self.var_gender_id.set(row[2])
        self.var_dob_id.set(row[3])
        self.var_doj_id.set(row[4])
        self.var_pass_id.set(row[5])
        self.var_utype_id.set(row[6])
        self.txt_address.delete('1.0', END)
        self.txt_address.insert(END,row[7])


    def update(self):
        con = sqlite3.connect(r'new_ims.db')
        cur = con.cursor()
        try:
            if self.var_emp_id.get() == "":
                messagebox.showerror("Error", "Invalid Employee ID", parent=self.root)
            else:
                cur.execute("Select * from employee where emp_id=?", (self.var_emp_id.get(),))
                row = cur.fetchone()
                if row == None:
                    messagebox.showerror("Error", "This employee ID already assigned, try different one")
                else:
                    cur.execute("update employee set name=?,gender=?,dob=?,doj=?,pass=?,utype=?,address=? where emp_id=?", (
                        self.var_name_id.get(), #you still need to change this to var_name
                        self.var_gender_id.get(),
                        self.var_dob_id.get(),
                        self.var_doj_id.get(),
                        self.var_pass_id.get(),
                        self.var_utype_id.get(),
                        self.txt_address.get('1.0', END),
                        self.var_emp_id.get()
                    ))
                    con.commit()
                    messagebox.showinfo("Employee updated successfully", parent=self.root)
                    self.show()

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}", parent=self.root)

if __name__ == "__main__":
    root = Tk()
    obj = employeeClass(root)
    root.mainloop()