import tkinter as tk
from tkinter import ttk
from VenAlumno import AlumnosFrame
from VenGrupo import GruposFrame

class SistemaPrincipal:
    def __init__(self, root):
        self.root = root
        self.root.title("SISTEMA DE CONTROL ESCOLAR")
        self.root.geometry("1000x750")
        self.root.configure(bg="#f0f2f5")

        # Contenedor 
        self.contenedor_vistas = tk.Frame(self.root, bg="#f0f2f5")
        self.contenedor_vistas.pack(fill="both", expand=True)

        self.mostrar_home()

    def limpiar_pantalla(self):
        for widget in self.contenedor_vistas.winfo_children():
            widget.destroy()

    def mostrar_home(self):
        self.limpiar_pantalla()
        
  
        header = tk.Frame(self.contenedor_vistas, bg="#2c3e50", height=150)
        header.pack(fill="x")
        tk.Label(header, text="MENU PRINCIPAL", font=("Arial", 30, "bold"), fg="white", bg="#2c3e50").pack(pady=45)

        # Panel de botones
        btn_frame = tk.Frame(self.contenedor_vistas, bg="#f0f2f5")
        btn_frame.pack(expand=True)

        # Botón Alumnos
        tk.Button(btn_frame, text="GESTIONAR ALUMNOS", font=("Arial", 14, "bold"),
                  bg="#4a90e2", fg="white", width=30, height=3, relief="flat",
                  command=self.ir_a_alumnos).pack(pady=20)

        # Botón Grupos
        tk.Button(btn_frame, text="GESTIONAR GRUPOS", font=("Arial", 14, "bold"),
                  bg="#2ecc71", fg="white", width=30, height=3, relief="flat",
                  command=self.ir_a_grupos).pack(pady=20)

    def ir_a_alumnos(self):
        self.limpiar_pantalla()
        AlumnosFrame(self.contenedor_vistas, self.mostrar_home)

    def ir_a_grupos(self):
        self.limpiar_pantalla()
        GruposFrame(self.contenedor_vistas, self.mostrar_home)

if __name__ == "__main__":
    root = tk.Tk()
    app = SistemaPrincipal(root)
    root.mainloop()
