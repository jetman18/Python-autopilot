from tkinter import *
import os,signal
from multiprocessing import Process
import multiprocessing as mp
import time
import struct
class window():
    root = Tk()
    root.title('view')
    root.geometry("600x400")
    canva = Canvas(root,width=200,height=200,bg='black')
    canva.place(x=0,y=200)

    #roll
    label1=Label(root, text='Roll:', font=('Helvetica 10'))
    label1.place(x=10,y=10)
    label11=Label(root, text='0', font=('Helvetica 10'))
    label11.place(x=50,y=10)
    #pitch
    label2=Label(root, text='Pitch:', font=('Helvetica 10'))
    label2.place(x=10,y=30)
    label22=Label(root, text='0', font=('Helvetica 10'))
    label22.place(x=50,y=30)
    #yaw
    label3=Label(root, text='Yaw:', font=('Helvetica 10'))
    label3.place(x=10,y=50)
    label33=Label(root, text='0', font=('Helvetica 10'))
    label33.place(x=50,y=50)
    #altitude
    label4=Label(root, text='Alt:', font=('Helvetica 10'))
    label4.place(x=10,y=75)
    label44=Label(root, text='0', font=('Helvetica 10'))
    label44.place(x=50,y=75)
    #lat
    label5=Label(root, text='Lat:', font=('Helvetica 10'))
    label5.place(x=10,y=95)
    label55=Label(root, text='0', font=('Helvetica 10'))
    label55.place(x=50,y=95)
    #lon
    label6=Label(root, text='Lon:', font=('Helvetica 10'))
    label6.place(x=10,y=115)
    label66=Label(root, text='0', font=('Helvetica 10'))
    label66.place(x=50,y=115)
    #yaw dot
    label7=Label(root, text='yaw_dot:', font=('Helvetica 10'))
    label7.place(x=10,y=140)
    label77=Label(root, text='0', font=('Helvetica 10'))
    label77.place(x=50,y=140)

    thrust_text=Label(root, text='thrust', font=('Helvetica 10'))
    thrust_text.place(x=400,y=50)
    ww = Scale(root, from_=-9, to=9,resolution=0.1,length=100)
    ww.place(x=400,y=100)

    roll_in = StringVar(root)  
    pitch_in = StringVar(root)
    yaw_in = StringVar(root)
    tt = 0
    def update_log(self):
        window.tt +=10
        if(window.tt>200):
            window.tt=0
        window.canva.create_text(20,window.tt, text=str(window.tt), fill="white", font=('Helvetica 7'))
    #pipe
    def __init__(self,pipe) -> None:
        self.roll =0 
        self.att = []
        self.last_t = time.time()
        self.p1,self.p2 = mp.Pipe()
        self.pp1,self.pp2 = mp.Pipe()
        self.run = 1
        p = Process(target=self.show,args=(pipe,))
        p.start()
    def bt_cback(self):
        window.label11.configure(text=str())
        #pipe.send('hello')
        #print(self.roll)
    def setAttitude(self,roll,pitch,yaw,alt,lat,lon,yaw_dot):
        if time.time() - self.last_t > 0.4:
            self.last_t = time.time()
            da = struct.pack('iiiiddi',roll,pitch,yaw,alt,lat,lon,int(yaw_dot))
            self.p2.send(da)
       
    def update_sc(self):
        if self.p1.poll():
            data = self.p1.recv()
            data = struct.unpack('iiiiddi',data)
            window.label11.configure(text=str(data[0]))
            window.label22.configure(text=str(data[1]))
            window.label33.configure(text=str(data[2]))
            window.label44.configure(text=str(data[3]))
            window.label55.configure(text=str(data[4]))
            window.label66.configure(text=str(data[5]))
            window.label77.configure(text=str(data[6]))
        #print(window.ww.get())
        window.root.after(100,self.update_sc)

    def setAtitud(self,pipe):
        roll = 0
        pitch = 0
        yaw = 0
        try:
            roll = float(window.roll_in.get())
            pitch =float(window.pitch_in.get())
            yaw = float(window.yaw_in.get())
        except:
            roll = 0
            pitch =0
            yaw = 0
        data = struct.pack('ddd',roll,pitch,yaw)
        pipe.send(data)
    def resetAtitud(self,pipe):
        data = struct.pack('ddd',0.0,0.0,0.0)
        pipe.send(data)


    def show(self,pipe):
        roll = Entry(window.root, textvariable=window.roll_in)
        roll.place(width=50,height=17)
        roll.place(x=100,y=13)
        pitch = Entry(window.root, textvariable=window.pitch_in)
        pitch.place(width=50,height=17)
        pitch.place(x=100,y=33)
        yaw = Entry(window.root, textvariable=window.yaw_in)
        yaw.place(width=50,height=17)
        yaw.place(x=100,y=53)
        # button
        B = Button(padx=20,pady=2, text ="set", command = lambda: self.setAtitud(pipe))
        B.place(x=170,y=13)
        RB = Button(padx=20,pady=2, text ="reset", command = lambda: self.resetAtitud(pipe))
        RB.place(x=240,y=13)
        connect = Button(padx=20,pady=2, text ="circle", command = self.update_log)
        connect.place(x=240,y=103)
    
        window.root.after(100,self.update_sc)
        window.root.mainloop()
        self.pp1.send('close')
    def isRun(self):
        if self.run:
            if self.pp2.poll():
                rec = self.pp2.recv()
                if rec == 'close':
                    self.run = 0
            else:
                return 1
        return self.run



