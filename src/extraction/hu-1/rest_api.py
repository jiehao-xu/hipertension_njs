import requests
import json
import pandas as pd
import openpyxl
from pathlib import Path
import numpy as np

# --- Obtención de lista medicamentos ---

# url a la que queremos acceder
url_ficha_tecnica = "https://cima.aemps.es/cima/rest/buscarEnFichaTecnica?pagina=1"

# settings del payload para obtener los nregistro de los medicamentos asociados a nuestra enfermedad
payload = json.dumps([
  {
    "seccion": "4.1",
    "texto": "Hipertensión",
    "contiene": 1
  }
])
headers = {
  'Cookie': 'JSESSIONID=jJHKTa7yffeRKOMGXBJNtxxaZfjpYRMpe64PZucCEpS8Ud6tKa4Y!962100432',
  'Content-Type': 'application/json'
}

response = requests.request("POST", url_ficha_tecnica, headers=headers, data=payload)

lista_medicamentos = response.json()

nregistros = []
for resultado in lista_medicamentos["resultados"]:
    nregistros.append(resultado["nregistro"])


medicamentos = []
for nregistro in nregistros:

    # Con el nregistro accedemos a las caracteristicas del medicamento
    url_medicamento = f"https://cima.aemps.es/cima/rest/medicamento?nregistro={nregistro}"

    payload = {}
    headers = {
    'Cookie': 'JSESSIONID=csLKX9bGs_bTIPE2h352j3KQwKQVEdchKAGQP1ixe8iHI5K7LZEL!962100432'
    }

    response = requests.request("GET", url_medicamento, headers=headers, data=payload)
    medicamento = response.json()

    # Primer Código Nacional disponible
    presentaciones = medicamento.get("presentaciones", [])
    cn = presentaciones[0].get("cn") if presentaciones else None

    # Vías de administración
    vias = [
        via.get("nombre")
        for via in medicamento.get("viasAdministracion", [])
    ]

    # URL HTML de la ficha técnica
    url_html_ficha = None

    for doc in medicamento.get("docs", []):
        if doc.get("tipo") == 1:
            url_html_ficha = doc.get("urlHtml")
            break

    # Foto de materiales
    url_foto_materiales = None

    for foto in medicamento.get("fotos", []):
        if "material" in foto.get("tipo", "").lower():
            url_foto_materiales = foto.get("url")
            break

    datos = {
        "nregistro": medicamento.get("nregistro"),
        "nombre": medicamento.get("nombre"),
        "pactivos": medicamento.get("pactivos"),
        "labtitular": medicamento.get("labtitular"),
        "labcomercializador": medicamento.get("labcomercializador"),

        "cn": cn,

        "dosis": medicamento.get("dosis"),

        "forma_farmaceutica_simplificada":
            medicamento.get("formaFarmaceuticaSimplificada", {}).get("nombre"),

        "estado_aut":
            medicamento.get("estado", {}).get("aut"),

        "estado_rev":
            (medicamento.get("estado") or {}).get("rev", np.nan),

        "vias_administracion": vias,

        "comercializado": int(medicamento.get("comerc", False)),
        "requiere_receta": int(medicamento.get("receta", False)),
        "generico": int(medicamento.get("generico", False)),
        "afecta_conduccion": int(medicamento.get("conduc", False)),
        "triangulo_negro": int(medicamento.get("triangulo", False)),
        "medicamento_huerfano": int(medicamento.get("huerfano", False)),
        "biosimilar": int(medicamento.get("biosimilar", False)),

        "url_html_ficha_tecnica": url_html_ficha,
        "url_foto_materiales": url_foto_materiales,

        "num_registros_atc":
            len(medicamento.get("atcs", [])),

        "num_principios_activos":
            len(medicamento.get("principiosActivos", [])),

        "num_excipientes":
            len(medicamento.get("excipientes", []))
    }

    medicamentos.append(datos)


df = pd.DataFrame(medicamentos)
print(df)

# Ejecutar desde la raíz del proyecto
output_path = Path("data/raw/medicamentos.xlsx")
output_path.parent.mkdir(parents=True, exist_ok=True)
df.to_excel(output_path, index=False)


   
