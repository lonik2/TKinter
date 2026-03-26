from tkinter import *
from tkinter import ttk

root = Tk()

def suma():
    try:    
        valor1 = float(entry1.get())
        valor2 = float(entry2.get())
        resultado.config(text=str(valor1+valor2))
    except:
        resultado.config(text = "solo se permiten numeros")

def resta():
    try:
        valor1 = float(entry1.get())
        valor2 = float(entry2.get())
        resultado.config(text=str(valor1-valor2))
    except:
        resultado.config(text = "solo se permiten numeros")

def multiplicacion():
    try:
        valor1 = float(entry1.get())
        valor2 = float(entry2.get())
        resultado.config(text=str(valor1*valor2))
    except:
        resultado.config(text = "solo se permiten numeros")

def division():
    try:
        valor1 = float(entry1.get())
        valor2 = float(entry2.get())
        resultado.config(text=str(valor1/valor2))
    except:
        resultado.config(text = "solo se permiten numeros")

def potencia():
    try:
        valor1 = float(entry1.get())
        valor2 = float(entry2.get())
        resultado.config(text=str(valor1**valor2))
    except:
        resultado.config(text = "solo se permiten numeros")

def raiz():
    try:
        valor1 = float(entry1.get())
        valor2 = float(entry2.get())
        resultado.config(text=str(valor1**(1/valor2)))
    except:
        resultado.config(text = "solo se permiten numeros")

entry1 = Entry(root)
entry1.pack()

entry2 = Entry(root)
entry2.pack()

boton = Button(root, text="+", command=suma)
boton.pack()

boton = Button(root, text="-", command=resta)
boton.pack()

boton = Button(root, text="*", command=multiplicacion)
boton.pack()

boton = Button(root, text="/", command=division)
boton.pack()

boton = Button(root, text="**", command=potencia)
boton.pack()

boton = Button(root, text="√", command=raiz)
boton.pack()

resultado = Label(root, text="")
resultado.pack()

root.mainloop()