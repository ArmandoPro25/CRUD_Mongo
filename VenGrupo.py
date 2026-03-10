import tkinter as tk
from tkinter import filedialog as fd
import subprocess
from pymongo import MongoClient as MC
import MongoXML as xml

# Cadena de conexión local a MongoDB
client = MC("mongodb://localhost:27017/")
db = client["BD_GrupoAlumno"]
grupos = db["Grupo"]

# Funcion para limpiar cadenas de texto
def Limpiar():
    txt_cveGru.delete(0, tk.END)
    txt_nomGru.delete(0, tk.END)
    txt_resultados.delete(1.0, tk.END)

# Funcion para buscar grupos
def Buscar():
    if txt_cveGru.get() == "" and txt_nomGru.get() == "":
        LimpiarValidacion()
        resultado = list(grupos.find())
        if not resultado:
            Validacion("No hay grupos registrados.", "green")
        else:
            for grupo in resultado:
                Validacion(f"Clave: {grupo['cveGru']}\nNombre: {grupo['nomGru']}\n\n", "black")
    elif txt_cveGru.get() != "" and txt_nomGru.get() == "":
        LimpiarValidacion()
        resultado = list(grupos.find({"cveGru":txt_cveGru.get()}))
        if not resultado:
            Validacion(f"No se encontraron resultados para la clave {txt_cveGru.get()}.", "green")
        else:
            for grupo in resultado:
                Validacion(f"Clave: {grupo['cveGru']}\nNombre: {grupo['nomGru']}\n\n", "black")
    elif txt_cveGru.get() == "" and txt_nomGru.get() != "":
        LimpiarValidacion()
        resultado = list(grupos.find({"nomGru":txt_nomGru.get()}))
        if not resultado:
            Validacion(f"No se encontraron resultados para el nombre {txt_nomGru.get()}.", "green")
        else:
            for grupo in resultado:
                Validacion(f"Clave: {grupo['cveGru']}\nNombre: {grupo['nomGru']}\n\n", "black")
    elif txt_cveGru.get() != "" and txt_nomGru.get() != "":
        LimpiarValidacion()
        resultado = list(grupos.find({"$and": [{"cveGru": txt_cveGru.get()}, {"nomGru": txt_nomGru.get()}]}))
        if not resultado:
            Validacion(f"No se encontraron resultados para el grupo {txt_nomGru.get()} con clave {txt_cveGru.get()}.", "green")
        else:
            for grupo in resultado:
                Validacion(f"Clave: {grupo['cveGru']}\nNombre: {grupo['nomGru']}\n\n", "black")
    else:
        LimpiarValidacion()
        Validacion("No se encontraron resultados con la clave y el nombre\nproporcionados.", "green")

def Agregar():
    cve = txt_cveGru.get().strip()
    nom = txt_nomGru.get().strip()

    if cve == "" and nom == "":
        LimpiarValidacion()
        Validacion("Ingrese la clave o el nombre del grupo a agregar", "red")
    elif cve != "" and nom == "":
        LimpiarValidacion()
        Validacion("Ingrese el nombre del grupo a agregar", "red")
    elif cve == "" and nom != "":
        LimpiarValidacion()
        Validacion("Ingrese la clave del grupo a agregar", "red")
    elif len(cve) > 7:
        LimpiarValidacion()
        Validacion("La clave del grupo no debe exceder los 7 caracteres.", "red")
    elif len(nom) > 15:
        LimpiarValidacion()
        Validacion("El nombre del grupo no debe exceder los 15 caracteres.", "red")
    elif grupos.find_one({"cveGru": cve}):
        LimpiarValidacion()
        Validacion(f"La clave {cve} ya existe.", "red")
    else:
        grupos.insert_one({"cveGru": cve, "nomGru": nom})
        LimpiarValidacion()
        Validacion(f"Grupo {nom} insertado.", "green")

def Eliminar():
    if txt_cveGru.get() == "" and txt_nomGru.get() == "":
        LimpiarValidacion()
        Validacion("Ingrese la clave o el nombre del grupo a eliminar", "red")
    elif txt_cveGru.get() != "" and txt_nomGru.get() == "":
        LimpiarValidacion()
        resultado = list(grupos.find({"cveGru":txt_cveGru.get()}))
        if not resultado:
            Validacion(f"No se encontraron resultados para la clave {txt_cveGru.get()}.", "green")
        else:
            ConfirmarEliminacion(txt_cveGru.get(), "")
    elif txt_cveGru.get() == "" and txt_nomGru.get() != "":
        LimpiarValidacion()
        resultado = list(grupos.find({"nomGru":txt_nomGru.get()}))
        if not resultado:
            Validacion(f"No se encontraron resultados para el grupo con nombre {txt_nomGru.get()}.", "green")
        else:
            ConfirmarEliminacion("", txt_nomGru.get())
    elif txt_cveGru.get() != "" and txt_nomGru.get() != "":
        LimpiarValidacion()
        resultado = list(grupos.find({"$and": [{"cveGru": txt_cveGru.get()}, {"nomGru": txt_nomGru.get()}]}))
        if not resultado:
            Validacion(f"No se encontraron resultados para el grupo {txt_nomGru.get()} con clave {txt_cveGru.get()}.", "green")
        else:
            ConfirmarEliminacion(txt_cveGru.get(), txt_nomGru.get())
    else:
        LimpiarValidacion()
        Validacion("No se encontraron resultados con la clave y el nombre\nproporcionados.", "green")

def Actualizar():
    cve = txt_cveGru.get().strip()
    nom = txt_nomGru.get().strip()

    if cve == "" and nom == "":
        LimpiarValidacion()
        Validacion("Ingrese la clave o el nombre del grupo a actualizar", "red")
    elif cve != "" and nom == "":
        LimpiarValidacion()
        resultado = list(grupos.find({"cveGru":cve}))
        if not resultado:
            Validacion(f"No se encontraron resultados para la clave {cve}.", "green")
        else:
            ActualizarForm(cve, "")        
    elif cve == "" and nom != "":
        LimpiarValidacion()
        resultado = list(grupos.find({"nomGru":nom}))
        if not resultado:
            Validacion(f"No se encontraron resultados para el grupo con nombre {nom}.", "green")
        else:
            ActualizarForm("", nom)        
    elif cve != "" and nom != "":
        LimpiarValidacion()
        resultado = list(grupos.find({"$and": [{"cveGru": cve}, {"nomGru": nom}]}))
        if not resultado:
            Validacion(f"No se encontraron resultados para el grupo {nom} con clave {cve}.", "green")
        else:
            ActualizarForm(cve, nom)
    else:
        LimpiarValidacion()
        Validacion("No se encontraron resultados con la clave y el nombre\nproporcionados.", "green")

# Configuración de ventana emergente para eliminar
def ConfirmarEliminacion(txt_cveGru, txt_nomGru):
    confirmacion = tk.Toplevel(window)
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
        if txt_cveGru != "" and txt_nomGru == "":
            grupos.delete_one({"cveGru": txt_cveGru})
            LimpiarValidacion()
            Validacion(f"Grupo con clave {txt_cveGru} eliminado", "green")
        elif txt_cveGru == "" and txt_nomGru != "":
            grupos.delete_one({"nomGru": txt_nomGru})
            LimpiarValidacion()
            Validacion(f"Grupo con nombre {txt_nomGru} eliminado", "green")
        else:
            grupos.delete_one({"$and": [{"cveGru": txt_cveGru}, {"nomGru": txt_nomGru}]})
            LimpiarValidacion()
            Validacion(f"Grupo {txt_nomGru} con clave {txt_cveGru} eliminado.", "green")
        confirmacion.destroy()

    btn_confirmar = tk.Button(confirmacion, text="Eliminar", font=("Arial", 12, "bold"), bg="white", fg="black", command=EliminarGrupo)
    btn_confirmar.pack(side=tk.RIGHT, padx=35, pady=10)

    btn_cancelar = tk.Button(confirmacion, text="Cancelar", font=("Arial", 12, "bold"), bg="white", fg="black", command=confirmacion.destroy)
    btn_cancelar.pack(side=tk.LEFT, padx=35, pady=10)

# Configuración de ventana emergente para actualizar
def ActualizarForm(clave, nombre):
    actualizacion = tk.Toplevel(window)
    actualizacion.title("Actualizar Grupo")
    actualizacion.geometry("320x180")
    actualizacion.resizable(0, 0)
    actualizacion.config(cursor="hand2")

    # Etiquetas
    act_cveGru = tk.Label(actualizacion, text="Clave:", font=("Arial", 11, "bold"))
    act_cveGru.grid(row=1, column=0, padx=10, pady=5)

    act_nomGru = tk.Label(actualizacion, text="Nombre:", font=("Arial", 11, "bold"))
    act_nomGru.grid(row=2, column=0, padx=10, pady=5)

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
            existente = grupos.find_one({"cveGru": nueva_cve})
            if existente and existente["cveGru"] != clave:
                lbl_Validacion.config(text=f"La clave {nueva_cve} ya pertenece a otro grupo.", fg="red")
                return

            if clave != "" and nombre == "":
                grupos.update_one({"cveGru": clave}, {"$set": {"cveGru": nueva_cve, "nomGru": nuevo_nom}})
            elif clave == "" and nombre != "":
                grupos.update_one({"nomGru": nombre}, {"$set": {"cveGru": nueva_cve, "nomGru": nuevo_nom}})
            elif clave != "" and nombre != "":
                grupos.update_one({"cveGru": clave, "nomGru": nombre}, {"$set": {"cveGru": nueva_cve, "nomGru": nuevo_nom}})

            actualizacion.destroy()
            LimpiarValidacion()
            Validacion(f"Se actualizó el grupo {nueva_cve}", "green")

    btn_noAct = tk.Button(actualizacion, text="Cancelar", font=("Arial", 12, "bold"), bg="white", fg="black", command=actualizacion.destroy)
    btn_noAct.grid(row=4, column=0, padx=15, pady=10)
    
    btn_act = tk.Button(actualizacion, text="Actualizar", font=("Arial", 12, "bold"), bg="white", fg="black", command=ActualizarGrupo)
    btn_act.grid(row=4, column=1, padx=15, pady=10)

def Purgar():
    grupos.delete_many({})
    LimpiarValidacion()
    Validacion("Se eliminaron TODOS los grupos.", "red")

def Importar():
    formatos = {
        "JSON": ("*.json","json"),
        "CSV": ("*.csv","csv")
    }
    formato = imp.get()

    if formato == "XML":
        archImport = fd.askopenfilename(
            title="Seleccionar archivo",
            filetypes=[("Archivos XML","*.xml")]
        )

        if archImport:
            xml.importarXML(archImport)
            LimpiarValidacion()
            Validacion("Restauración XML importada correctamente.\n","green")

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
                LimpiarValidacion()
                Validacion("Restauración importada correctamente.\n","green")

            except Exception as e:
                LimpiarValidacion()
                Validacion(f"Error al importar:\n{e}","red")

def Exportar():
    formatos = {
        "JSON": ("*.json", "json"),
        "CSV": ("*.csv", "csv")
    }
    formato = exp.get()

    if formato == "XML":
        archExport = fd.asksaveasfilename(
            title="Guardar archivo",
            defaultextension=".xml",
            filetypes=[("Archivos XML","*.xml")]
        )

        if archExport:
            xml.exportarXML(archExport)
            LimpiarValidacion()
            Validacion("Backup XML exportado correctamente.\n", "green")

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
                LimpiarValidacion()
                Validacion("Backup exportado correctamente.\n", "green")

            except Exception as e:
                LimpiarValidacion()
                Validacion(f"Error al exportar:\n{e}", "red")

def Validacion(validacion, alert):
    if validacion != "":
        txt_resultados.tag_config("color", foreground=alert)  
        txt_resultados.insert(tk.END, validacion, "color")

def LimpiarValidacion():
    txt_resultados.delete(1.0, tk.END)

# Configuración de la ventana
window = tk.Tk()
window.title("Agregar Grupo")
window.geometry("800x400")
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
btn_buscar = tk.Button(window, text=" Buscar ", font=("Arial", 12, "bold"), bg="white", fg="black", command=Buscar)
btn_buscar.grid(row=1, column=3, pady=10, padx=10)

# Botón para agregar grupo
btn_agregar = tk.Button(window, text="Agregar ", font=("Arial", 12, "bold"), bg="white", fg="black", command=Agregar)
btn_agregar.grid(row=2, column=3, pady=10, padx=10)

# Botón para limpiar cajas de texto
btn_limpiar = tk.Button(window, text="  Limpiar  ", font=("Arial", 12, "bold"), bg="white", fg="black", command=Limpiar)
btn_limpiar.grid(row=1, column=4, pady=10, padx=10)

# Botón para eliminar grupo
btn_eliminar = tk.Button(window, text="Eliminar", font=("Arial", 12, "bold"), bg="white", fg="black", command=Eliminar)
btn_eliminar.grid(row=1, column=5, pady=10, padx=10)

# Botón para eliminar todos los registros
btn_purgar = tk.Button(window, text=" Purgar ", font=("Arial", 12, "bold"), bg="white", fg="black", command=Purgar)
btn_purgar.grid(row=2, column=5, pady=10, padx=10)

# Botón para actualizar grupo
btn_actualizar = tk.Button(window, text="Actualizar", font=("Arial", 12, "bold"), bg="white", fg="black", command=Actualizar)
btn_actualizar.grid(row=2, column=4, pady=10, padx=10)

# Botón para importar (Restore)
btn_importar = tk.Button(window, text="Importar", font=("Arial", 12, "bold"), bg="white", fg="black", command=Importar)
btn_importar.grid(row=1, column=7, pady=10, padx=10)

# Botón para exportar (Backup)
btn_exportar = tk.Button(window, text="Exportar", font=("Arial", 12, "bold"), bg="white", fg="black", command=Exportar)
btn_exportar.grid(row=2, column=7, pady=10, padx=10)

# Texto para mostrar resultados
txt_resultados = tk.Text(window, width=70, height=10)
txt_resultados.grid(row=3, column=0, columnspan=6, padx=10, pady=10)

# Lista de importación
imp = tk.StringVar()
imp.set("JSON")
opciones = ["JSON", "CSV", "XML"]
impList = tk.OptionMenu(window, imp, *opciones)
impList.grid(row=1, column=6, pady=10, padx=10)

# Lista de exportación
exp = tk.StringVar()
exp.set("JSON")
opciones = ["JSON", "CSV", "XML"]
expList = tk.OptionMenu(window, exp, *opciones)
expList.grid(row=2, column=6, pady=10, padx=10)

window.mainloop()