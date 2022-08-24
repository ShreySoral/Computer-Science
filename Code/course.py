from tkinter import *
from PIL import Image,ImageTk
from tkinter import ttk,messagebox
import mysql.connector
import os
con=mysql.connector.connect(host='localhost',username='root',password='shrey',database='rms')
cur=con.cursor(buffered=True)
cur.execute("SELECT * FROM session order by sno DESC")
authen = cur.fetchone()
print(authen)
class CourseClass:
    def __init__(self,root):
        self.root=root
        self.root.title('Student management sytem')
        self.root.geometry('1200x480+80+170')
        self.root.config(bg='white')
        self.root.resizable('false','false')
        title= Label(self.root,text='Manage course details',font=('times',20,'bold'),bg='blue',fg='white').place(x=10,y=15,width=1180,height=35)

        self.var_course=StringVar()
        self.var_duration=StringVar()
        self.var_charges=StringVar()
       

        lbl_courseName= Label(self.root,text='course name',font=('times',15,'bold'),bg='white').place(x=10,y=60)
        lbl_duration= Label(self.root,text='Duration',font=('times',15,'bold'),bg='white').place(x=10,y=100)
        lbl_charges= Label(self.root,text='Charges',font=('times',15,'bold'),bg='white').place(x=10,y=140)
        lbl_description= Label(self.root,text='Description',font=('times',15,'bold'),bg='white').place(x=10,y=180)


        self.txt_courseName= Entry(self.root,textvariable=self.var_course,font=('times',15,'bold'),bg='white')
        self.txt_courseName.place(x=150,y=60,width=200)
        txt_duration= Entry(self.root,textvariable=self.var_duration,font=('times',15,'bold'),bg='white').place(x=150,y=100,width=200)
        txt_charges= Entry(self.root,textvariable=self.var_charges,font=('times',15,'bold'),bg='white').place(x=150,y=140,width=200)
        self.txt_description= Text(self.root,font=('times',15,'bold'),bg='white')
        self.txt_description.place(x=150,y=180,width=500,height=130)

        #buttons#
        self.btn_add=Button(self.root,text='Save',font=('times',15,'bold'),bg='red',fg='white',command=self.add)
        self.btn_add.place(x=150,y=400,width=110,height=40)

        self.btn_update=Button(self.root,text='Update',font=('times',15,'bold'),bg='red',fg='white',command=self.update)
        self.btn_update.place(x=270,y=400,width=110,height=40)
        
        if authen[3] == "1":
            self.btn_delete=Button(self.root,text='Delete',font=('times',15,'bold'),bg='red',fg='white',command=self.delete)
            self.btn_delete.place(x=390,y=400,width=110,height=40)

        self.btn_clear=Button(self.root,text='Clear',font=('times',15,'bold'),bg='red',fg='white',command=self.clear)
        self.btn_clear.place(x=510,y=400,width=110,height=40)

        self.var_search=StringVar()
        lbl_search_coursename=Label(self.root,text='Search by course',font=('times',15,'bold'),bg='white').place(x=720,y=60)
        txt_search_courseName= Entry(self.root,textvariable=self.var_search,font=('times',15,'bold'),bg='white').place(x=870,y=60,width=180)
        btn_search=Button(self.root,text='Search',font=('times',15,'bold'),bg='red',fg='white',command=self.search).place(x=1070,y=60,width=120,height=28)


        self.C_frame=Frame(self.root,bd=2,relief=RIDGE)
        self.C_frame.place(x=720,y=100,width=470,height=340)
        
        scrolly=Scrollbar(self.C_frame,orient=VERTICAL)
        scrollx=Scrollbar(self.C_frame,orient=HORIZONTAL)
        self.CourseTable=ttk.Treeview(self.C_frame,columns=('cid','name','duration','charges','description'),xscrollcommand=scrollx.set,yscrollcommand=scrolly.set)

        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.CourseTable.xview)
        scrolly.config(command=self.CourseTable.yview)

        self.CourseTable.heading('cid',text='CourseID')
        self.CourseTable.heading('name',text='Name')
        self.CourseTable.heading('duration',text='duration')
        self.CourseTable.heading('charges',text='charges')
        self.CourseTable.heading('description',text='description')
        self.CourseTable['show']='headings'
        self.CourseTable.column('cid',width=100)
        self.CourseTable.column('name',width=100)
        self.CourseTable.column('duration',width=100)
        self.CourseTable.column('charges',width=100)
        self.CourseTable.column('description',width=150)
        self.CourseTable.pack(fill=BOTH,expand=1)
        self.CourseTable.bind("<ButtonRelease-1>",self.get_data)
        self.show()


    def clear(self):
        self.show()
        self.var_course.set("")
        self.var_duration.set("")
        self.var_charges.set("")
        self.var_search.set("")
        self.txt_description.delete('1.0',END)
        self.txt_courseName.config(state=NORMAL)



    def get_data(self,ev):
        self.txt_courseName.config(state='readonly')
        self.txt_courseName
        r=self.CourseTable.focus()
        content=self.CourseTable.item(r)
        row=content["values"]
        print(row)
        self.var_course.set(row[0])
        self.var_duration.set(row[2])
        self.var_charges.set(row[3])
        # self.var_course.set(row[4])
        self.txt_description.delete('1.0',END)
        self.txt_description.insert(END,row[4])

    def add(self):
        try:
            if self.var_course.get() and self.var_charges.get()=="":
                messagebox.showerror("Error","all fields are required",parent=self.root)
            else:
                cur.execute("select * from course where name=%s",(self.var_course.get(),))
                row=cur.fetchone()
                if row!=None:
                    messagebox.showerror("Error","Course name already present",parent=self.root)
                else:
                    cur.execute("insert into course (name,duration,charges,description) values(%s,%s,%s,%s)",(self.var_course.get(),self.var_duration.get(),self.var_charges.get(),
                        self.txt_description.get("1.0",END)
                    ))
                    con.commit()
                    messagebox.showinfo("Success","Record added successfully",parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to{str(ex)}")


    def show(self):
        try:
            cur.execute("select * from course")
            rows= cur.fetchall()
            self.CourseTable.delete(*self.CourseTable.get_children())
            for row in rows:
                self.CourseTable.insert('',END,values=row)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to {str(ex)}")

    def update(self):
        try:
            if self.var_course.get() and self.var_charges.get()=="":
                messagebox.showerror("Error","All fields are required",parent=self.root)
            else:
                print(self.var_course.get())
                cur.execute("select * from course where cid = %s",(self.var_course.get(),))
                row=cur.fetchone()
                #print(row)
                if row==None:
                    messagebox.showerror("Error","Select course from list",parent=self.root)
                else:
                    cur.execute("update course set duration=%s, charges=%s, description=%s where cid=%s",(
                        self.var_duration.get(),
                        self.var_charges.get(),
                        self.txt_description.get("1.0",END),
                        self.var_course.get()
                    ))
                    con.commit()
                    messagebox.showinfo("Success","Record Updated successfully",parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to{str(ex)}")

    def delete(self):
        con=mysql.connector.connect(host='localhost',username='root',password='shrey',database='rms')
        cur=con.cursor()
        try:
            if self.var_course.get() and self.var_charges.get()=="":
                messagebox.showerror("Error","All fields are required",parent=self.root)
            else:
                 cur.execute("select * from course where cid=%s",(self.var_course.get(),))
                 row=cur.fetchone()
                 if row==None:
                    messagebox.showerror("Error","Please select the course from the list first",parent=self.root)
                 else:
                      op=messagebox.askyesno("Confirm","Do you really want to delete this course?",parent=self.root)
                      if op==True:
                        cur.execute("delete from course where cid=%s",(self.var_course.get(),))
                        con.commit()
                        messagebox.showinfo("Delete","Course deleted successfully",parent=self.root)
                        self.clear
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to {str(ex)}")
                    


    def search(self):
        try:
            cur.execute(f"select * from course where name LIKE '%{self.var_search.get()}%'")
            rows=cur.fetchall()
            self.CourseTable.delete(*self.CourseTable.get_children())
            for row in rows:
                self.CourseTable.insert('',END,values=row)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to {str(ex)}")



if __name__=='__main__':
    root=Tk()
    obj=CourseClass(root)
    root.mainloop()