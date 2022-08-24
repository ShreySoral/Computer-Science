from tkinter import *
from tkinter import messagebox 
from PIL import Image,ImageTk
from course import CourseClass
from student import studentClass
from result import resultClass
from report import reportClass
import os
import time
import mysql.connector

con = mysql.connector.connect(host="localhost",user="root",password="shrey",database="rms")
cur = con.cursor(buffered=True)
cur.execute("SELECT * FROM session order by sno DESC")
authen = cur.fetchone()
if authen == None:
    os.system("python register.py")
    os._exit(0)



class SMS:
    def __init__(self,root):
        self.root=root
        self.root.title('Student management sytem')
        self.root.geometry('1350x700+0+0')
        self.root.config(bg='red')
        self.root.resizable('False','False')
        title= Label(self.root,text='Student  management system',font=('times',20,'bold'),bg='blue',fg='white').place(x=0,y=0,relwidth=1,height=50)

        M_frame=LabelFrame(self.root,text='Menus',font=('times',15,'bold'),bg='white')
        M_frame.place(x=10,y=70,width=1340,height=80)

        btn_courses=Button(M_frame,text='Course',font=('times',15,'bold'),bg='blue',fg='white',command=self.add_course).place(x=20,y=5,width=200,height=40)
        btn_student=Button(M_frame,text='Student',font=('times',15,'bold'),bg='blue',fg='white',command=self.add_student).place(x=240,y=5,width=200,height=40)
        btn_result=Button(M_frame,text='Marks',font=('times',15,'bold'),bg='blue',fg='white',command=self.add_result).place(x=460,y=5,width=200,height=40)
        btn_view=Button(M_frame,text='View Student Results',font=('times',15,'bold'),bg='blue',fg='white',command=self.add_report).place(x=680,y=5,width=200,height=40)
        btn_logout=Button(M_frame,text='Logout',font=('times',15,'bold'),bg='blue',fg='white',command=self.logout).place(x=900,y=5,width=200,height=40)
        btn_exit=Button(M_frame,text='Exit',font=('times',15,'bold'),bg='blue',fg='white',command=self.exit).place(x=1120,y=5,width=200,height=40)

        #self.lbl_img=Image.open("login/csia.jpg")
        #self.lbl_img=self.lbl_img.resize((920,400),Image.ANTIALIAS)
        #self.lbl_img=ImageTk.PhotoImage(self.lbl_img)
        #self.lbl_img=Label(self.root,image=self.lbl_img).place(x=400,y=180,width=920,height=350)

        #canvas = Canvas(root, width = 600, height =9000)      
        #canvas.pack()      
        #img = PhotoImage(file="login/project.png")      
        #canvas.create_image(20,20, anchor=NW, image=img) 

    def add_course(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=CourseClass(self.new_win)

    def add_student(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=studentClass(self.new_win)

    def add_result(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=resultClass(self.new_win)

    def add_report(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=reportClass(self.new_win)

    def logout(self):
        op=messagebox.askyesno("Confirm","Do you really want to logout?",parent=self.root)
        if op==True:
            cur.execute("DELETE FROM session")
            con.commit()
            self.root.destroy()
            os.system("python register.py")

    def exit(self):
        op=messagebox.askyesno("Confirm","Do you really want to exit?",parent=self.root)
        if op==True:
            self.root.destroy()


if __name__=='__main__':
    root=Tk()
    obj=SMS(root)
    root.mainloop()