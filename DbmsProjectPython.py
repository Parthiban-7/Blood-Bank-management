from tkinter import *
from tkinter import ttk
import tkinter.font as font
from tkinter import messagebox
from PIL import ImageTk,Image

import sqlite3
class DataBase:

    def __init__(self,db):
        self.con=sqlite3.connect(db)
        self.curr=self.con.cursor()
        table1=""" create table if not exists BloodDonor(D_ID integer primary key autoincrement,
        DonorName text,Age int,BloodGroup text,Addr text,Infected text)"""
        self.curr.execute(table1)
        table2= """ create table if not exists BBank(D_ID integer primary key autoincrement,
               BloodGroup text,Addr text)"""
        self.curr.execute(table2)
        table3= """ create table if not exists BloodReceiver(R_ID integer primary key autoincrement,
               DonorName text,Age int,BloodGroup text,Addr text)"""
        self.curr.execute(table3)
        self.con.commit()

    def insertDonor(self,Dname,age,Bgrp,adr,Dis):
        if(str.upper(Dis)=='NO'):
            self.curr.execute("insert into BloodDonor values(null,?,?,?,?,?)",
                              (Dname, age, Bgrp, adr, Dis))
            self.curr.execute("insert into BBank values(null,?,?)",
                              (Bgrp, adr))
            self.con.commit()
            return True
        self.con.commit()
        return False

    def BloodB(self,BGroup,adr):
        self.curr.execute("insert into BBank values(?,?)",
                          (BGroup,adr))
        self.con.commit()

    def insertReceive(self,Rname,age,Bgroup,ad):
        Bgr = str.upper(Bgroup)
        adr = str.upper(ad)
        self.curr.execute("select count(*) from BBank where upper(BloodGroup)=? and upper(Addr)=?",(Bgr,adr))
        cur_result =self.curr.fetchall()
        if(cur_result[0][0]==0):
            self.con.commit()
            return False
        else:
            self.curr.execute("insert into BloodReceiver values(NULL,?,?,?,?)",
                              (Rname,age,Bgroup,ad))
            self.con.commit()
            return cur_result[0][0]

    def fetchdonor(self):
        self.curr.execute("select * from BloodDonor")
        rows1=self.curr.fetchall()
        return rows1

    def fetchBank(self):
        self.curr.execute("select * from BBank")
        rows2= self.curr.fetchall()
        return rows2

    def fetchReciever(self):
        self.curr.execute("select * from BloodReceiver")
        row = self.curr.fetchall()
        return row
    def DelDonor(self,DoId):
        self.curr.execute("select count(*) from BloodDonor where D_ID=?", (DoId))
        cur_result = self.curr.fetchall()
        if (cur_result[0][0] == 1):
            self.curr.execute("Delete from BloodDonor where D_ID=?", (DoId))
            self.curr.execute("Delete from BBank where D_ID=?", (DoId))
            self.con.commit()
            return True
        else:
            self.con.commit()
            return False
    def DelReceiver(self,RoId):
        self.curr.execute("select count(*) from BloodReceiver where R_ID=?", (RoId))
        cur_result = self.curr.fetchall()
        if (cur_result[0][0] == 1):
            self.curr.execute("Delete from BloodReceiver where R_ID=?", (RoId))
            self.con.commit()
            return True
        else:
            self.con.commit()
            return False


def InsertDonor():
    if (Etd1.get() == "" or Etd2.get()=="" or Etd3.get()=="" or Etd4.get()=="" or Etd5.get()==""):
        messagebox.showerror("Error","Please fill all the details")
        return

    res=db.insertDonor(Etd1.get(),Etd2.get(),Etd3.get(),Etd4.get(),Etd5.get())
    if(res==False):
        messagebox.showerror("Error", "Not allowed to Donate Blood")
        return
    messagebox.showinfo(screen1,"Blood Donated")

def BloodDonarDetails():
    global Etd1,Etd2,Etd3,Etd4,screen1,Etd5,imgg
    screen1=Toplevel(root)
    screen1.title("Enter Details")
    screen1.geometry("1920x1080+0+0")
    labl2 = Label(screen1, image=imgg3)
    labl2.place(x=0, y=0, relwidth=1, relheight=1)
    lbs1 = Label(screen1, text="ENTER THE DETAILS", width=600, height=2, background='Black', fg='White',
    font=("Times New Roman", 22, 'bold'))
    lbs1.pack()
    name=StringVar()
    Age=StringVar()
    Bgroup=StringVar()
    Addr=StringVar()
    dis=StringVar()
    lbd1=Label(screen1,text="NAME",background='black',fg='White', font=("Times New Roman",16,'bold'))
    lbd1.place(x="240", y="120")
    Etd1 = Entry(screen1,textvariable=name, width=30,font='Helvetica 13')
    Etd1.place(x="320", y="124", height="24")
    lbd2 = Label(screen1,text="AGE",background='black',fg='White', font=("Times New Roman",16,'bold'))
    lbd2.place(x="680", y="120")
    Etd2 = Entry(screen1,textvariable=Age, width=26,font='Helvetica 13')
    Etd2.place(x="740", y="124", height="24")
    lbd3 = Label(screen1, text="BLOOD GROUP",background='black',fg='White', font=("Times New Roman",16,'bold'))
    lbd3.place(x="512", y="220")
    Etd3 = Entry(screen1, textvariable=Bgroup, width=26,font='Helvetica 13')
    Etd3.place(x="480", y="262", height="24")
    lbd4 = Label(screen1, text="LOCATION",background='black',fg='White', font=("Times New Roman",16,'bold'))
    lbd4.place(x="534", y="310")
    Etd4 = Entry(screen1, textvariable=Addr, width=44,font='Helvetica 13')
    Etd4.place(x="400", y="350", height="40")
    lbd5 = Label(screen1, text="INFECTED",background='black',fg='White', font=("Times New Roman",16,'bold'))
    lbd5.place(x="540", y="410")
    Etd5 = Entry(screen1, textvariable=dis, width=26,font='Helvetica 13')
    Etd5.place(x="480", y="460", height="24")
    btd=Button(screen1,text="SUBMIT",width=12,height=2,bg="#808080",fg="#fdfff5",command=InsertDonor)
    btd.place(x="524", y="530")
    BFont = font.Font(family="Times New Roman", size=14, weight='bold')
    btd['font']=BFont

def InsertReciever():
    if (Etr1.get() == "" or Etr2.get()=="" or Etr3.get()=="" or Etr4.get()==""):
        messagebox.showerror("Error","Please fill all the details")
        return
    r=db.insertReceive(Etr1.get(),Etr2.get(),Etr3.get(),Etr4.get())
    if(r==False):
        messagebox.showinfo(screen2, "Blood Not available")
    else:
        messagebox.showinfo(screen2,f"Blood Request Accepted, No of people with this blood group {r}")


def BloodRequestDetails():
    global Etr1, Etr2, Etr3, Etr4, screen2
    screen2 = Toplevel(root)
    screen2.title("Enter Details")
    screen2.geometry("1920x1080+0+0")
    labl2 = Label(screen2, image=imgg3)
    labl2.place(x=0, y=0, relwidth=1, relheight=1)
    lbs1 = Label(screen2, text="ENTER THE DETAILS", width=600, height=2, background='Black', fg='White',font=("Times New Roman", 22, 'bold'))
    lbs1.pack()
    name = StringVar()
    Age = StringVar()
    Bgroup = StringVar()
    Addr = StringVar()
    lbr1 = Label(screen2, text="NAME",background='black',fg='White', font=("Times New Roman",16,'bold'))
    lbr1.place(x="240", y="120")
    Etr1 = Entry(screen2, textvariable=name, width=26,font='Helvetica 13')
    Etr1.place(x="320", y="124", height="24")
    lbr2 = Label(screen2, text="AGE",background='black',fg='White', font=("Times New Roman",16,'bold'))
    lbr2.place(x="680", y="120")
    Etr2 = Entry(screen2, textvariable=Age, width=26,font='Helvetica 13')
    Etr2.place(x="740", y="125", height="24")
    lbr3 = Label(screen2, text="BLOOD GROUP",background='black',fg='White', font=("Times New Roman",16,'bold'))
    lbr3.place(x="520", y="220")
    Etr3 = Entry(screen2, textvariable=Bgroup, width=26,font='Helvetica 13')
    Etr3.place(x="480", y="262", height="24")
    lbr4 = Label(screen2, text="LOCATION",background='black',fg='White', font=("Times New Roman",16,'bold'))
    lbr4.place(x="545", y="310")
    Etr4 = Entry(screen2, textvariable=Addr, width=46,font='Helvetica 13')
    Etr4.place(x="400", y="350", height="40")
    btd = Button(screen2, text="SUBMIT", width=12, height=2,bg="#808080",fg="#fdfff5",command=InsertReciever)
    btd.place(x="532", y="436")
    BFont = font.Font(family="Times New Roman", size=14, weight='bold')
    btd['font'] = BFont


def DispBloodDonor():
    screen1=Toplevel(root)
    screen1.title("DonorDatabase")
    screen1.geometry("1920x1080+0+0")
    style=ttk.Style()
    style.configure("mystyle.Treeview",font=('Times New Roman',18),rowheight=100)
    style.configure("mystyle.Treeview.Heading", font=('Times New Roman', 18))
    tvt = ttk.Treeview(screen1,columns=(1,2,3,4,5,6),style="mystyle.Treeview")
    treeScroll = ttk.Scrollbar(screen1)
    treeScroll.configure(command=tvt.yview)
    tvt.configure(yscrollcommand=treeScroll.set)
    treeScroll.pack(side=RIGHT, fill=BOTH)
    tvt.pack()
    tvt.heading("1", text="D_ID")
    tvt.heading("2",text="Name")
    tvt.heading("3", text="Age")
    tvt.heading("4", text="BloodGroup")
    tvt.heading("5", text="Location")
    tvt.heading("6",text="Infected")
    for row in db.fetchdonor():
        tvt.insert("",END,values=row)
    tvt['show']='headings'
    tvt.pack(fill=X)

def DispBloodBank():
    screen1 = Toplevel(root)
    screen1.title("Blood Bank Database")
    screen1.geometry("1920x1080+0+0")
    style = ttk.Style()
    style.configure("mystyle.Treeview", font=('Times New Roman', 18),rowheight=100)
    style.configure("mystyle.Treeview.Heading", font=('Times New Roman', 18))
    tvt = ttk.Treeview(screen1, columns=(1,2,3), style="mystyle.Treeview")
    treeScroll = ttk.Scrollbar(screen1)
    treeScroll.configure(command=tvt.yview)
    tvt.configure(yscrollcommand=treeScroll.set)
    treeScroll.pack(side=RIGHT, fill=BOTH)
    tvt.pack()
    tvt.heading("1", text="D_ID")
    tvt.heading("2", text="Blood Group")
    tvt.heading("3", text="Location")
    for row in db.fetchBank():
        tvt.insert("", END, values=row)
    tvt['show'] = 'headings'
    tvt.pack(fill=X)

def DispBloodReciever():
    screen1 = Toplevel(root)
    screen1.title("RecieverDatabase")
    screen1.geometry("1920x1080+0+0")
    style = ttk.Style()
    style.configure("mystyle.Treeview", font=('Times New Roman', 18), rowheight=100)
    style.configure("mystyle.Treeview.Heading", font=('Times New Roman', 18))

    tvt = ttk.Treeview(screen1, columns=(1,2,3,4,5), style="mystyle.Treeview")
    treeScroll = ttk.Scrollbar(screen1)
    treeScroll.configure(command=tvt.yview)
    tvt.configure(yscrollcommand=treeScroll.set)
    treeScroll.pack(side=RIGHT, fill=BOTH)
    tvt.pack()
    tvt.heading("1", text="R_ID")
    tvt.heading("2", text="Name")
    tvt.heading("3", text="Age")
    tvt.heading("4", text="BloodGroup")
    tvt.heading("5", text="Location")
    for row in db.fetchReciever():
        tvt.insert("", END, values=row)
    tvt['show'] = 'headings'
    tvt.pack(fill=X)


def DeleteDdonor():
    if (Et6.get()==""):
        messagebox.showerror("Error","Enter the Donor ID")
        return
    res=db.DelDonor(Et6.get())
    if(res==True):
        messagebox.showinfo(screen1,"Record Deleted")
    else:
        messagebox.showerror("Error", "ID not found")

def DeleteRreceiver():
    if (Et8.get()==""):
        messagebox.showerror("Error","Enter the Receiver ID")
        return
    res=db.DelReceiver(Et8.get())
    if(res==True):
        messagebox.showinfo(screen1,"Record Deleted")
    else:
        messagebox.showerror("Error", "ID not found")

def Admin():
    username_inf=Et1.get()
    password_inf=Et2.get()
    if(username_inf=="Admin" and password_inf=="1234"):
        global Et6,Et8,screen1
        screen1 = Toplevel(root)
        screen1.title("DataBase")
        screen1.geometry("1920x1080+0+0")
        labl2 = Label(screen1, image=imgg3)
        labl2.place(x=0, y=0, relwidth=1, relheight=1)

        D_id =int
        R_id=int

        BFont = font.Font(family="Times New Roman", size=12, weight='bold')
        Btd1 = Button(screen1,text="BLOOD DONOR DETAILS",bg="Black",fg="White", width=23, height=2, command=DispBloodDonor)
        Btd1.place(x="535", y="80")
        Btd1['font']=BFont
        Btd2 = Button(screen1, text="BLOOD BANK DETAILS",bg="Black",fg="White", width=23, height=2, command=DispBloodBank)
        Btd2.place(x="535", y="180")
        Btd2['font'] = BFont
        Btd3 = Button(screen1, text="BLOOD RECEIVER DETAILS",bg="Black",fg="White", width=25, height=2, command=DispBloodReciever)
        Btd3.place(x="530", y="280")
        Btd3['font'] = BFont
        Btd4 = Button(screen1, text="DELETE DONOR", bg="Black", fg="White", width=25, height=2,command=DeleteDdonor)
        Btd4.place(x="300", y="380")
        Btd4['font'] = BFont
        Et6 = Entry(screen1,textvariable=D_id, width=12,font='Helvetica 13')
        Et6.place(x="360", y="450", height="24")
        Btd5 = Button(screen1, text="DELETE RECEIVER", bg="Black", fg="White", width=25, height=2,command=DeleteRreceiver)
        Btd5.place(x="740", y="380")
        Btd5['font'] = BFont
        lbname = Label(screen1,text="DONOR ID", bd=0, background='#FF7377', fg='Black', font=("Times New Roman", 15, 'bold'))
        lbname.place(x="198", y="450")
        Et8= Entry(screen1, textvariable=R_id, width=12,font='Helvetica 13')
        Et8.place(x="810", y="450", height="24")
        lBR = Label(screen1, text="RECEIVER ID", bd=0, background='#FF7377', fg='Black',font=("Times New Roman", 15, 'bold'))
        lBR.place(x="610", y="450")
    else:
        messagebox.showerror("Error","Invalid User")


def main_screen():
    global root,Et1,Et2,imgg3
    root=Tk()
    root.title("Blood Donation Management")
    root.geometry("1920x1080+0+0")
    imgg2=ImageTk.PhotoImage(Image.open(r"C:\Users\mithr\PycharmProjects\pythonProject3\TkinterProject\img1Project.png"))
    mylabel1=Label(root,image=imgg2)
    imgg3 = ImageTk.PhotoImage(Image.open(r"C:\Users\mithr\PycharmProjects\pythonProject3\TkinterProject\img2Project.png"))
    mylabel1.place(x=0,y=0,relwidth=1,relheight=1)
    title=Label(text="BLOOD BANK",width="600",bg='white',height="2",background='Black',fg='White',font=("Times New Roman",36,'bold'))
    title.pack()
    username=StringVar()
    password=StringVar()
    lbname=Label(text="USERNAME",bd=0,background='#FF7377',fg='Black',font=("Times New Roman",17,'bold'))
    lbname.place(x="400",y="256")
    Et1=Entry(textvariable=username,width=26,font='Helvetica 13')
    Et1.place(x="560",y="258",height="24")
    lpass = Label(text="PASSWORD",background='#FF7377',fg='Black', font=("Times New Roman",17,'bold'))
    lpass.place(x="400",y="308")
    Et2=Entry(textvariable=password,width=26,font='Helvetica 13')
    Et2.place(x="560", y="310",height="24")
    BFont = font.Font(family="Times New Roman",size=12,weight='bold')
    Bt1=Button(text="ADMIN LOGIN",bg="#808080",fg="Black",command=Admin,width=13,height=2)
    Bt1.place(x="580",y="360")
    Bt1['font']=BFont
    Bt2= Button(text="BLOOD DONATE",width=15,height=2,bg="#808080",fg="Black",command=BloodDonarDetails)
    Bt2.place(x="480", y="440")
    Bt2['font'] = BFont
    Bt3 = Button(text="BLOOD REQUEST", width=15, height=2,bg="#808080",fg="Black",command=BloodRequestDetails)
    Bt3.place(x="680", y="440")
    Bt3['font'] = BFont
    root.mainloop()
db = DataBase("DataDb.db")
main_screen()

