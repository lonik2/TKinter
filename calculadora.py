from tkinter import *
from tkinter import ttk

root = Tk()
root.title("Calculadora")
root.geometry("300x400")
root.configure(bg="#2C2F33")

style = ttk.Style()
style.configure("TButton", font=("Arial", 12), padding=10)
style.configure("TLabel", font=("Arial", 14), background="#2C2F33", foreground="white")

def obtener_valores():
    try:
        return float(entry1.get()), float(entry2.get())
    except:
        resultado.config(text="⚠ Solo números")
        return None, None

def suma():
    v1, v2 = obtener_valores()
    if v1 is not None:
        resultado.config(text=str(v1 + v2))

def resta():
    v1, v2 = obtener_valores()
    if v1 is not None:
        resultado.config(text=str(v1 - v2))

def multiplicacion():
    v1, v2 = obtener_valores()
    if v1 is not None:
        resultado.config(text=str(v1 * v2))

def division():
    v1, v2 = obtener_valores()
    if v1 is not None:
        try:
            resultado.config(text=str(v1 / v2))
        except:
            resultado.config(text="❌ Error")

def potencia():
    v1, v2 = obtener_valores()
    if v1 is not None:
        resultado.config(text=str(v1 ** v2))

def raiz():
    v1, v2 = obtener_valores()
    if v1 is not None:
        resultado.config(text=str(v1 ** (1 / v2)))

entry1 = Entry(root, font=("Arial", 14), justify="center")
entry1.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

entry2 = Entry(root, font=("Arial", 14), justify="center")
entry2.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

ttk.Button(root, text="+", command=suma).grid(row=2, column=0, padx=10, pady=5, sticky="ew")
ttk.Button(root, text="-", command=resta).grid(row=2, column=1, padx=10, pady=5, sticky="ew")

ttk.Button(root, text="×", command=multiplicacion).grid(row=3, column=0, padx=10, pady=5, sticky="ew")
ttk.Button(root, text="÷", command=division).grid(row=3, column=1, padx=10, pady=5, sticky="ew")

ttk.Button(root, text="xʸ", command=potencia).grid(row=4, column=0, padx=10, pady=5, sticky="ew")
ttk.Button(root, text="√", command=raiz).grid(row=4, column=1, padx=10, pady=5, sticky="ew")

resultado = ttk.Label(root, text="Resultado", anchor="center")
resultado.grid(row=5, column=0, columnspan=2, pady=20)

root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)

root.mainloop()