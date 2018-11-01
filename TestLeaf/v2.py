from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfilename
from tkinter import Tk,Entry,Button,INSERT
from tkinter import messagebox
import base64
import pyDes
from Cryptodome.Cipher import DES3
import os

root =Tk()
root.geometry("900x400")

root.iconbitmap('lock.ico')
root.title("LBS Encrypt & Decryp0t")
root.resizable(width=False, height=False)
#root.config(bg='blue')
image = tk.PhotoImage(file="bgda.gif")
w = image.width()
h = image.height()
panel = tk.Label(root, image=image)
panel.pack(side='bottom', fill='both', expand='yes')


def encrypt_3des(clear_text):
    
        key="Laserbeam-Compass"
        clear_text_byte = clear_text.encode('utf-8')
        key_byte = key.encode('utf-8')
        key_byte = key_byte.ljust(24, "\0".encode('utf-8'))
        if len(key_byte) > 24:
            key_byte = key_byte[:24]

        k = pyDes.triple_des(key_byte, pyDes.ECB, IV = None, pad = None, padmode = pyDes.PAD_PKCS5)
        d = k.encrypt(clear_text_byte)

        return base64.b64encode(d).decode('utf-8')
def decrypt_3des(data):
    key="Laserbeam-Compass"
    data_byte = base64.b64decode(data.encode('utf-8'))
    key_byte = key.encode('utf-8')
    key_byte = key_byte.ljust(24, "\0".encode('utf-8'))
    if len(key_byte) > 24:
        key_byte = key_byte[:24]

    cryptor = DES3.new(key_byte, DES3.MODE_ECB)
    c_text = cryptor.decrypt(data_byte)

    
    pad_len = ord(c_text.decode('utf-8')[-1])
    clear_text = c_text.decode('utf-8')[:-pad_len]

    return clear_text




def fun():
    global w
    s=w.get()
    if(s==''):
        messagebox.showerror("Error", "Plese Enter the Text to Encrypt")
    else:
        def clear():
                w.delete(0,END)
                ent.destroy()
                button3.destroy()
                
                
            
                
        en=encrypt_3des(s)

        ent = Entry(root, state='readonly', readonlybackground='white', fg='red')
        var = StringVar()
        var.set(en)
        ent.config(textvariable=var, relief='flat')
        ent.place(x=200,y=75,height=32,width=500)
        #label = Label(text=en,foreground="red",font=("Corbel", 16))
        #label.place(x=200,y=75,height=32,width=500)
        button3=Button(padx = 5, pady = 5, text="clear",font=("Cooper Black",16),relief=RAISED,foreground='red',command=clear)
        button3.place(x=500,y=115)


    



def fun2():
    global w1
    s=w1.get()
    
    if(s==''):
        messagebox.showerror("Error", "Plese Enter the Text to Decrypt")
    else:
        def clear():
                w1.delete(0,END)
                ent1.destroy()
                button4.destroy()
                
        
        dc=decrypt_3des(s)
        ent1 = Entry(root, state='readonly', readonlybackground='white', fg='green')
        var = StringVar()
        var.set(dc)     
        ent1.config(textvariable=var, relief='flat')
        ent1.place(x=200,y=220,height=32,width=500)
        
        button4=Button(padx = 5, pady = 5, text="clear",font=("Cooper Black",16),relief=RAISED,foreground='red',command=clear)
        button4.place(x=500,y=265)

        
        #labe2 = Label(text=en,foreground="red",font=("Cooper Black", 16))
        #labe2.place(x=200,y=220,height=32,width=500)

label = Label(text="Text to Encrypt",foreground="RED",font=("Cooper Black", 16))
label.place(x=15,y=35)

svalue = StringVar()
w = Entry(root,textvariable=svalue,foreground='GREEN',font=("Corbel", 14))
w.place(x=200,y=35,height=32,width=500)

        

button=Button(padx = 5, pady = 5, text="Encrypt",font=("Cooper Black",14),relief=RAISED,foreground='red',command=fun)
button.place(x=200,y=115)


label1 = Label(text="Text to Decrypt",foreground="green",font=("Cooper Black", 16))
label1.place(x=15,y=170)

svalue1 = StringVar()
w1 = Entry(root,textvariable=svalue1,font=("Corbel", 12),foreground='red')
w1.place(x=200,y=170,height=32,width=500)

#labe2 = Label(text='',foreground="red",font=("Cooper Black", 16))
#labe2.place(x=200,y=220,height=32,width=500)


button1=Button(padx = 5, pady = 5, text="Decrypt",font=("Cooper Black",14),relief=RAISED,foreground='green',command=fun2)
button1.place(x=200,y=265)


root.mainloop()
