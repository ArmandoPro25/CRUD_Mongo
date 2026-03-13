import tkinter as tk
from tkinter import filedialog as fd
import subprocess
from pymongo import MongoClient as MC
import MongoXML as xml

class GruposFrame:
    def __init__(self, parent, callback_home):
        self.container = parent
        self.callback_home = callback_home
        
        # Cadena de conexión local a MongoDB
        self.client = MC("mongodb://localhost:27017/")
        self.db = self.client["BD_GrupoAlumno"]
        self.grupos = self.db["Grupo"]
        self.alumnos = self.db["Alumno"]
        
        self.render()
    
    def render(self):
        # Frame principal
        self.window = tk.Frame(self.container, bg="#f0f2f5")
        self.window.pack(fill="both", expand=True)
        
        # Header
        header = tk.Frame(self.window, bg="#2c3e50", height=80)
        header.pack(fill="x")
        
        tk.Button(header, text=" Volver", command=self.callback_home,
                  bg="#2c3e50", fg="white", relief='flat', cursor='hand2', font=("Arial", 11)).pack(side="left", padx=20)
        
        tk.Label(header, text="Gestión de Grupos", font=("Arial", 20, "bold"), 
                 bg="#2c3e50", fg="white").pack(pady=15)
        
        # Contenido principal
        content = tk.Frame(self.window, bg="#f0f2f5")
        content.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Etiquetas
        lbl_Bienvenido = tk.Label(content, text="Bienvenido(a)", font=("Arial", 11), bg="#f0f2f5")
        lbl_Bienvenido.grid(row=0, column=0, padx=10, pady=10)

        lbl_cveGru = tk.Label(content, text="Clave:", font=("Arial", 11, "bold"), bg="#f0f2f5")
        lbl_cveGru.grid(row=1, column=0, padx=10, pady=5)

        lbl_nomGru = tk.Label(content, text="Nombre:", font=("Arial", 11, "bold"), bg="#f0f2f5")
        lbl_nomGru.grid(row=2, column=0, padx=10, pady=5)

        # Entradas de texto
        self.txt_cveGru = tk.Entry(content, width=20, font=("Arial",12))
        self.txt_cveGru.grid(row=1, column=1)

        self.txt_nomGru = tk.Entry(content, width=20, font=("Arial",12))
        self.txt_nomGru.grid(row=2, column=1)

        # Botón para buscar grupo
        btn_buscar = tk.Button(content, text=" Buscar ", font=("Arial", 12, "bold"), bg="white", fg="black", command=self.Buscar)
        btn_buscar.grid(row=1, column=3, pady=10, padx=10)

        # Botón para agregar grupo
        btn_agregar = tk.Button(content, text="Agregar ", font=("Arial", 12, "bold"), bg="white", fg="black", command=self.Agregar)
        btn_agregar.grid(row=2, column=3, pady=10, padx=10)

        # Botón para limpiar cajas de texto
        btn_limpiar = tk.Button(content, text="  Limpiar  ", font=("Arial", 12, "bold"), bg="white", fg="black", command=self.Limpiar)
        btn_limpiar.grid(row=1, column=4, pady=10, padx=10)

        # Botón para eliminar grupo
        btn_eliminar = tk.Button(content, text="Eliminar", font=("Arial", 12, "bold"), bg="white", fg="black", command=self.Eliminar)
        btn_eliminar.grid(row=1, column=5, pady=10, padx=10)

        # Botón para eliminar todos los registros
        btn_purgar = tk.Button(content, text=" Purgar ", font=("Arial", 12, "bold"), bg="white", fg="black", command=self.Purgar)
        btn_purgar.grid(row=2, column=5, pady=10, padx=10)

        # Botón para actualizar grupo
        btn_actualizar = tk.Button(content, text="Actualizar", font=("Arial", 12, "bold"), bg="white", fg="black", command=self.Actualizar)
        btn_actualizar.grid(row=2, column=4, pady=10, padx=10)

        # Botón para importar (Restore)
        btn_importar = tk.Button(content, text="Importar", font=("Arial", 12, "bold"), bg="white", fg="black", command=self.Importar)
        btn_importar.grid(row=1, column=7, pady=10, padx=10)

        # Botón para exportar (Backup)
        btn_exportar = tk.Button(content, text="Exportar", font=("Arial", 12, "bold"), bg="white", fg="black", command=self.Exportar)
        btn_exportar.grid(row=2, column=7, pady=10, padx=10)

        # Texto para mostrar resultados
        self.txt_resultados = tk.Text(content, width=70, height=10)
        self.txt_resultados.grid(row=3, column=0, columnspan=6, padx=10, pady=10)

        # Lista de importación
        self.imp = tk.StringVar()
        self.imp.set("JSON")
        opciones = ["JSON", "CSV", "XML"]
        impList = tk.OptionMenu(content, self.imp, *opciones)
        impList.grid(row=1, column=6, pady=10, padx=10)

        # Lista de exportación
        self.exp = tk.StringVar()
        self.exp.set("JSON")
        opciones = ["JSON", "CSV", "XML"]
        expList = tk.OptionMenu(content, self.exp, *opciones)
        expList.grid(row=2, column=6, pady=10, padx=10)

        # Tabla de grupos
        table_frame = tk.Frame(self.window, bg="#f0f2f5")
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)

        self.tree = tk.ttk.Treeview(table_frame, columns=("cve", "nom"), show="headings", height=8)
        self.tree.heading("cve", text="Clave")
        self.tree.heading("nom", text="Nombre")
        self.tree.column("cve", width=100)
        self.tree.column("nom", width=200)
        self.tree.pack(fill="both", expand=True)

        self.actualizar_tabla()

    def actualizar_tabla(self):
        self.tree.delete(*self.tree.get_children())
        for grupo in self.grupos.find():
            self.tree.insert("", "end", values=(grupo["cveGru"], grupo["nomGru"]))

    # Funcion para limpiar cadenas de texto
    def Limpiar(self):
        self.txt_cveGru.delete(0, tk.END)
        self.txt_nomGru.delete(0, tk.END)
        self.txt_resultados.delete(1.0, tk.END)

    # Funcion para buscar grupos
    def Buscar(self):
        if self.txt_cveGru.get() == "" and self.txt_nomGru.get() == "":
            self.LimpiarValidacion()
            self.Validacion("Debe ingresar al menos un campo para buscar.", "red")
        elif self.txt_cveGru.get() != "" and self.txt_nomGru.get() == "":
            self.LimpiarValidacion()
            resultado = list(self.grupos.find({"cveGru":self.txt_cveGru.get()}))
            if not resultado:
                self.Validacion(f"No se encontraron resultados para la clave {self.txt_cveGru.get()}.", "green")
            else:
                for grupo in resultado:
                    self.Validacion(f"Clave: {grupo['cveGru']}\nNombre: {grupo['nomGru']}\n\n", "black")
        elif self.txt_cveGru.get() == "" and self.txt_nomGru.get() != "":
            self.LimpiarValidacion()
            resultado = list(self.grupos.find({"nomGru":self.txt_nomGru.get()}))
            if not resultado:
                self.Validacion(f"No se encontraron resultados para el nombre {self.txt_nomGru.get()}.", "green")
            else:
                for grupo in resultado:
                    self.Validacion(f"Clave: {grupo['cveGru']}\nNombre: {grupo['nomGru']}\n\n", "black")
        elif self.txt_cveGru.get() != "" and self.txt_nomGru.get() != "":
            self.LimpiarValidacion()
            resultado = list(self.grupos.find({"$and": [{"cveGru": self.txt_cveGru.get()}, {"nomGru": self.txt_nomGru.get()}]}))
            if not resultado:
                self.Validacion(f"No se encontraron resultados para el grupo {self.txt_nomGru.get()} con clave {self.txt_cveGru.get()}.", "green")
            else:
                for grupo in resultado:
                    self.Validacion(f"Clave: {grupo['cveGru']}\nNombre: {grupo['nomGru']}\n\n", "black")
        else:
            self.LimpiarValidacion()
            self.Validacion("No se encontraron resultados con la clave y el nombre\nproporcionados.", "green")

    def Agregar(self):
        cve = self.txt_cveGru.get().strip()
        nom = self.txt_nomGru.get().strip()

        if cve == "" and nom == "":
            self.LimpiarValidacion()
            self.Validacion("Ingrese la clave o el nombre del grupo a agregar", "red")
        elif cve != "" and nom == "":
            self.LimpiarValidacion()
            self.Validacion("Ingrese el nombre del grupo a agregar", "red")
        elif cve == "" and nom != "":
            self.LimpiarValidacion()
            self.Validacion("Ingrese la clave del grupo a agregar", "red")
        elif len(cve) > 7:
            self.LimpiarValidacion()
            self.Validacion("La clave del grupo no debe exceder los 7 caracteres.", "red")
        elif len(nom) > 15:
            self.LimpiarValidacion()
            self.Validacion("El nombre del grupo no debe exceder los 15 caracteres.", "red")
        elif self.grupos.find_one({"cveGru": cve}):
            self.LimpiarValidacion()
            self.Validacion(f"La clave {cve} ya existe.", "red")
        else:
            self.grupos.insert_one({"cveGru": cve, "nomGru": nom})
            self.LimpiarValidacion()
            self.Validacion(f"Grupo {nom} insertado.", "green")
            self.actualizar_tabla()

    def Eliminar(self):
        if self.txt_cveGru.get() == "" and self.txt_nomGru.get() == "":
            self.LimpiarValidacion()
            self.Validacion("Ingrese la clave o el nombre del grupo a eliminar", "red")
        elif self.txt_cveGru.get() != "" and self.txt_nomGru.get() == "":
            self.LimpiarValidacion()
            resultado = list(self.grupos.find({"cveGru":self.txt_cveGru.get()}))
            if not resultado:
                self.Validacion(f"No se encontraron resultados para la clave {self.txt_cveGru.get()}.", "green")
            else:
                self.ConfirmarEliminacion(self.txt_cveGru.get(), "")
        elif self.txt_cveGru.get() == "" and self.txt_nomGru.get() != "":
            self.LimpiarValidacion()
            resultado = list(self.grupos.find({"nomGru":self.txt_nomGru.get()}))
            if not resultado:
                self.Validacion(f"No se encontraron resultados para el grupo con nombre {self.txt_nomGru.get()}.", "green")
            else:
                self.ConfirmarEliminacion("", self.txt_nomGru.get())
        elif self.txt_cveGru.get() != "" and self.txt_nomGru.get() != "":
            self.LimpiarValidacion()
            resultado = list(self.grupos.find({"$and": [{"cveGru": self.txt_cveGru.get()}, {"nomGru": self.txt_nomGru.get()}]}))
            if not resultado:
                self.Validacion(f"No se encontraron resultados para el grupo {self.txt_nomGru.get()} con clave {self.txt_cveGru.get()}.", "green")
            else:
                self.ConfirmarEliminacion(self.txt_cveGru.get(), self.txt_nomGru.get())
        else:
            self.LimpiarValidacion()
            self.Validacion("No se encontraron resultados con la clave y el nombre\nproporcionados.", "green")

    def Actualizar(self):
        cve = self.txt_cveGru.get().strip()
        nom = self.txt_nomGru.get().strip()

        if cve == "" and nom == "":
            self.LimpiarValidacion()
            self.Validacion("Ingrese la clave o el nombre del grupo a actualizar", "red")
        elif cve != "" and nom == "":
            self.LimpiarValidacion()
            resultado = list(self.grupos.find({"cveGru":cve}))
            if not resultado:
                self.Validacion(f"No se encontraron resultados para la clave {cve}.", "green")
            else:
                self.ActualizarForm(cve, "")        
        elif cve == "" and nom != "":
            self.LimpiarValidacion()
            resultado = list(self.grupos.find({"nomGru":nom}))
            if not resultado:
                self.Validacion(f"No se encontraron resultados para el grupo con nombre {nom}.", "green")
            else:
                self.ActualizarForm("", nom)        
        elif cve != "" and nom != "":
            self.LimpiarValidacion()
            resultado = list(self.grupos.find({"$and": [{"cveGru": cve}, {"nomGru": nom}]}))
            if not resultado:
                self.Validacion(f"No se encontraron resultados para el grupo {nom} con clave {cve}.", "green")
            else:
                self.ActualizarForm(cve, nom)
        else:
            self.LimpiarValidacion()
            self.Validacion("No se encontraron resultados con la clave y el nombre\nproporcionados.", "green")

    # Configuración de ventana emergente para eliminar
    def ConfirmarEliminacion(self, txt_cveGru, txt_nomGru):
        confirmacion = tk.Toplevel(self.window)
        confirmacion.title("Confirmar Eliminación")
        confirmacion.geometry("300x150")
        confirmacion.resizable(0, 0)
        confirmacion.config(cursor="hand2")

        if txt_cveGru != "" and txt_nomGru == "":
            lbl_confirmacion = tk.Label(confirmacion, text="¿Está seguro de eliminar\nel grupo con clave " + txt_cveGru + "?", font=("Arial", 11))
        elif txt_cveGru == "" and txt_nomGru != "":
            lbl_confirmacion = tk.Label(confirmacion, text="¿Está seguro de eliminar\nel grupo con nombre " + txt_nomGru + "?", font=("Arial", 11))
        else:
            lbl_confirmacion = tk.Label(confirmacion, text="¿Está seguro de eliminar\nel grupo " + txt_nomGru + " con clave " + txt_cveGru + "?", font=("Arial", 11))
        
        lbl_confirmacion.pack(pady=10)

        def EliminarGrupo():
            clave_grupo = None
            if txt_cveGru != "" and txt_nomGru == "":
                clave_grupo = txt_cveGru
                self.grupos.delete_one({"cveGru": txt_cveGru})
                self.LimpiarValidacion()
                self.Validacion(f"Grupo con clave {txt_cveGru} eliminado", "green")
            elif txt_cveGru == "" and txt_nomGru != "":
                grupo = self.grupos.find_one({"nomGru": txt_nomGru})
                if grupo:
                    clave_grupo = grupo["cveGru"]
                self.grupos.delete_one({"nomGru": txt_nomGru})
                self.LimpiarValidacion()
                self.Validacion(f"Grupo con nombre {txt_nomGru} eliminado", "green")
            else:
                clave_grupo = txt_cveGru
                self.grupos.delete_one({"$and": [{"cveGru": txt_cveGru}, {"nomGru": txt_nomGru}]})
                self.LimpiarValidacion()
                self.Validacion(f"Grupo {txt_nomGru} con clave {txt_cveGru} eliminado.", "green")
            
            # Eliminación en cascada: eliminar alumnos del grupo
            if clave_grupo:
                resultado_alumnos = self.alumnos.delete_many({"cveGru": clave_grupo})
                if resultado_alumnos.deleted_count > 0:
                    self.Validacion(f"Se eliminaron {resultado_alumnos.deleted_count} alumno(s) del grupo.", "green")
            
            self.actualizar_tabla()
            confirmacion.destroy()

        btn_confirmar = tk.Button(confirmacion, text="Eliminar", font=("Arial", 12, "bold"), bg="white", fg="black", command=EliminarGrupo)
        btn_confirmar.pack(side=tk.RIGHT, padx=35, pady=10)

        btn_cancelar = tk.Button(confirmacion, text="Cancelar", font=("Arial", 12, "bold"), bg="white", fg="black", command=confirmacion.destroy)
        btn_cancelar.pack(side=tk.LEFT, padx=35, pady=10)

    # Configuración de ventana emergente para actualizar
    def ActualizarForm(self, clave, nombre):
        actualizacion = tk.Toplevel(self.window)
        actualizacion.title("Actualizar Grupo")
        actualizacion.geometry("320x180")
        actualizacion.resizable(0, 0)
        actualizacion.config(cursor="hand2")

        # Etiquetas
        act_cveGru_lbl = tk.Label(actualizacion, text="Clave:", font=("Arial", 11, "bold"))
        act_cveGru_lbl.grid(row=1, column=0, padx=10, pady=5)

        act_nomGru_lbl = tk.Label(actualizacion, text="Nombre:", font=("Arial", 11, "bold"))
        act_nomGru_lbl.grid(row=2, column=0, padx=10, pady=5)

        # Entradas de texto
        act_cveGru = tk.Entry(actualizacion, width=20, font=("Arial",12))
        act_cveGru.grid(row=1, column=1)

        act_nomGru = tk.Entry(actualizacion, width=20, font=("Arial",12))
        act_nomGru.grid(row=2, column=1)

        # Etiquetas
        lbl_Validacion = tk.Label(actualizacion, text="Ingresa los datos actualizados", font=("Arial", 8))
        lbl_Validacion.grid(row=3, column=0, columnspan=2)

        if clave != "" and nombre != "":
            act_cveGru.insert(0, clave)
            act_nomGru.insert(0, nombre)
        elif clave != "":
            act_cveGru.insert(0, clave)
        elif nombre != "":
            act_nomGru.insert(0, nombre)

        def ActualizarGrupo():
            nueva_cve = act_cveGru.get().strip()
            nuevo_nom = act_nomGru.get().strip()

            # Validaciones
            if nueva_cve == "" and nuevo_nom == "":
                lbl_Validacion.config(text="Los campos no pueden estar vacios.", fg="red")
            elif nueva_cve != "" and nuevo_nom == "":
                lbl_Validacion.config(text="El nombre del grupo no puede estar vacio.", fg="red")
            elif nueva_cve == "" and nuevo_nom != "":
                lbl_Validacion.config(text="La clave no puede estar vacia.", fg="red")
            elif len(nueva_cve) > 7:
                lbl_Validacion.config(text="La clave no puede exceder los 7 caracteres.", fg="red")
            elif len(nuevo_nom) > 15:
                lbl_Validacion.config(text="El nombre no puede exceder los 15 caracteres.", fg="red")
            else:
                existente = self.grupos.find_one({"cveGru": nueva_cve})
                if existente and existente["cveGru"] != clave:
                    lbl_Validacion.config(text=f"La clave {nueva_cve} ya pertenece a otro grupo.", fg="red")
                    return

                if clave != "" and nombre == "":
                    self.grupos.update_one({"cveGru": clave}, {"$set": {"cveGru": nueva_cve, "nomGru": nuevo_nom}})
                elif clave == "" and nombre != "":
                    self.grupos.update_one({"nomGru": nombre}, {"$set": {"cveGru": nueva_cve, "nomGru": nuevo_nom}})
                elif clave != "" and nombre != "":
                    self.grupos.update_one({"cveGru": clave, "nomGru": nombre}, {"$set": {"cveGru": nueva_cve, "nomGru": nuevo_nom}})

                actualizacion.destroy()
                self.LimpiarValidacion()
                self.Validacion(f"Se actualizó el grupo {nueva_cve}", "green")
                self.actualizar_tabla()

        btn_noAct = tk.Button(actualizacion, text="Cancelar", font=("Arial", 12, "bold"), bg="white", fg="black", command=actualizacion.destroy)
        btn_noAct.grid(row=4, column=0, padx=15, pady=10)
        
        btn_act = tk.Button(actualizacion, text="Actualizar", font=("Arial", 12, "bold"), bg="white", fg="black", command=ActualizarGrupo)
        btn_act.grid(row=4, column=1, padx=15, pady=10)

    def Purgar(self):
        self.grupos.delete_many({})
        self.alumnos.delete_many({})
        self.LimpiarValidacion()
        self.Validacion("Se eliminaron TODOS los grupos y sus alumnos.", "red")
        self.actualizar_tabla()

    def Importar(self):
        formatos = {
            "JSON": ("*.json","json"),
            "CSV": ("*.csv","csv")
        }
        formato = self.imp.get()

        if formato == "XML":
            archImport = fd.askopenfilename(
                title="Seleccionar archivo",
                filetypes=[("Archivos XML","*.xml")]
            )

            if archImport:
                xml.importarXML(archImport)
                self.LimpiarValidacion()
                self.Validacion("Restauración XML importada correctamente.\n","green")
                self.actualizar_tabla()

            return

        if formato in formatos:
            ext, tipoMongo = formatos[formato]
            archImport = fd.askopenfilename(
                title="Seleccionar archivo",
                filetypes=[(f"Archivos {formato}",ext)]
            )

            if archImport:
                comando = [
                    r"C:\Program Files\MongoDB\Tools\100\bin\mongoimport.exe",
                    "--db=BD_GrupoAlumno",
                    "--collection=Grupo",
                    f"--type={tipoMongo}",
                    f"--file={archImport}",
                    "--drop"
                ]

                if tipoMongo == "csv":
                    comando.append("--headerline")

                try:
                    subprocess.run(comando, check=True)
                    self.LimpiarValidacion()
                    self.Validacion("Restauración importada correctamente.\n","green")
                    self.actualizar_tabla()

                except Exception as e:
                    self.LimpiarValidacion()
                    self.Validacion(f"Error al importar:\n{e}","red")

    def Exportar(self):
        formatos = {
            "JSON": ("*.json", "json"),
            "CSV": ("*.csv", "csv")
        }
        formato = self.exp.get()

        if formato == "XML":
            archExport = fd.asksaveasfilename(
                title="Guardar archivo",
                defaultextension=".xml",
                filetypes=[("Archivos XML","*.xml")]
            )

            if archExport:
                xml.exportarXML(archExport)
                self.LimpiarValidacion()
                self.Validacion("Backup XML exportado correctamente.\n", "green")

            return

        if formato in formatos:
            ext, tipoMongo = formatos[formato]
            archExport = fd.asksaveasfilename(
                title="Guardar archivo",
                defaultextension=ext,
                filetypes=[(f"Archivos {formato}", ext)]
            )

            if archExport:
                comando = [
                    r"C:\Program Files\MongoDB\Tools\100\bin\mongoexport.exe",
                    "--db=BD_GrupoAlumno",
                    "--collection=Grupo",
                    f"--type={tipoMongo}",
                    f"--out={archExport}"
                ]

                if tipoMongo == "csv":
                    comando.append("--fields=cveGru,nomGru")

                try:
                    subprocess.run(comando, check=True)
                    self.LimpiarValidacion()
                    self.Validacion("Backup exportado correctamente.\n", "green")

                except Exception as e:
                    self.LimpiarValidacion()
                    self.Validacion(f"Error al exportar:\n{e}", "red")

    def Validacion(self, validacion, alert):
        if validacion != "":
            self.txt_resultados.tag_config("color", foreground=alert)  
            self.txt_resultados.insert(tk.END, validacion, "color")

    def LimpiarValidacion(self):
        self.txt_resultados.delete(1.0, tk.END)


