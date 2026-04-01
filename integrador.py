from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import json
import os

class SistemaInventario:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Gestión de Inventario")
        self.root.geometry("1000x500")
        self.root.minsize(800, 400)

        self.archivo_datos = "inventario.json"
        self.datos = self.cargar_datos()

        self.var_codigo = StringVar()
        self.var_nombre = StringVar()
        self.var_precio = DoubleVar(value=0.0)
        self.var_categoria = StringVar()
        self.var_cantidad = IntVar(value=0)
        self.var_busqueda = StringVar()

        self.orden_reverso = False

        self.crear_interfaz()
        self.refrescar_tabla()

        self.var_busqueda.trace_add("write", self.filtrar_busqueda)

    def crear_interfaz(self):
        frame_top = Frame(self.root, padx=10, pady=5)
        frame_top.pack(side=TOP, fill=X)
        Label(frame_top, text="Buscar por Nombre:").pack(side=LEFT)
        ttk.Entry(frame_top, textvariable=self.var_busqueda, width=40).pack(side=LEFT, padx=10)

        panel_izq = ttk.LabelFrame(self.root, text="Panel de Operaciones", padding=(10, 10))
        panel_izq.pack(side=LEFT, fill=Y, padx=10, pady=10)

        ttk.Label(panel_izq, text="Nombre:").grid(row=0, column=0, sticky=W, pady=5)
        ttk.Entry(panel_izq, textvariable=self.var_codigo).grid(row=0, column=1, pady=5)

        ttk.Label(panel_izq, text="Descripción:").grid(row=1, column=0, sticky=W, pady=5)
        ttk.Entry(panel_izq, textvariable=self.var_nombre).grid(row=1, column=1, pady=5)

        ttk.Label(panel_izq, text="Precio:").grid(row=2, column=0, sticky=W, pady=5)
        ttk.Entry(panel_izq, textvariable=self.var_precio).grid(row=2, column=1, pady=5)

        ttk.Label(panel_izq, text="Categoría:").grid(row=3, column=0, sticky=W, pady=5)
        ttk.Entry(panel_izq, textvariable=self.var_categoria).grid(row=3, column=1, pady=5)

        ttk.Label(panel_izq, text="Cantidad en Stock:").grid(row=4, column=0, sticky=W, pady=5)
        ttk.Spinbox(panel_izq, from_=0, to=10000, textvariable=self.var_cantidad, width=18).grid(row=4, column=1, pady=5)

        frame_botones = Frame(panel_izq)
        frame_botones.grid(row=5, column=0, columnspan=2, pady=20)
        
        ttk.Button(frame_botones, text="Guardar", command=self.guardar_registro).grid(row=0, column=0, padx=5)
        ttk.Button(frame_botones, text="Modificar", command=self.modificar_registro).grid(row=0, column=1, padx=5)
        ttk.Button(frame_botones, text="Borrar", command=self.borrar_registro).grid(row=0, column=2, padx=5)
        ttk.Button(frame_botones, text="Limpiar Form", command=self.limpiar_formulario).grid(row=1, column=0, columnspan=3, pady=10, sticky=EW)

        panel_der = ttk.LabelFrame(self.root, text="Base de Datos del Inventario", padding=(10, 10))
        panel_der.pack(side=RIGHT, fill=BOTH, expand=True, padx=10, pady=10)

        columnas = ("codigo", "nombre", "precio", "categoria", "cantidad")
        self.tree = ttk.Treeview(panel_der, columns=columnas, show="headings", selectmode="browse")
        
        scrollbar_y = ttk.Scrollbar(panel_der, orient=VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar_y.set)

        scrollbar_y.pack(side=RIGHT, fill=Y)
        self.tree.pack(side=LEFT, fill=BOTH, expand=True)

        encabezados = {"codigo": "Código", "nombre": "Descripción", "precio": "Precio", "categoria": "Categoría", "cantidad": "Stock"}
        for col in columnas:
            self.tree.heading(col, text=encabezados[col], command=lambda c=col: self.ordenar_por_columna(c))
            self.tree.column(col, width=100, anchor=CENTER)

        self.tree.tag_configure("stock_bajo", background="#ffcccc")

        self.tree.bind("<ButtonRelease-1>", self.seleccionar_registro)

    def refrescar_tabla(self, datos_mostrar=None):
        if datos_mostrar is None:
            datos_mostrar = self.datos

        for fila in self.tree.get_children():
            self.tree.delete(fila)

        for item in datos_mostrar:
            tags = ("stock_bajo",) if item["cantidad"] < 5 else ()
            valores = (item["codigo"], item["nombre"], item["precio"], item["categoria"], item["cantidad"])
            self.tree.insert("", END, values=valores, tags=tags)

    def guardar_registro(self):
        cod = self.var_codigo.get().strip()
        nom = self.var_nombre.get().strip()
        cat = self.var_categoria.get().strip()
        
        try:
            pre = float(self.var_precio.get())
            can = int(self.var_cantidad.get())
        except ValueError:
            messagebox.showerror("Error", "Precio y Cantidad deben ser numéricos.")
            return

        if not all([cod, nom, cat]):
            messagebox.showwarning("Advertencia", "Todos los campos de texto son obligatorios.")
            return

        for item in self.datos:
            if item["codigo"] == cod:
                messagebox.showerror("Error", f"El código '{cod}' ya existe.")
                return

        nuevo_producto = {
            "codigo": cod, "nombre": nom, "precio": pre, 
            "categoria": cat, "cantidad": can
        }
        self.datos.append(nuevo_producto)
        
        self.guardar_datos_disco()
        self.refrescar_tabla()
        self.limpiar_formulario()
        messagebox.showinfo("Éxito", "Producto guardado correctamente.")

    def seleccionar_registro(self, event):
        seleccion = self.tree.focus()
        if not seleccion: return
        
        valores = self.tree.item(seleccion, "values")
        if valores:
            self.var_codigo.set(valores[0])
            self.var_nombre.set(valores[1])
            self.var_precio.set(float(valores[2]))
            self.var_categoria.set(valores[3])
            self.var_cantidad.set(int(valores[4]))

    def modificar_registro(self):
        cod = self.var_codigo.get().strip()
        if not cod:
            messagebox.showwarning("Advertencia", "Seleccione un producto para modificar.")
            return

        try:
            pre = float(self.var_precio.get())
            can = int(self.var_cantidad.get())
        except ValueError:
            messagebox.showerror("Error", "Precio y Cantidad deben ser numéricos.")
            return

        actualizado = False
        for item in self.datos:
            if item["codigo"] == cod:
                item["nombre"] = self.var_nombre.get().strip()
                item["precio"] = pre
                item["categoria"] = self.var_categoria.get().strip()
                item["cantidad"] = can
                actualizado = True
                break

        if actualizado:
            self.guardar_datos_disco()
            self.refrescar_tabla()
            self.limpiar_formulario()
            messagebox.showinfo("Éxito", "Producto modificado.")
        else:
            messagebox.showerror("Error", "Producto no encontrado.")

    def borrar_registro(self):
        cod = self.var_codigo.get().strip()
        if not cod:
            messagebox.showwarning("Advertencia", "Seleccione un producto para borrar.")
            return

        respuesta = messagebox.askyesno("Confirmar", f"¿Borrar el producto '{cod}'?")
        if not respuesta: return

        for i in range(len(self.datos)):
            if self.datos[i]["codigo"] == cod:
                del self.datos[i]
                break
        
        self.guardar_datos_disco()
        self.refrescar_tabla()
        self.limpiar_formulario()
        messagebox.showinfo("Éxito", "Producto eliminado.")

    def limpiar_formulario(self):
        self.var_codigo.set("")
        self.var_nombre.set("")
        self.var_precio.set(0.0)
        self.var_categoria.set("")
        self.var_cantidad.set(0)

    def filtrar_busqueda(self, *args):
        termino = self.var_busqueda.get().lower()
        if termino == "":
            self.refrescar_tabla(self.datos)
            return
        
        sub_lista = [
            item for item in self.datos 
            if termino in item["nombre"].lower() or termino in item["codigo"].lower()
        ]
        self.refrescar_tabla(sub_lista)

    def ordenar_por_columna(self, col):
        es_numerico = col in ["precio", "cantidad"]
        self.datos.sort(
            key=lambda x: float(x[col]) if es_numerico else x[col].lower(),
            reverse=self.orden_reverso
        )
        self.orden_reverso = not self.orden_reverso
        self.refrescar_tabla()

    def cargar_datos(self):
        if os.path.exists(self.archivo_datos):
            try:
                with open(self.archivo_datos, "r", encoding="utf-8") as archivo:
                    return json.load(archivo)
            except json.JSONDecodeError:
                messagebox.showerror("Error", "El archivo JSON está corrupto. Se iniciará vacío.")
                return []
        return []

    def guardar_datos_disco(self):
        with open(self.archivo_datos, "w", encoding="utf-8") as archivo:
            json.dump(self.datos, archivo, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    root = Tk()  
    app = SistemaInventario(root)
    root.mainloop()