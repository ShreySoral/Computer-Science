from tkinter import*
from tkinter import messagebox
from PIL import Image,ImageTk
import time
import os
import mysql.connector
con = mysql.connector.connect(host="localhost",user="root",password="shrey",database="rms")
cur = con.cursor()

cur.execute("SELECT * FROM session order by sno DESC")
authen = cur.fetchone()
if authen != None:
    os.system("python dashboard.py")
    os._exit(0)


class login:
    def __init__(self,root):
        self.root = root
        self.root.title('login window')
        self.root.geometry('1350x700+0+0')
        self.root.config(bg='grey')


        frame=Frame(self.root,bg='crimson')
        frame.place(x=480,y=100,width=700,height=500)
        self.Username = StringVar()
        self.Password = StringVar()
        self.var = StringVar()
        r1 = Radiobutton(frame,variable=self.var, font=('times',25,'bold'),bg='lightyellow', text='Super Admin',value=1)
        r2 = Radiobutton(frame,variable=self.var, font=('times',25,'bold'),bg='lightyellow', text='Junior Admin', value=2)
        self.var.set(1)
        r1.place(x=100,y=30)
        r2.place(x=400,y=30)

        title=Label(frame,text='Login here',font=('times',30,'bold'),justify=CENTER,bg='blue').place(x=50,y=100)
        Username=Label(frame,text='Username',font=('times',20,'bold'),bg='red').place(x=60,y=190)
        Password=Label(frame,text='Password',font=('times',20,'bold'),bg='lightgrey').place(x=60,y=260)

        Username=Entry(frame,textvariable=self.Username,font=('times',25,'bold'),bg='lightyellow').place(x=200,y=190)
        Password=Entry(frame,textvariable=self.Password,font=('times',25,'bold'),bg='lightyellow').place(x=200,y=260)
      

        btn_login=Button(frame,font=('times',25,'bold'),text='Submit',bg='blue',command=self.check,relief=RIDGE).place(x=290,y=330)


    def check(self):
        con=mysql.connector.connect(host='localhost',username='root',password='shrey',database='rms')
        cur=con.cursor()
        try:
            if self.Username.get()=="" or self.Password.get()=="":
                messagebox.showerror("Error","Please Fill All Fields",parent=self.root)
            else:
                if self.var.get()=='1':
                    #cur.execute("select * from login where username=? and password=? and admin='1'",(self.Username.get(),self.Password.get(),))
                    cur.execute("select * from login where username=%s and password=%s and admin='1'",(self.Username.get(),self.Password.get()))
                else:
                    cur.execute("select * from login where username=%s and password=%s and admin='2'",(self.Username.get(),self.Password.get()))
                    #cur.execute("select * from login where username=? and password=? and admin='2'",(self.Username.get(),self.Password.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Invalid username or password",parent=self.root)
                else:
                    #cur.execute("insert into session (time,user,admin) values(?,?,?)",(int(time.time()),self.Username.get(),self.var.get(),))
                    cur.execute("insert into session (time,user,admin)values(%s,%s,%s)",(int(time.time()),self.Username.get(),self.var.get()))
                    con.commit()
                    os.system("python dashboard.py")
                    os._exit(0)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to{str(ex)}")

                    

root=Tk()
obj=login(root)
root.mainloop()