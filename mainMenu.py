import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as mb
from tkinter import scrolledtext as st
import personasSancionadas

class mainMenu:
    def __init__(self):
        self.articulo1=personasSancionadas.personasSancionadas()
        self.ventana1=tk.Tk()
        self.ventana1.title("Listas de Control onu -- ofac")
        self.cuaderno1 = ttk.Notebook(self.ventana1)        
        self.consulta_por_codigo()
        self.listado_completo()
        self.cuaderno1.grid(column=0, row=0, padx=100, pady=100)
        self.ventana1.mainloop()

    def consulta_por_codigo(self):
        self.pagina2 = ttk.Frame(self.cuaderno1)
        self.cuaderno1.add(self.pagina2, text="Consulta por Nombre")
        self.labelframe1=ttk.LabelFrame(self.pagina2, text="Persona Sancionada:")
        self.labelframe1.grid(column=0, row=0, padx=5, pady=10)
        self.label1=ttk.Label(self.labelframe1, text="Identificacion:")
        self.codigo=tk.StringVar()
        self.entrycodigo=ttk.Entry(self.labelframe1, textvariable=self.codigo)
        self.entrycodigo.grid(column=1, row=0, padx=4, pady=4)
        self.label1.grid(column=0, row=0, padx=4, pady=4)
        self.boton1=ttk.Button(self.labelframe1, text="Consultar", command=self.consultar)
        self.boton1.grid(column=1, row=3, padx=4, pady=4)

    def consultar(self):
        datos=(self.codigo.get(), )
        print(datos)
        respuesta=self.articulo1.personByIdentification(datos)
        if respuesta:
            print("Fila seleccionada:", respuesta)
            # Crear una ventana
            ventana_resultado = tk.Toplevel()
            ventana_resultado.title("Resultados de la consulta")

            # Crear un Treeview en la ventana
            self.tree_resultado = ttk.Treeview(ventana_resultado, columns=("ID", "First Name", "Last Name"))
            self.tree_resultado.heading("ID", text="ID")
            self.tree_resultado.heading("First Name", text="First Name")
            self.tree_resultado.heading("Last Name", text="Last Name")
            self.tree_resultado.grid(row=0, column=0, sticky="nsew")

            # Agregar datos al Treeview
            if respuesta:
                self.tree_resultado.insert("", "end", values=respuesta)
            self.tree_resultado.bind("<Double-1>", self.on_treeview_click_consulta)
            # Configurar el Scrollbar
            scroll_resultado = ttk.Scrollbar(ventana_resultado, orient="vertical", command=self.tree_resultado.yview)
            scroll_resultado.grid(row=0, column=1, sticky="ns")
            self.tree_resultado.configure(yscrollcommand=scroll_resultado.set)
        else:
            mb.showinfo("Información", "No esite")

    def on_treeview_click_consulta(self, event):
        item = self.tree_resultado.selection()[0]
        fila_seleccionada = self.tree_resultado.item(item, "values")
        print("Fila seleccionada:", fila_seleccionada)
        ventana_detalle = tk.Toplevel()
        ventana_detalle.title("Detalles de Fila")
        identifications=self.articulo1.identificacionesPersona(fila_seleccionada[0])
        print(identifications)
        self.mostrarIdentifications(identifications,ventana_detalle)

    def listado_completo(self):
        self.pagina3 = ttk.Frame(self.cuaderno1)
        self.cuaderno1.add(self.pagina3, text="Listado completo")

        self.tree = ttk.Treeview(self.pagina3, columns=("ID", "First Name", "Last Name"))
        self.tree.heading("ID", text="ID")
        self.tree.heading("First Name", text="First Name")
        self.tree.heading("Last Name", text="Last Name")
        self.tree.grid(row=0, column=0, sticky="nsew")

        self.scroll = ttk.Scrollbar(self.pagina3, orient="vertical", command=self.tree.yview)
        self.scroll.grid(row=0, column=1, sticky="ns")
        self.tree.configure(yscrollcommand=self.scroll.set)

        self.boton1 = ttk.Button(self.pagina3, text="Obtener Todos", command=self.listar)
        self.boton1.grid(row=1, column=0, padx=4, pady=4)

    def listar(self):
        respuesta=self.articulo1.recuperar_todos()
        # Limpiar la tabla antes de insertar nuevos datos
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Insertar datos en la tabla
        for index, fila in enumerate(respuesta, start=1):
            self.tree.insert("", "end", values=fila)

        self.tree.bind("<Double-1>", self.on_treeview_click)

    def on_treeview_click(self, event):
        item = self.tree.selection()[0]
        fila_seleccionada = self.tree.item(item, "values")
        print("Fila seleccionada:", fila_seleccionada)
        ventana_detalle = tk.Toplevel()
        ventana_detalle.title("Detalles de Fila")
        identifications=self.articulo1.identificacionesPersona(fila_seleccionada[0])
        print(identifications)
        self.mostrarIdentifications(identifications,ventana_detalle)

    def mostrarIdentifications(self,identifications,ventana):

        tree = ttk.Treeview(ventana)
        if(len(identifications)<=0):
            texto = tk.Text(ventana)
            texto.pack()
            texto.insert(tk.END, "No hay identificaciones.")
        else:
            tree["columns"] = ( "Columna1", "Columna2", "Columna3")  # Puedes agregar más columnas según sea necesario
            tree.heading("#0", text="Índice")
            tree.heading("Columna1", text="Tipo Documento")
            tree.heading("Columna2", text="Documento")
            tree.heading("Columna3", text="Pais")

            for index, identificacion in enumerate(identifications, start=1):
                tree.insert("", "end", text=str(index), values=[identificacion[1],identificacion[2],identificacion[3]])
            tree.pack(expand=True, fill="both")

def abrir_ventana_principal():
    ventana_principal = mainMenu()

if __name__ == "__main__":
    abrir_ventana_principal()