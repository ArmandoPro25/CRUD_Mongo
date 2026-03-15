import tkinter as tk
from tkinter import messagebox, ttk, filedialog as fd
import subprocess
from pymongo import MongoClient as MC
import MongoXML as xml

class AlumnosFrame:
    def __init__(self, parent, callback_home):
        self.container = parent
        self.callback_home = callback_home
        
        self.colors = {
            'primary': '#4a90e2', 'success': '#2ecc71', 'clean': "#649331",
            'danger': '#e74c3c', 'dark': '#2c3e50', 'bg': '#f0f2f5',
            'white': '#ffffff', 'text': '#34495e'
        }

        try:
            self.client = MC("mongodb://localhost:27017/")
            self.db = self.client["BD_GrupoAlumno"]
        except Exception as e:
            messagebox.showerror("Error", f"No se conectó a Mongo: {e}")

        self.render()

    def render(self):
        self.main_frame = tk.Frame(self.container, bg=self.colors['bg'])
        self.main_frame.pack(fill="both", expand=True)

        header = tk.Frame(self.main_frame, bg=self.colors['dark'], height=80)
        header.pack(fill="x")
        
        tk.Button(header, text=" Volver", command=self.callback_home, bg=self.colors['dark'], fg="white", relief='flat', cursor='hand2', font=("Arial", 11)).pack(side="left", padx=20)
        
        tk.Label(header, text="Gestión de Alumnos", font=("Arial", 20, "bold"), bg=self.colors['dark'], fg="white").pack(pady=15)

        form_f = tk.Frame(self.main_frame, bg=self.colors['white'], relief='solid', bd=1)
        form_f.pack(fill="x", padx=30, pady=20)

        fields = ["Clave", "Nombre Completo", "Edad", "Grupo"]
        self.ents = []
        input_p = tk.Frame(form_f, bg=self.colors['white'])
        input_p.pack(pady=15)

        for i, f in enumerate(fields):
            row, col = i // 2, (i % 2) * 2
            tk.Label(input_p, text=f"{f}:", font=("Arial", 11, "bold"), 
                    bg=self.colors['white'], fg="#2c3e50").grid(row=row, column=col, padx=10, pady=5)
            e = tk.Entry(input_p, width=20, font=("Arial", 11), bg="white", fg="#2c3e50", relief="solid", bd=1, highlightthickness=2, highlightcolor="#3498db", highlightbackground="#bdc3c7")
            e.grid(row=row, column=col+1, padx=10, pady=5, ipady=5)
            self.ents.append(e)

        btn_p = tk.Frame(form_f, bg=self.colors['white'])
        btn_p.pack(pady=10)
        
        tk.Button(btn_p, text="Registrar", bg="#27ae60", fg="white", font=("Arial", 11, "bold"), relief="flat", bd=0, cursor="hand2", padx=15, pady=8, activebackground="#229954", activeforeground="white",
                 command=self.guardar).pack(side="left", padx=5)
        
        tk.Button(btn_p, text="Limpiar", bg="#95a5a6", fg="white", font=("Arial", 11, "bold"), relief="flat", bd=0, cursor="hand2", padx=15, pady=8, activebackground="#7f8c8d", activeforeground="white",
                 command=self.limpiar).pack(side="left", padx=5)
        
        tk.Button(btn_p, text="Buscar", bg="#3498db", fg="white", font=("Arial", 11, "bold"), relief="flat", bd=0, cursor="hand2",  padx=15, pady=8, activebackground="#2980b9", activeforeground="white",
                 command=self.abrir_buscar).pack(side="left", padx=5)
        
        tk.Button(btn_p, text="Modificar", bg="#f39c12", fg="white", font=("Arial", 11, "bold"), relief="flat", bd=0, cursor="hand2", padx=15, pady=8, activebackground="#e67e22", activeforeground="white",
                 command=self.modificar).pack(side="left", padx=5)
        
        tk.Button(btn_p, text="Eliminar", bg="#e74c3c", fg="white", font=("Arial", 11, "bold"), relief="flat", bd=0, cursor="hand2", padx=15, pady=8, activebackground="#c0392b", activeforeground="white",
                 command=self.eliminar).pack(side="left", padx=5)
        
        tk.Button(btn_p, text="Eliminar Todo", bg="#c0392b", fg="white", font=("Arial", 11, "bold"), relief="flat", bd=0, cursor="hand2", padx=15, pady=8, activebackground="#a93226", activeforeground="white",
                 command=self.eliminar_todos).pack(side="left", padx=5)

        btn_export = tk.Frame(form_f, bg=self.colors['white'])
        btn_export.pack(pady=10)

        self.imp = tk.StringVar()
        self.imp.set("JSON")
        opciones = ["JSON", "CSV", "XML"]
        impList = tk.OptionMenu(btn_export, self.imp, *opciones)
        impList.config(bg="#ecf0f1", fg="#2c3e50", font=("Arial", 10, "bold"), relief="flat", bd=0, cursor="hand2", highlightthickness=0, activebackground="#bdc3c7")
        impList["menu"].config(bg="#ecf0f1", fg="#2c3e50", font=("Arial", 10))
        impList.pack(side="left", padx=5)

        tk.Button(btn_export, text="Importar", bg="#16a085", fg="white", font=("Arial", 11, "bold"), relief="flat", bd=0, cursor="hand2", padx=15, pady=8, activebackground="#138d75", activeforeground="white",
                 command=self.importar).pack(side="left", padx=5)

        self.exp = tk.StringVar()
        self.exp.set("JSON")
        opciones = ["JSON", "CSV", "XML"]
        expList = tk.OptionMenu(btn_export, self.exp, *opciones)
        expList.config(bg="#ecf0f1", fg="#2c3e50", font=("Arial", 10, "bold"),  relief="flat", bd=0, cursor="hand2", highlightthickness=0, activebackground="#bdc3c7")
        expList["menu"].config(bg="#ecf0f1", fg="#2c3e50", font=("Arial", 10))
        expList.pack(side="left", padx=5)

        tk.Button(btn_export, text="Exportar", bg="#16a085", fg="white", font=("Arial", 11, "bold"), relief="flat", bd=0, cursor="hand2", padx=15, pady=8, activebackground="#138d75", activeforeground="white",
                 command=self.exportar).pack(side="left", padx=5)
        
        tk.Button(btn_export, text="Backup BSON", bg="#34495e", fg="white", font=("Arial", 11, "bold"), relief="flat", bd=0, cursor="hand2", padx=15, pady=8, activebackground="#2c3e50", activeforeground="white",
                 command=self.backup_bson).pack(side="left", padx=5)

        tk.Button(btn_export, text="Restaurar BSON", bg="#34495e", fg="white", font=("Arial", 11, "bold"), relief="flat", bd=0, cursor="hand2", padx=15, pady=8, activebackground="#2c3e50", activeforeground="white",
                 command=self.restaurar_bson).pack(side="left", padx=5)
        
        #Tabla

        table_frame = tk.Frame(self.main_frame, bg=self.colors['bg'])
        table_frame.pack(fill="both", expand=True, padx=30, pady=10)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background="#ffffff", foreground="#2c3e50", rowheight=30, fieldbackground="#ffffff", font=("Arial", 10))
        style.configure("Treeview.Heading", background="#34495e", foreground="white", font=("Arial", 11, "bold"), relief="flat")
        style.map("Treeview",
                 background=[("selected", "#3498db")])
        style.map("Treeview.Heading",
                 background=[("active", "#2c3e50")])

        self.tree = ttk.Treeview(table_frame, columns=("cve", "nom", "eda", "gru"), show="headings", height=8)
        self.tree.heading("cve", text="Clave")
        self.tree.heading("nom", text="Nombre")
        self.tree.heading("eda", text="Edad")
        self.tree.heading("gru", text="Grupo")
        self.tree.column("cve", width=100, anchor="center")
        self.tree.column("nom", width=250, anchor="w")
        self.tree.column("eda", width=80, anchor="center")
        self.tree.column("gru", width=100, anchor="center")

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        self.tree.pack(fill="both", expand=True)

        self.tree.tag_configure("oddrow", background="#ecf0f1")
        self.tree.tag_configure("evenrow", background="#ffffff")
        
        self.actualizar_tabla()

    def limpiar(self):
        for e in self.ents: e.delete(0, tk.END)
        self.ents[0].focus_set()

    def actualizar_tabla(self):
        self.tree.delete(*self.tree.get_children())
        for a in self.db.Alumno.find():
            self.tree.insert("", "end", values=(a["cveAlu"], a["nomAlu"], a.get("edaAlu",""), a.get("cveGru","")))

    def guardar(self):
        try:
            cve = self.ents[0].get().strip()
            nom = self.ents[1].get().strip()
            eda = self.ents[2].get().strip()
            gru = self.ents[3].get().strip()

            if cve == "" or nom == "" or eda == "" or gru == "":
                messagebox.showwarning("Validación", "Todos los campos son obligatorios")
                return

            if self.db.Alumno.find_one({"cveAlu": cve}):
                messagebox.showwarning("Error", f"La clave {cve} ya existe")
                return

            self.db.Alumno.insert_one({
                "cveAlu": cve, "nomAlu": nom,
                "edaAlu": int(eda), "cveGru": gru
            })
            self.actualizar_tabla()
            self.limpiar()
            messagebox.showinfo("Éxito", "Alumno registrado correctamente")
        except ValueError:
            messagebox.showerror("Error", "La edad debe ser un número")

    def modificar(self):
        item = self.tree.selection()
        if not item:
            messagebox.showwarning("Aviso", "Selecciona un alumno para modificar")
            return

        valores = self.tree.item(item)["values"]
        clave = str(valores[0])
        alumno = self.db.Alumno.find_one({"cveAlu": clave})

        if not alumno:
            messagebox.showerror("Error", "No se encontró el alumno")
            return

        mod_window = tk.Toplevel(self.main_frame)
        mod_window.title("Modificar Alumno")
        mod_window.geometry("350x250")
        mod_window.resizable(0, 0)
        mod_window.config(cursor="hand2")

        tk.Label(mod_window, text="Clave:", font=("Arial", 11, "bold")).grid(row=0, column=0, padx=10, pady=5)
        txt_cve = tk.Entry(mod_window, width=20, font=("Arial", 12))
        txt_cve.grid(row=0, column=1, padx=10, pady=5)
        txt_cve.insert(0, alumno["cveAlu"])
        txt_cve.config(state="disabled")

        tk.Label(mod_window, text="Nombre:", font=("Arial", 11, "bold")).grid(row=1, column=0, padx=10, pady=5)
        txt_nom = tk.Entry(mod_window, width=20, font=("Arial", 12))
        txt_nom.grid(row=1, column=1, padx=10, pady=5)
        txt_nom.insert(0, alumno["nomAlu"])

        tk.Label(mod_window, text="Edad:", font=("Arial", 11, "bold")).grid(row=2, column=0, padx=10, pady=5)
        txt_eda = tk.Entry(mod_window, width=20, font=("Arial", 12))
        txt_eda.grid(row=2, column=1, padx=10, pady=5)
        txt_eda.insert(0, str(alumno.get("edaAlu", "")))

        tk.Label(mod_window, text="Grupo:", font=("Arial", 11, "bold")).grid(row=3, column=0, padx=10, pady=5)
        txt_gru = tk.Entry(mod_window, width=20, font=("Arial", 12))
        txt_gru.grid(row=3, column=1, padx=10, pady=5)
        txt_gru.insert(0, alumno.get("cveGru", ""))

        lbl_msg = tk.Label(mod_window, text="", font=("Arial", 9))
        lbl_msg.grid(row=4, column=0, columnspan=2, pady=5)

        def guardar_cambios():
            nom = txt_nom.get().strip()
            eda = txt_eda.get().strip()
            gru = txt_gru.get().strip()

            if nom == "" or eda == "" or gru == "":
                lbl_msg.config(text="Todos los campos son obligatorios", fg="red")
                return

            try:
                self.db.Alumno.update_one({"cveAlu": clave}, {"$set": {"nomAlu": nom, "edaAlu": int(eda), "cveGru": gru}})
                mod_window.destroy()
                self.actualizar_tabla()
                messagebox.showinfo("Éxito", "Alumno modificado correctamente")
            except ValueError:
                lbl_msg.config(text="La edad debe ser un número", fg="red")

        btn_frame = tk.Frame(mod_window)
        btn_frame.grid(row=5, column=0, columnspan=2, pady=10)

        tk.Button(btn_frame, text="Guardar", bg="#2ecc71", fg="white", width=12,
                  command=guardar_cambios).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Cancelar", bg="#e74c3c", fg="white", width=12,
                  command=mod_window.destroy).pack(side="left", padx=5)

    def eliminar(self):
        item = self.tree.selection()
        if not item:
            messagebox.showwarning("Aviso", "Selecciona un alumno")
            return
        clave = self.tree.item(item)["values"][0]
        if messagebox.askyesno("Confirmar", f"¿Eliminar alumno {clave}?"):
            self.db.Alumno.delete_one({"cveAlu": str(clave)})
            self.actualizar_tabla()
            messagebox.showinfo("Éxito", "Alumno eliminado correctamente")

    def eliminar_todos(self):
        if messagebox.askyesno("Confirmar", "¿Eliminar TODOS los alumnos?"):
            self.db.Alumno.delete_many({})
            self.actualizar_tabla()
            messagebox.showinfo("Éxito", "Todos los alumnos fueron eliminados")

    def abrir_buscar(self):
        buscar_window = tk.Toplevel(self.main_frame)
        buscar_window.title("Buscar Alumno")
        buscar_window.geometry("350x200")
        buscar_window.resizable(0, 0)
        buscar_window.config(cursor="hand2")

        tk.Label(buscar_window, text="Clave:", font=("Arial", 11, "bold")).grid(row=0, column=0, padx=10, pady=5)
        txt_cve = tk.Entry(buscar_window, width=20, font=("Arial", 12))
        txt_cve.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(buscar_window, text="Nombre:", font=("Arial", 11, "bold")).grid(row=1, column=0, padx=10, pady=5)
        txt_nom = tk.Entry(buscar_window, width=20, font=("Arial", 12))
        txt_nom.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(buscar_window, text="Grupo:", font=("Arial", 11, "bold")).grid(row=2, column=0, padx=10, pady=5)
        txt_gru = tk.Entry(buscar_window, width=20, font=("Arial", 12))
        txt_gru.grid(row=2, column=1, padx=10, pady=5)

        lbl_msg = tk.Label(buscar_window, text="", font=("Arial", 9))
        lbl_msg.grid(row=3, column=0, columnspan=2, pady=5)

        def realizar_busqueda():
            cve = txt_cve.get().strip()
            nom = txt_nom.get().strip()
            gru = txt_gru.get().strip()

            if cve == "" and nom == "" and gru == "":
                lbl_msg.config(text="Debe ingresar al menos un campo para buscar.", fg="red")
                return

            query = {}
            if cve != "": query["cveAlu"] = cve
            if nom != "": query["nomAlu"] = nom
            if gru != "": query["cveGru"] = gru

            resultado = list(self.db.Alumno.find(query))

            self.tree.delete(*self.tree.get_children())
            if not resultado:
                lbl_msg.config(text="No se encontraron resultados.", fg="green")
                self.actualizar_tabla()
            else:
                for a in resultado:
                    self.tree.insert("", "end", values=(a["cveAlu"], a["nomAlu"], a.get("edaAlu",""), a.get("cveGru","")))
                lbl_msg.config(text=f"Se encontraron {len(resultado)} resultado(s).", fg="green")

        def limpiar_busqueda():
            txt_cve.delete(0, tk.END)
            txt_nom.delete(0, tk.END)
            txt_gru.delete(0, tk.END)
            lbl_msg.config(text="")
            self.actualizar_tabla()

        btn_frame = tk.Frame(buscar_window)
        btn_frame.grid(row=4, column=0, columnspan=2, pady=10)

        tk.Button(btn_frame, text="Buscar", bg="#4a90e2", fg="white", width=12,
                  command=realizar_busqueda).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Limpiar", bg="#649331", fg="white", width=12,
                  command=limpiar_busqueda).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Cerrar", bg="#e74c3c", fg="white", width=12,
                  command=buscar_window.destroy).pack(side="left", padx=5)

    def importar(self):
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
                try:
                    xml.importarXMLAlumnos(archImport)
                    self.actualizar_tabla()
                    messagebox.showinfo("Éxito", "Archivo XML importado correctamente")
                except Exception as e:
                    messagebox.showerror("Error", f"Error al importar: {e}")
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
                    "--collection=Alumno",
                    f"--type={tipoMongo}",
                    f"--file={archImport}",
                    "--drop"
                ]

                if tipoMongo == "csv":
                    comando.append("--headerline")

                try:
                    subprocess.run(comando, check=True)
                    self.actualizar_tabla()
                    messagebox.showinfo("Éxito", "Archivo importado correctamente")
                except Exception as e:
                    messagebox.showerror("Error", f"Error al importar: {e}")

    def exportar(self):
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
                try:
                    xml.exportarXMLAlumnos(archExport)
                    messagebox.showinfo("Éxito", "Archivo XML exportado correctamente")
                except Exception as e:
                    messagebox.showerror("Error", f"Error al exportar: {e}")
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
                    "--collection=Alumno",
                    f"--type={tipoMongo}",
                    f"--out={archExport}"
                ]

                if tipoMongo == "csv":
                    comando.append("--fields=cveAlu,nomAlu,edaAlu,cveGru")

                try:
                    subprocess.run(comando, check=True)
                    messagebox.showinfo("Éxito", "Archivo exportado correctamente")
                except Exception as e:
                    messagebox.showerror("Error", f"Error al exportar: {e}")

    def backup_bson(self):
        archBackup = fd.asksaveasfilename(
            title="Guardar backup BSON",
            defaultextension=".bson",
            filetypes=[("Archivos BSON","*.bson")]
        )
    
        if archBackup:
            try:
                comando = [
                    r"C:\Program Files\MongoDB\Tools\100\bin\mongodump.exe",
                    "--db=BD_GrupoAlumno",
                    "--collection=Alumno",
                    f"--out={archBackup.replace('.bson', '')}"
                ]
                subprocess.run(comando, check=True)
                messagebox.showinfo("Éxito", "Backup BSON creado correctamente")
            except Exception as e:
                messagebox.showerror("Error", f"Error al crear backup: {e}")

    def restaurar_bson(self):
        carpeta = fd.askdirectory(title="Seleccionar carpeta del backup")

        if carpeta:
            try:
                if messagebox.askyesno("Confirmar", "¿Restaurar este backup?"):

                    comando = [
                        r"C:\Program Files\MongoDB\Tools\100\bin\mongorestore.exe",
                        f"--dir={carpeta}"
                    ]

                    subprocess.run(comando, check=True)
                    self.actualizar_tabla()
                    messagebox.showinfo("Éxito", "Backup restaurado correctamente")
            except Exception as e:
                messagebox.showerror("Error", f"Error al restaurar: {e}")