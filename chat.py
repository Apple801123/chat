from tkinter import *
from tkinter.scrolledtext import ScrolledText
from socket import socket,AF_INET,SOCK_DGRAM
from threading import Thread
from functools import partial
from json import dumps,loads
class Chat(Tk):
    def __init__(self,ip='127.0.0.1',port=35243):
        super().__init__()
        self.des=False
        self.ip=ip
        self.port=port
        self.addr = ("0.0.0.0",35244)
        self.title("Chat ——Sign up")
        self.resizable(False,False)
        self.main = Frame(self)
        self.__signup()
    def __signup(self):
        self.__reload()
        inp = Frame(self.main)
        inp.pack()
        Label(inp,font=("Microsoft yahei",15),text='用户名:').grid(row=0,column=0)
        self.username = Entry(inp,font=("Microsoft Yahei",15),border=0)
        self.username.grid(row=0,column=1)
        Button(self.main,command=self.__chat,text='开始',font=("Microsoft yahei",15),border=0).pack()
    def __reload(self):
        self.main.destroy()
        del self.main
        self.main = Frame(self)
        self.main.pack()
    def __chat(self):
        self.username = self.username.get()
        self.__reload()
        def destroy():
            self.destroy()
            o=socket(AF_INET,SOCK_DGRAM)
            o.sendto(dumps({"type":"logout","user":self.username,"addr":self.addr}))
            self.des=True
            self.recv.join()
        self.protocol("WM_DELETE_WINDOW",destroy)
        o = socket(AF_INET,SOCK_DGRAM)
        o.sendto(dumps({"type":"signup","user":self.username,"addr":self.addr}).encode(),(self.ip,self.port))
        o.close()
        self.messages = ScrolledText(self.main,height=40,width=150,border=0,state='disabled',font=("Microsoft yahei",10))
        self.messages.pack()
        self.__recv_message()
        inp = Frame(self.main)
        inp.pack()
        self.msg =Entry(inp,font=("Microsoft yahei",15),border=0,width=97)
        self.msg.grid(row=0,column=0)
        Button(inp,command=self.__send_message,text="发送",font=("microsoft yahei",9),border=0).grid(row=0,column=1)
    def __recv_message(self):
        def cliend():
            i = socket(AF_INET,SOCK_DGRAM)
            i.bind(self.addr)
            while True:
                if(self.des==True):break
                data,addr = i.recvfrom(2048)
                data = data.decode()
                self.messages.config(state='normal')
                self.messages.insert("end",data+"\n")
                self.messages.config(state='disabled')
                self.messages.see("end")
        self.recv = Thread(target=cliend)
        self.recv.start()
    def __send_message(self):
        message = dumps({"type":"msg","user":self.username,"msg":self.msg.get(),"addr":self.addr})
        self.msg.delete(0,'end')
        o = socket(AF_INET,SOCK_DGRAM)
        o.sendto(message.encode(),(self.ip,self.port))
        o.close()
Chat().mainloop()