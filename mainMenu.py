import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as mb
from tkinter import scrolledtext as st
import personasSancionadas

class mainMenu:
    def __init__(self):
        self.sanctionActions=personasSancionadas.personasSancionadas()
        self.ventana1=tk.Tk()
        self.ventana1.title("Listas de Control ONU/OFAC")
        self.cuaderno1 = ttk.Notebook(self.ventana1)    
        self.listado_completo()  
        self.consulta_por_codigo()
        self.cuaderno1.grid(column=0, row=0, padx=50, pady=50)
        self.ventana1.mainloop()

    def consulta_por_codigo(self):
        pagina2 = ttk.Frame(self.cuaderno1)
        self.cuaderno1.add(pagina2, text="Consulta por ID")
        self.labelframe1=ttk.LabelFrame(pagina2, text="Persona Sancionada:")
        self.labelframe1.grid(column=0, row=0, padx=5, pady=10)
        self.label1=ttk.Label(self.labelframe1, text="Identificacion:")
        self.codigo=tk.StringVar()
        self.entrycodigo=ttk.Entry(self.labelframe1, textvariable=self.codigo)
        self.entrycodigo.grid(column=1, row=0, padx=4, pady=4)
        self.label1.grid(column=0, row=0, padx=4, pady=4)
        self.boton1=ttk.Button(self.labelframe1, text="Consultar por ID", command=lambda: self.consultar("ID"))
        self.boton1.grid(column=1, row=3, padx=4, pady=4)

        # Pestaña de consulta por Nombre
        pagina3 = ttk.Frame(self.cuaderno1)
        self.cuaderno1.add(pagina3, text="Consulta por Nombre")
        self.labelframe2 = ttk.LabelFrame(pagina3, text="Persona Sancionada:")
        self.labelframe2.grid(column=0, row=0, padx=5, pady=10)
        self.label2 = ttk.Label(self.labelframe2, text="Nombre:")
        self.codigo_nombre = tk.StringVar()
        self.entrynombre = ttk.Entry(self.labelframe2, textvariable=self.codigo_nombre)
        self.entrynombre.grid(column=1, row=0, padx=4, pady=4)
        self.label2.grid(column=0, row=0, padx=4, pady=4)
        self.boton2 = ttk.Button(self.labelframe2, text="Consultar por Nombre", command=lambda: self.consultar("NOMBRE"))
        self.boton2.grid(column=1, row=3, padx=4, pady=4)

        pagina4 = ttk.Frame(self.cuaderno1)
        self.cuaderno1.add(pagina4, text="Actualizar")
        self.labelframe3 = ttk.LabelFrame(pagina4, text="Actualizar las listas de control:")
        self.labelframe3.grid(column=0, row=0, padx=5, pady=10)
        self.label3 = ttk.Label(self.labelframe3, text="Vuelve a recibir los datos conforme a la ultima actualizacion de la onu/ofac")
        self.label3.grid(column=0, row=0, padx=4, pady=4)
        self.boton3 = ttk.Button(self.labelframe3, text="Actualizar", command=lambda: self.sanctionActions.updateControlLists())
        self.boton3.grid(column=1, row=3, padx=4, pady=4)

    def consultar(self,type):
        if(type=="ID"):
            datos=(self.codigo.get(), )
            respuesta=self.sanctionActions.personLikeIdentification(datos)
        else:
            datos=(self.codigo_nombre.get(), )
            respuesta=self.sanctionActions.personLikeName(datos)
        
        #print('JSJSJS=>',self.sanctionActions.personLikeIdentification(datos))
        if respuesta:
            #print("Fila seleccionada:", respuesta)
            # Crear una ventana
            ventana_resultado = tk.Toplevel()
            ventana_resultado.geometry("1000x400") 
            ventana_resultado.title("Resultados de la consulta")
            anchos_columnas = {
                "#0":0,
                "ID": 30,
                "Identification": 200,
                "First Name": 200,
                "Last Name": 300,
                "Type Control": 150
            }
            self.tree_resultado = ttk.Treeview(ventana_resultado, columns=("ID","Identification", "First Name", "Last Name", "Type Control"))
            self.tree_resultado.config(height=15)
            self.tree_resultado.heading("ID", text="ID")
            self.tree_resultado.heading("Identification", text="Identification")
            self.tree_resultado.heading("First Name", text="First Name")
            self.tree_resultado.heading("Last Name", text="Last Name")
            self.tree_resultado.heading("Type Control", text="Type Control")
            self.tree_resultado.grid(row=0, column=0, sticky="nsew")

            for col, ancho in anchos_columnas.items():
                self.tree_resultado.column(col, width=ancho)
            self.tree_resultado.pack(fill="both", expand=True)
            if respuesta:
                for index, fila in enumerate(respuesta, start=1):
                    self.tree_resultado.insert("", "end", values=fila)

            self.tree_resultado.bind("<Double-1>", lambda event: self.on_treeview_click(self.tree_resultado))
            scroll_resultado = ttk.Scrollbar(ventana_resultado, orient="vertical", command=self.tree_resultado.yview)
            #scroll_resultado.grid(row=0, column=1, sticky="ns")
            self.tree_resultado.configure(yscrollcommand=scroll_resultado.set)
        else:
            mb.showinfo("Información", "No esite")

    def listado_completo(self):
        self.pagina3 = ttk.Frame(self.cuaderno1)
        self.cuaderno1.add(self.pagina3, text="Listado completo")

        anchos_columnas = {
                "#0":0,
                "ID": 40,
                "First Name": 200,
                "Last Name": 300,
                "Type Control": 200
            }
        self.tree = ttk.Treeview(self.pagina3, columns=("ID", "First Name", "Last Name","Type Control"))
        self.tree.heading("ID", text="ID")
        self.tree.heading("First Name", text="First Name")
        self.tree.heading("Last Name", text="Last Name")
        self.tree.heading("Type Control", text="Type Control")
        self.tree.grid(row=0, column=0, sticky="nsew")

        for col, ancho in anchos_columnas.items():
            self.tree.column(col, width=ancho)

        self.scroll = ttk.Scrollbar(self.pagina3, orient="vertical", command=self.tree.yview)
        self.scroll.grid(row=0, column=1, sticky="ns")
        self.tree.configure(yscrollcommand=self.scroll.set)

        self.boton1 = ttk.Button(self.pagina3, text="Obtener Todos", command=self.listar)
        self.boton1.grid(row=1, column=0, padx=4, pady=4)
        
    def listar(self):
        respuesta=self.sanctionActions.recuperar_todos()
        for row in self.tree.get_children():
            self.tree.delete(row)

        for index, fila in enumerate(respuesta, start=1):
            self.tree.insert("", "end", values=fila)
            self.tree.grid(row=0, column=0, sticky="nsew")

        self.tree.bind("<Double-1>", lambda event: self.on_treeview_click(self.tree))

    def on_treeview_click(self, selectedTree):
        item = selectedTree.selection()[0]
        fila_seleccionada = selectedTree.item(item, "values")
        print("Fila seleccionada:", fila_seleccionada)
        identifications=self.sanctionActions.identificacionesPersona(fila_seleccionada[0])
        if(len(identifications)<=0):
            mb.showinfo("Información", "No tiene Identificaciones")
        else:
            ventana_detalle = tk.Toplevel()
            ventana_detalle.title(f"Idenficaciones de:  {fila_seleccionada[0]}")
        
            self.mostrarIdentifications(identifications,ventana_detalle)

    def mostrarIdentifications(self,identifications,ventana):
        anchos_columnas = {
                "#0":40,
                "Tipo Document": 200,
                "Documento": 300,
                "Pais": 150
            }
        identificationsView = ttk.Treeview(ventana)
        identificationsView["columns"] = ( "Tipo Document", "Documento", "Pais")  # Puedes agregar más columnas según sea necesario
        for col, ancho in anchos_columnas.items():
            identificationsView.column(col, width=ancho)
        identificationsView.heading("Tipo Document", text="Tipo Documento")
        identificationsView.heading("Documento", text="Documento")
        identificationsView.heading("Pais", text="Pais")

        for index, identificacion in enumerate(identifications, start=1):
            identificationsView.insert("", "end", text=str(index), values=[identificacion[1],identificacion[2],identificacion[3]])
        identificationsView.pack(expand=True, fill="both")

def abrir_ventana_principal():
    ventana_principal = mainMenu()

if __name__ == "__main__":
    abrir_ventana_principal()