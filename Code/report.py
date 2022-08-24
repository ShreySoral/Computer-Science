from tkinter import *
from PIL import Image,ImageTk
from tkinter import ttk,messagebox
import mysql.connector
import os
import time
con=mysql.connector.connect(host='localhost',username='root',password='shrey',database='rms')
cur=con.cursor()
cur.execute("select * from session order by sno DESC")
authen=cur.fetchone()
class reportClass:
    def __init__(self,root):
        self.root=root
        self.root.title('Student management sytem')
        self.root.geometry('1200x480+80+170')
        self.root.config(bg='grey')
        self.root.resizable('false','false')
        title= Label(self.root,text='View result details',font=('times',20,'bold'),bg='orange',fg='#262626').place(x=10,y=15,width=1180,height=50)

        self.var_search=StringVar()
        self.var_id=""
        lbl_search=Label(self.root,text='Search by roll no',font=('times',20,'bold'),bg='white').place(x=300,y=100)
        txt_search=Entry(self.root,textvariable=self.var_search,font=('times',20,'bold'),bg='white').place(x=520,y=100,width=150)
        btn_search=Button(self.root,text='search',font=('times',15,'bold'),bg='red',fg='white',command=self.search).place(x=680,y=100,width=100,height=35)
        btn_clear=Button(self.root,text='clear',font=('times',15,'bold'),bg='red',fg='white',command=self.clear).place(x=800,y=100,width=100,height=35)

        rollno=Label(self.root,text='Roll no',font=('times',15,'bold'),bg='white',bd=2,relief=GROOVE).place(x=150,y=230,width=150,height=50)
        name=Label(self.root,text='Name',font=('times',15,'bold'),bg='white',bd=2,relief=GROOVE).place(x=300,y=230,width=150,height=50)
        course=Label(self.root,text='Course',font=('times',15,'bold'),bg='white',bd=2,relief=GROOVE).place(x=450,y=230,width=150,height=50)
        marksobtained=Label(self.root,text='Marks obtained',font=('times',15,'bold'),bg='white',bd=2,relief=GROOVE).place(x=600,y=230,width=150,height=50)
        fullmarks=Label(self.root,text='total marks',font=('times',15,'bold'),bg='white',bd=2,relief=GROOVE).place(x=750,y=230,width=150,height=50)
        percentage=Label(self.root,text='percentage',font=('times',15,'bold'),bg='white',bd=2,relief=GROOVE).place(x=900,y=230,width=150,height=50)



        self.roll=Label(self.root,font=('times',15,'bold'),bg='white',bd=2,relief=GROOVE)
        self.roll.place(x=150,y=280,width=150,height=50)

        self.name=Label(self.root,font=('times',15,'bold'),bg='white',bd=2,relief=GROOVE)
        self.name.place(x=300,y=280,width=150,height=50)

        self.course=Label(self.root,font=('times',15,'bold'),bg='white',bd=2,relief=GROOVE)
        self.course.place(x=450,y=280,width=150,height=50)

        self.marks=Label(self.root,font=('times',15,'bold'),bg='white',bd=2,relief=GROOVE)
        self.marks.place(x=600,y=280,width=150,height=50)

        self.full=Label(self.root,font=('times',15,'bold'),bg='white',bd=2,relief=GROOVE)
        self.full.place(x=750,y=280,width=150,height=50)

        self.per=Label(self.root,font=('times',15,'bold'),bg='white',bd=2,relief=GROOVE)
        self.per.place(x=900,y=280,width=150,height=50)

        if authen[3]=='1':
            btn_delete=Button(self.root,text='delete',font=('times',15,'bold'),bg='red',fg='white',command=self.delete).place(x=500,y=350,width=150,height=35)


    def search(self):
        con=mysql.connector.connect(host='localhost',username='root',password='shrey',database='rms')
        cur=con.cursor()
        try:
            if self.var_search.get()=="":
                messagebox.showerror("Error","roll no required",parent=self.root)
            else:
                cur.execute("select * from result where roll=%s",(self.var_search.get(),))
                row=cur.fetchone()
                if row!=None:
                    self.var_id=row[0]
                    self.roll.config(text=row[1])
                    self.name.config(text=row[2])
                    self.course.config(text=row[3])
                    self.marks.config(text=row[4])
                    self.full.config(text=row[5])
                    self.per.config(text=row[6])
                else:
                    messagebox.showerror("Error","no record found",parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to {str(ex)}")

    def clear(self):
        self.var_id=""
        self.roll.config(text="")
        self.name.config(text="")
        self.course.config(text="")
        self.marks.config(text="")
        self.full.config(text="")
        self.per.config(text="")
        self.var_search.set("")

    def delete(self):
        con=mysql.connector.connect(host='localhost',username='root',password='shrey',database='rms')
        cur=con.cursor()
        try:
            if self.var_id=="":
                messagebox.showerror("Error","Search student result first",parent=self.root)
            else:
                cur.execute("select * from result where rid=%s",(self.var_id,))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Invalid student result",parent=self.root)
                else:
                    op=messagebox.askyesno("Confirm","Do you really want to delete this record?",parent=self.root)
                    if op==True:
                        cur.execute("delete from result where rid=%s",(self.var_id,))
                        con.commit()
                        messagebox.showinfo("Delete","Record deleted successfully",parent=self.root)
                        self.clear()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to {str(ex)}")


if __name__=='__main__':
    root=Tk()
    obj=reportClass(root)
    root.mainloop()