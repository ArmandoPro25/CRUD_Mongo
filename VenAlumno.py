import tkinter as tk
from tkinter import messagebox, ttk
from pymongo import MongoClient as MC

class AlumnosFrame:
    def __init__(self, parent, callback_home):
        self.container = parent
        self.callback_home = callback_home
        
        self.colors = {
            'primary': '#4a90e2', 'success': '#2ecc71', 'clean': "#649331",
            'danger': '#e74c3c', 'dark': '#2c3e50', 'bg': '#f0f2f5',
            'white': '#ffffff', 'text': '#34495e'
        }

        # Conexión
        try:
            self.client = MC("mongodb://localhost:27017/")
            self.db = self.client["BD_GrupoAlumno"]
        except Exception as e:
            messagebox.showerror("Error", f"No se conectó a Mongo: {e}")

        self.render()

    def render(self):
        # Frame Principal
        self.main_frame = tk.Frame(self.container, bg=self.colors['bg'])
        self.main_frame.pack(fill="both", expand=True)

        # Header
        header = tk.Frame(self.main_frame, bg=self.colors['dark'], height=80)
        header.pack(fill="x")
        
        tk.Button(header, text=" Volver", command=self.callback_home,
                  bg=self.colors['dark'], fg="white", relief='flat', cursor='hand2').pack(side="left", padx=20)
        
        tk.Label(header, text="Gestión de Alumnos", font=("Arial", 20, "bold"), 
                 bg=self.colors['dark'], fg="white").pack(pady=15)

        # Formulario
        form_f = tk.Frame(self.main_frame, bg=self.colors['white'], relief='solid', bd=1)
        form_f.pack(fill="x", padx=30, pady=20)

        fields = ["Clave", "Nombre Completo", "Edad", "Grupo"]
        self.ents = []
        input_p = tk.Frame(form_f, bg=self.colors['white'])
        input_p.pack(pady=15)

        for i, f in enumerate(fields):
            row, col = i // 2, (i % 2) * 2
            tk.Label(input_p, text=f"{f}:", bg=self.colors['white']).grid(row=row, column=col, padx=10, pady=5)
            e = tk.Entry(input_p, font=("Arial", 11), relief='solid', bd=1)
            e.grid(row=row, column=col+1, padx=10, pady=5)
            self.ents.append(e)

        # Botones
        btn_p = tk.Frame(form_f, bg=self.colors['white'])
        btn_p.pack(pady=10)
        
        tk.Button(btn_p, text="Registrar", bg=self.colors['primary'], fg="white", width=15,
                  command=self.guardar).pack(side="left", padx=5)
        tk.Button(btn_p, text="Limpiar", bg=self.colors['clean'], fg="white", width=15,
                  command=self.limpiar).pack(side="left", padx=5)
        tk.Button(btn_p, text="Buscar", bg=self.colors['primary'], fg="white", width=15,
                  command=self.abrir_buscar).pack(side="left", padx=5)
        tk.Button(btn_p, text="Eliminar", bg=self.colors['danger'], fg="white", width=15,
                  command=self.eliminar).pack(side="left", padx=5)

        # Tabla
        self.tree = ttk.Treeview(self.main_frame, columns=("cve", "nom", "eda", "gru"), show="headings")
        self.tree.heading("cve", text="Clave"); self.tree.heading("nom", text="Nombre")
        self.tree.heading("eda", text="Edad"); self.tree.heading("gru", text="Grupo")
        self.tree.pack(fill="both", expand=True, padx=30, pady=10)
        
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
            self.db.Alumno.insert_one({
                "cveAlu": self.ents[0].get(), "nomAlu": self.ents[1].get(),
                "edaAlu": int(self.ents[2].get()), "cveGru": self.ents[3].get()
            })
            self.actualizar_tabla()
            self.limpiar()
        except: messagebox.showerror("Error", "Datos inválidos")

    def eliminar(self):
        item = self.tree.selection()
        if not item: return messagebox.showwarning("Aviso", "Selecciona un alumno")
        clave = self.tree.item(item)["values"][0]
        if messagebox.askyesno("Confirmar", f"¿Eliminar alumno {clave}?"):
            self.db.Alumno.delete_one({"cveAlu": str(clave)})
            self.actualizar_tabla()

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
