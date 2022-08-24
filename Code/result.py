from tkinter import *
from PIL import Image,ImageTk
from tkinter import ttk,messagebox
import mysql.connector
import os
import time

class resultClass:
    def __init__(self,root):
        self.root=root
        self.root.title('Student management sytem')
        self.root.geometry('1200x480+80+170')
        self.root.config(bg='crimson')
        self.root.resizable('false','false')
        title= Label(self.root,text='Add Marks details',font=('times',20,'bold'),bg='orange',fg='#262626').place(x=10,y=15,width=1180,height=50)
        self.var_roll=StringVar()
        self.var_name=StringVar()
        self.var_course=StringVar()
        self.var_marks=StringVar()
        self.var_full_marks=StringVar()
        self.roll_list=[]
        self.fetch_roll()
        lbl_select=Label(self.root,text='Select student',font=('times',20,'bold'),bg='white').place(x=50,y=100)
        lbl_name=Label(self.root,text='Name',font=('times',20,'bold'),bg='white').place(x=50,y=160)
        lbl_course=Label(self.root,text='Course',font=('times',20,'bold'),bg='white').place(x=50,y=220)
        lbl_marksobtained=Label(self.root,text='Marks obtained',font=('times',20,'bold'),bg='white').place(x=50,y=280)
        lbl_fullmarks=Label(self.root,text='full marks',font=('times',20,'bold'),bg='white').place(x=50,y=340)


        self.txt_student= ttk.Combobox(self.root,textvariable=self.var_roll,values=self.roll_list,font=('times',15,'bold'),state='readonly',justify=CENTER)
        self.txt_student.place(x=280,y=100,width=200)
        self.txt_student.set("Select")
        btn_search=Button(self.root,text='search',font=('times',15,'bold'),bg='black',fg='white',command=self.search).place(x=500,y=100,width=100,height=28)

        txt_name= Entry(self.root,textvariable=self.var_name,font=('times',20,'bold'),bg='white',state='readonly').place(x=280,y=160,width=320)
        txt_course= Entry(self.root,textvariable=self.var_course,font=('times',20,'bold'),bg='white',state='readonly').place(x=280,y=220,width=320)
        txt_marks= Entry(self.root,textvariable=self.var_marks,font=('times',20,'bold'),bg='white').place(x=280,y=280,width=320)
        txt_fullmarks= Entry(self.root,textvariable=self.var_full_marks,font=('times',20,'bold'),bg='white').place(x=280,y=340,width=320)


        button_add=Button(self.root,text='submit',font=('times',20,'bold'),bg='gold',activebackground='lightblue',command=self.add).place(x=300,y=420,width=120,height=35)
        button_clear=Button(self.root,text='clear',font=('times',20,'bold'),bg='gold',activebackground='lightblue',command=self.clear).place(x=430,y=420,width=120,height=35)




    def fetch_roll(self):
        con=mysql.connector.connect(host='localhost',username='root',password='shrey',database='rms')
        cur=con.cursor()
        try:
            cur.execute("select roll from student")
            rows= cur.fetchall()
            if len(rows)>0:
                for row in rows:
                    self.roll_list.append(row[0])
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to {str(ex)}")


    def search(self):
        con=mysql.connector.connect(host='localhost',username='root',password='shrey',database='rms')
        cur=con.cursor()
        try:
            cur.execute("select name,course from student where roll=%s",(self.var_roll.get(),))
            row=cur.fetchone()
            if row!=None:
                self.var_name.set(row[0])
                self.var_course.set(row[1])
            else:
                messagebox.showerror("Error","No record found",parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to {str(ex)}")

    def add(self):
        con=mysql.connector.connect(host='localhost',username='root',password='shrey',database='rms')
        cur=con.cursor()
        try:
            if self.var_name.get()=="":
                messagebox.showerror("Error","please first search student record",parent=self.root)
            else:
                cur.execute("select * from result where roll=%s and course=%s",(self.var_roll.get(),self.var_course.get(),))
                row=cur.fetchone()
                if row!=None:
                    messagebox.showerror("Error","Result already present",parent=self.root)
                else:
                    per=(float(self.var_marks.get())*100)/float(self.var_full_marks.get())
                    cur.execute("insert into result (roll,name,course,marks_ob,full_marks,per_1) values(%s,%s,%s,%s,%s,%s)",(
                        self.var_roll.get(),
                        self.var_name.get(),
                        self.var_course.get(),
                        self.var_marks.get(),
                        self.var_full_marks.get(),
                        str(per)
                    ))
                    con.commit()
                    messagebox.showinfo("Success","Result added successfully",parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to{str(ex)}")



    def clear(self):
        self.var_roll.set("Select")
        self.var_name.set("")
        self.var_course.set("")
        self.var_marks.set("")
        self.var_full_marks.set("")



if __name__=='__main__':
    root=Tk()
    obj=resultClass(root)
    root.mainloop()