import tkinter as tk
from tkinter import messagebox, ttk, filedialog as fd
import subprocess
from pymongo import MongoClient as MC

class BackupFrame:
    def __init__(self, parent, callback_home):
        self.container = parent
        self.callback_home = callback_home
        
        self.colors = {
            'primary': '#4a90e2', 'success': '#2ecc71', 'danger': '#e74c3c',
            'dark': '#2c3e50', 'bg': '#f0f2f5', 'white': '#ffffff'
        }
        
        try:
            self.client = MC("mongodb://localhost:27017/")
            self.db = self.client["BD_GrupoAlumno"]
        except Exception as e:
            messagebox.showerror("Error", f"No se conectó a MongoDB: {e}")
        
        self.render()
    
    def render(self):
        self.main_frame = tk.Frame(self.container, bg=self.colors['bg'])
        self.main_frame.pack(fill="both", expand=True)
        
        header = tk.Frame(self.main_frame, bg=self.colors['dark'], height=80)
        header.pack(fill="x")
        
        tk.Button(header, text=" Volver", command=self.callback_home, bg=self.colors['dark'], fg="white", relief='flat', cursor='hand2').pack(side="left", padx=20)
        
        tk.Label(header, text="Gestión de Base de Datos", font=("Arial", 20, "bold"), bg=self.colors['dark'], fg="white").pack(pady=15)
        
        content = tk.Frame(self.main_frame, bg=self.colors['bg'])
        content.pack(fill="both", expand=True, padx=20, pady=20)
        
        tk.Label(content, text="Tablas de la Base de Datos", font=("Arial", 14, "bold"), bg=self.colors['bg']).pack(pady=10)
        
        self.tree = ttk.Treeview(content, columns=("tabla", "documentos"), show="headings", height=10)
        self.tree.heading("tabla", text="Tabla"); self.tree.heading("documentos", text="Documentos")
        self.tree.column("tabla", width=200); self.tree.column("documentos", width=100)
        self.tree.pack(fill="both", expand=True, pady=10)
        
        self.actualizar_tablas()
        
        btn_frame = tk.Frame(content, bg=self.colors['bg'])
        btn_frame.pack(pady=20)
        
        tk.Button(btn_frame, text="Backup Completo BD", bg=self.colors['success'], fg="white", width=20, height=2, relief="flat", command=self.backup_completo).pack(side="left", padx=10)
        
        tk.Button(btn_frame, text="Restaurar BD", bg=self.colors['primary'], fg="white", width=20, height=2, relief="flat", command=self.restaurar_completo).pack(side="left", padx=10)
        
        tk.Button(btn_frame, text="Eliminar BD", bg=self.colors['danger'], fg="white",  width=20, height=2, relief="flat", command=self.eliminar_bd).pack(side="left", padx=10)
    
    def actualizar_tablas(self):
        self.tree.delete(*self.tree.get_children())
        colecciones = self.db.list_collection_names()
        for col in colecciones:
            count = self.db[col].count_documents({})
            self.tree.insert("", "end", values=(col, count))
    
    def backup_completo(self):
        archBackup = fd.asksaveasfilename(
            title="Guardar backup completo",
            defaultextension="",
            filetypes=[("Carpeta", "")]
        )
        
        if archBackup:
            try:
                comando = [
                    r"C:\Program Files\MongoDB\Tools\100\bin\mongodump.exe",
                    "--db=BD_GrupoAlumno",
                    f"--out={archBackup}"
                ]
                subprocess.run(comando, check=True)
                messagebox.showinfo("Éxito", "Backup completo creado correctamente")
            except Exception as e:
                messagebox.showerror("Error", f"Error al crear backup: {e}")
    
    def restaurar_completo(self):
        carpeta = fd.askdirectory(title="Seleccionar carpeta de backup")
        
        if carpeta:
            try:
                if messagebox.askyesno("Confirmar", "¿Restaurar la base de datos completa? Se sobrescribirán todos los datos"):
                    comando = [
                        r"C:\Program Files\MongoDB\Tools\100\bin\mongorestore.exe",
                        "--db=BD_GrupoAlumno",
                        f"--dir={carpeta}/BD_GrupoAlumno"
                    ]
                    subprocess.run(comando, check=True)
                    self.actualizar_tablas()
                    messagebox.showinfo("Éxito", "Base de datos restaurada correctamente")
            except Exception as e:
                messagebox.showerror("Error", f"Error al restaurar: {e}")
    
    def eliminar_bd(self):
        if messagebox.askyesno("Advertencia", "¿Eliminar TODA la base de datos? Esta acción no se puede deshacer"):
            try:
                self.client.drop_database("BD_GrupoAlumno")
                self.actualizar_tablas()
                messagebox.showinfo("Éxito", "Base de datos eliminada correctamente")
            except Exception as e:
                messagebox.showerror("Error", f"Error al eliminar: {e}")