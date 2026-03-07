import tkinter as tk
from pymongo import MongoClient as MC

# Cadena de conexión local a MongoDB
client = MC("mongodb://localhost:27017/")
db = client["BD_GrupoAlumno"]
grupos = db["Grupo"]

def Limpiar():
    txt_cveGru.delete(0, tk.END)
    txt_nomGru.delete(0, tk.END)

def Buscar():
    # Buscar grupo
    resultadoOR = list(grupos.find({"$or": [{"cveGru": txt_cveGru.get()}, {"nomGru": txt_nomGru.get()}]}))
    resultadoAND = list(grupos.find({"$and": [{"cveGru": txt_cveGru.get()}, {"nomGru": txt_nomGru.get()}]}))

    if (txt_cveGru.get() == "" and txt_nomGru.get() == ""):
        print("Ingrese la clave o el nombre del grupo a buscar")
    elif (len(resultadoOR) == 0):
        print("No se encontraron resultados.")
    elif (txt_cveGru.get() != "" and txt_nomGru.get() == ""):
        for grupo in grupos.find({"cveGru":txt_cveGru.get()}):
            print(grupo)
    elif (txt_cveGru.get() == "" and txt_nomGru.get() != ""):
        for grupo in grupos.find({"nomGru":txt_nomGru.get()}):
            print(grupo)
    elif (txt_cveGru.get() != "" and txt_nomGru.get() != "" and len(resultadoAND) > 0):
        for grupo in resultadoAND:
            print(grupo)  
    else:
        print("No se encontraron resultados con la clave y el nombre proporcionados.")  

def Agregar():
    if (txt_cveGru.get() == "" and txt_nomGru.get() == ""):
        print("Ingrese la clave o el nombre del grupo a agregar")
    elif (txt_cveGru.get() != "" and txt_nomGru.get() == ""):
        print("Ingrese el nombre del grupo a agregar")
    elif (txt_cveGru.get() == "" and txt_nomGru.get() != ""):
        print("Ingrese la clave del grupo a agregar")
    elif (len(txt_cveGru.get()) > 7):
        print("La clave del grupo no debe exceder los 7 caracteres.")  
    elif (len(txt_nomGru.get()) > 15):
        print("El nombre del grupo no debe exceder los 15 caracteres.")
    else:
        grupos.insert_one({"cveGru":txt_cveGru.get(), "nomGru": txt_nomGru.get()})
        print("\nGrupo Insertado")

def Eliminar():
    resultadoOR = list(grupos.find({"$or": [{"cveGru": txt_cveGru.get()}, {"nomGru": txt_nomGru.get()}]}))
    resultadoAND = list(grupos.find({"$and": [{"cveGru": txt_cveGru.get()}, {"nomGru": txt_nomGru.get()}]}))

    if (txt_cveGru.get() == "" and txt_nomGru.get() == ""):
        print("Ingrese la clave o el nombre del grupo a eliminar")
    elif (len(resultadoOR) == 0):
        print("No se encontraron resultados para eliminar.")
    elif (txt_cveGru.get() != "" and txt_nomGru.get() == ""):
        ConfirmarEliminacion(txt_cveGru.get(), "")
    elif (txt_cveGru.get() == "" and txt_nomGru.get() != ""):
        ConfirmarEliminacion("", txt_nomGru.get())
    elif (txt_cveGru.get() != "" and txt_nomGru.get() != "" and len(resultadoAND) > 0):
        ConfirmarEliminacion(txt_cveGru.get(), txt_nomGru.get())
    else:
        print("No se encontraron resultados con la clave y el nombre proporcionados.") 

def Actualizar():
    print("Función de actualizar grupo aún no implementada.")

# Configuración de ventana emergente para eliminar
def ConfirmarEliminacion(txt_cveGru, txt_nomGru):
    confirmacion = tk.Toplevel(window)
    confirmacion.title("Confirmar Eliminación")
    confirmacion.geometry("300x150")
    confirmacion.resizable(0, 0)
    confirmacion.config(cursor="hand2")

    if (txt_cveGru != "" and txt_nomGru == ""):
        lbl_confirmacion = tk.Label(confirmacion, text="¿Está seguro de eliminar\nel grupo con clave " + txt_cveGru + " ?", font=("Arial", 11))
    elif (txt_cveGru == "" and txt_nomGru != ""):
        lbl_confirmacion = tk.Label(confirmacion, text="¿Está seguro de eliminar\nel grupo con nombre " + txt_nomGru + " ?", font=("Arial", 11))
    else:
        lbl_confirmacion = tk.Label(confirmacion, text="¿Está seguro de eliminar\nel grupo " + txt_nomGru + " con clave " + txt_cveGru + " ?", font=("Arial", 11))
    
    lbl_confirmacion.pack(pady=20)

    def EliminarGrupo():
        if (txt_cveGru != "" and txt_nomGru == ""):
            grupos.delete_one({"cveGru": txt_cveGru})
            print("\nGrupo con clave " + txt_cveGru + " eliminado.")
        elif (txt_cveGru == "" and txt_nomGru != ""):
            grupos.delete_one({"nomGru": txt_nomGru})
            print("\nGrupo con nombre " + txt_nomGru + " eliminado.")
        else:
            grupos.delete_one({"$and": [{"cveGru": txt_cveGru}, {"nomGru": txt_nomGru}]})
            print("\nGrupo " + txt_nomGru + " con clave " + txt_cveGru + " eliminado.")
        confirmacion.destroy()

    btn_confirmar = tk.Button(confirmacion, text="Aceptar", font=("Arial", 12, "bold"), bg="white", fg="black", command=EliminarGrupo)
    btn_confirmar.pack(side=tk.RIGHT, padx=35)

    btn_cancelar = tk.Button(confirmacion, text="Cancelar", font=("Arial", 12, "bold"), bg="white", fg="black", command=confirmacion.destroy)
    btn_cancelar.pack(side=tk.LEFT, padx=35)

# Configuración de ventana emergente para actualizar
def ActualizarForm(clave, nombre):
    confirmacion = tk.Toplevel(window)
    confirmacion.title("Actualizar Grupo")
    confirmacion.geometry("300x150")
    confirmacion.resizable(0, 0)
    confirmacion.config(cursor="hand2")

    # Etiquetas
    lbl_Bienvenido = tk.Label(window, text="Actualizar Grupo", font=("Arial", 11))
    lbl_Bienvenido.grid(row=0, column=0, padx=10, pady=10)

    lbl_cveGru = tk.Label(window, text="Clave:", font=("Arial", 11, "bold"))
    lbl_cveGru.grid(row=1, column=0, padx=10, pady=5)

    lbl_nomGru = tk.Label(window, text="Nombre:", font=("Arial", 11, "bold"))
    lbl_nomGru.grid(row=2, column=0, padx=10, pady=5)

    txt_cveGru = tk.Entry(window, width=20, font=("Arial",12))
    txt_cveGru.grid(row=1, column=1)

    txt_nomGru = tk.Entry(window, width=20, font=("Arial",12))
    txt_nomGru.grid(row=2, column=1)

    # Entradas de texto
    if (clave != "" and nombre == ""):
        txt_cveGru.insert(0, clave)
    elif (clave == "" and nombre != ""):
        txt_nomGru.insert(0, nombre)
    elif (clave != "" and nombre != ""):
        txt_cveGru.insert(0, clave)
        txt_nomGru.insert(0, nombre)

    def EliminarGrupo():
        if (txt_cveGru != "" and txt_nomGru == ""):
            grupos.delete_one({"cveGru": txt_cveGru})
            print("\nGrupo con clave " + txt_cveGru + " eliminado.")
        elif (txt_cveGru == "" and txt_nomGru != ""):
            grupos.delete_one({"nomGru": txt_nomGru})
            print("\nGrupo con nombre " + txt_nomGru + " eliminado.")
        else:
            grupos.delete_one({"$and": [{"cveGru": txt_cveGru}, {"nomGru": txt_nomGru}]})
            print("\nGrupo " + txt_nomGru + " con clave " + txt_cveGru + " eliminado.")
        confirmacion.destroy()

    btn_confirmar = tk.Button(confirmacion, text="Aceptar", font=("Arial", 12, "bold"), bg="white", fg="black", command=EliminarGrupo)
    btn_confirmar.pack(side=tk.RIGHT, padx=35)

    btn_cancelar = tk.Button(confirmacion, text="Cancelar", font=("Arial", 12, "bold"), bg="white", fg="black", command=confirmacion.destroy)
    btn_cancelar.pack(side=tk.LEFT, padx=35)


# Configuración de la ventana
window = tk.Tk()
window.title("Agregar Grupo")
window.geometry("600x400")
window.resizable(0, 0)
window.config(cursor="hand2")

# Etiquetas
lbl_Bienvenido = tk.Label(window, text="Bienvenido(a)", font=("Arial", 11))
lbl_Bienvenido.grid(row=0, column=0, padx=10, pady=10)

lbl_cveGru = tk.Label(window, text="Clave:", font=("Arial", 11, "bold"))
lbl_cveGru.grid(row=1, column=0, padx=10, pady=5)

lbl_nomGru = tk.Label(window, text="Nombre:", font=("Arial", 11, "bold"))
lbl_nomGru.grid(row=2, column=0, padx=10, pady=5)

# Entradas de texto
txt_cveGru = tk.Entry(window, width=20, font=("Arial",12))
txt_cveGru.grid(row=1, column=1)

txt_nomGru = tk.Entry(window, width=20, font=("Arial",12))
txt_nomGru.grid(row=2, column=1)

# Botón para buscar grupo
btn_buscar = tk.Button(window, text="Buscar", font=("Arial", 12, "bold"), bg="white", fg="black", command=Buscar)
btn_buscar.grid(row=1, column=3, pady=10, padx=20)

# Botón para agregar grupo
btn_agregar = tk.Button(window, text="Agregar", font=("Arial", 12, "bold"), bg="white", fg="black", command=Agregar)
btn_agregar.grid(row=2, column=3, pady=10, padx=20)

# Botón para limpiar cajas de texto
btn_limpiar = tk.Button(window, text="Limpiar", font=("Arial", 12, "bold"), bg="white", fg="black", command=Limpiar)
btn_limpiar.grid(row=1, column=4, pady=10)

# Botón para eliminar grupo
btn_eliminar = tk.Button(window, text="Eliminar", font=("Arial", 12, "bold"), bg="white", fg="black", command=Eliminar)
btn_eliminar.grid(row=2, column=4, pady=10)

# Botón para actualizar grupo
btn_actualizar = tk.Button(window, text="Actualizar", font=("Arial", 12, "bold"), bg="white", fg="black", command=Actualizar)
btn_actualizar.grid(row=2, column=4, pady=10)

window.mainloop()