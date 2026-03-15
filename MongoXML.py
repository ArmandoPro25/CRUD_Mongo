import xml.etree.ElementTree as ET
from pymongo import MongoClient as MC

# Cadena de conexión local a MongoDB
client = MC("mongodb://localhost:27017/")
db = client["BD_GrupoAlumno"]
grupos = db["Grupo"]
alumnos = db["Alumno"]
# Función para Exportar en XML
def exportarXML(ruta):
    datos = list(grupos.find({}, {"_id":0}))
    root = ET.Element("grupos")

    for grupo in datos:
        g = ET.SubElement(root, "grupo")
        cve = ET.SubElement(g, "cveGru")
        cve.text = grupo["cveGru"]

        nom = ET.SubElement(g, "nomGru")
        nom.text = grupo["nomGru"]

    tree = ET.ElementTree(root)
    tree.write(ruta, encoding="utf-8", xml_declaration=True)

# Función para importar en XML
def importarXML(ruta):
    tree = ET.parse(ruta)
    root = tree.getroot()
    grupos.delete_many({})

    for g in root.findall("grupo"):
        cve = g.find("cveGru").text
        nom = g.find("nomGru").text

        grupos.insert_one({
            "cveGru": cve,
            "nomGru": nom
        })


def exportarXMLAlumnos(ruta):
    datos = list(alumnos.find({}, {"_id":0}))
    root = ET.Element("alumnos")

    for alumno in datos:
        a = ET.SubElement(root, "alumno")
        cve = ET.SubElement(a, "cveAlu")
        cve.text = alumno["cveAlu"]

        nom = ET.SubElement(a, "nomAlu")
        nom.text = alumno["nomAlu"]

        eda = ET.SubElement(a, "edaAlu")
        eda.text = str(alumno.get("edaAlu", ""))

        gru = ET.SubElement(a, "cveGru")
        gru.text = alumno.get("cveGru", "")

    tree = ET.ElementTree(root)
    tree.write(ruta, encoding="utf-8", xml_declaration=True)

def importarXMLAlumnos(ruta):
    tree = ET.parse(ruta)
    root = tree.getroot()
    alumnos.delete_many({})

    for a in root.findall("alumno"):
        cve = a.find("cveAlu").text
        nom = a.find("nomAlu").text
        eda = int(a.find("edaAlu").text) if a.find("edaAlu").text else 0
        gru = a.find("cveGru").text

        alumnos.insert_one({
            "cveAlu": cve,
            "nomAlu": nom,
            "edaAlu": eda,
            "cveGru": gru
        })
