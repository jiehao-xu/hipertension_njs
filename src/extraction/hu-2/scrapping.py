import requests
import pandas as pd
from bs4 import BeautifulSoup


# url = "https://cima.aemps.es/cima/dochtml/ft/59082/FT_59082.html"


# Leer excel
medicamentos = pd.read_excel("./data/raw/medicamentos.xlsx")


# Columnas resultados
medicamentos["num_palabras4.4"] = 0
medicamentos["num_tablas"] = 0
medicamentos["indicador_riesgo_grave"] = 0

# Identificador, para que el servidor no nos bloquee por ser un bot
headers = {
 "User-Agent": "EducationalScraper/1.0"
}

for index, medicamento in medicamentos.iterrows():
    url = medicamento["url_html_ficha_tecnica"]

    # Saltar medicamentos sin URL
    if pd.isna(url) or not str(url).strip():
        continue        

    response = requests.get(url, headers=headers, timeout=30)

    response.raise_for_status() # raises on 4xx or 5xx

    if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")

            # SECCION 4.4
            section4_4 = soup.find("h2", id="4.4")
            if section4_4:
                # Get the next elements until the next h2
                content = []
                for element in section4_4.find_next_siblings():
                    if element.name == "h2":
                        break
                    content.append(element.get_text())
                
                text_content = " ".join(content)
                word_count = len(text_content.split())

                # Guardar el numero de palabras en el dataframe
                medicamentos.at[index, "num_palabras4.4"] = word_count

            else:
                print(f"Section 4.4 not found for URL: {url}")


            # NUMERO TABLAS
            tables = soup.find_all("table")
            num_tablas = len(tables)
            medicamentos.at[index, "num_tablas"] = num_tablas



            # NUMERO INDICADORES DE RIESGO GRAVE
            text = soup.get_text(" ", strip=True)
            risk_indicator_count = text.lower().count("grave")
            medicamentos.at[index, "indicador_riesgo_grave"] = risk_indicator_count



            # Guardar resultados
            # print(f"  Palabras 4.4: {word_count}" f" | Tablas: {num_tablas}" f" | 'grave': {risk_indicator_count}")

        
    # Guardar solo una vez al terminar
    medicamentos.to_excel(
        "./data/raw/medicamentosHU2.xlsx",
        index=False
    )





# for url in lista_urls:
#     # Download the page; stop waiting after 30 seconds
#     response = requests.get(url, headers=headers, timeout=30)

#     # print(f"Status code: {response.status_code}")
#     # print(f"Content type: {type(response.content)}") 
#     # print(f"First 200 bytes: {response.content[:200]}")
#     # print(f"Content: {response.text}")
#     # print(f"Headers: {response.headers}")
#     # print(f"Encoding: {response.encoding}")

#     response.raise_for_status() # raises on 4xx or 5xx

#     # If the request was successful, count how many words are in the 4.4 section of the page
#     if response.status_code == 200:
#         soup = BeautifulSoup(response.content, "html.parser")

#         # Count words in section 4.4
#         # Find the h2 element with id="4.4"
#         section_4_4 = soup.find("h2", id="4.4")
#         if section_4_4:
#             # Get the next elements until the next h2
#             content = []
#             for element in section_4_4.find_next_siblings():
#                 if element.name == "h2":
#                     break
#                 content.append(element.get_text())
            
#             # Join the content and count words
#             text_content = " ".join(content)
#             word_count = len(text_content.split())
#             # print(f"Word count in section 4.4: {word_count}")
            

#             # Count how many table etiq are in the whole page
#             tables = soup.find_all("table")



#             # Count the number of severe risk indicators in the whole page
#             text = soup.get_text(" ", strip=True)
#             risk_indicator_count = text.lower().count("grave")


#             # Add word count (4.4), table count and risk indicator to a copy of the xlsx file
#             medicamento = pd.read_excel("./data/raw/medicamentos.xlsx", encoding="utf-8")
#             medicamento["num_palabras4.4"] = word_count
#             medicamento["num_tablas"] = len(tables)
#             medicamento["indicador_riesgo_grave"] = risk_indicator_count
#             medicamento.to_excel("./data/raw/medicamentosHU2.xlsx", index=False)

#             # print(f"Content of section 4.4: {text_content}[-100:]")  # Print last 100 characters of the content
        
#         else:
#             print("Section 4.4 not found in the page.")

#     else:
#         print("URL not found or request failed. Status code:", response.status_code)