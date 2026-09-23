import requests
import pandas as pd
from io import StringIO		# Transform text into file-like

XLSX_FILE = "../../../data/raw/medicamentos.xlsx"

def downloadCNlist(cn_list):

	original_df = pd.DataFrame()

	for cn in cn_list:
		url = f'https://www.sanidad.gob.es/profesionales/nomenclator.do?6578706f7274=1&codnacional={cn}&metodo=buscarProductos&priact_cuatro=&d-4015021-e=1&buscar=Buscar'
		payload = {}
		headers = {}
		print(f'Download CN {cn}')
		response = requests.request("GET", url, headers=headers, data=payload)
		response_csv = StringIO(response.text)
		try:
			df = pd.read_csv(response_csv)
			original_df = pd.concat([original_df, df], ignore_index=True)
		except pd.errors.EmptyDataError:
			print("[X] ERROR: Empty row")
	
	return original_df

def readXLSX(file):
	print("[*] Reading file...")
	df = pd.read_excel(file)
	print(f'[+] Readed. DF size: {df.shape}')
	return df
	

original_df = readXLSX(XLSX_FILE)
cn_df = original_df["cn"]

df = downloadCNlist(cn_df)

cleaned_df = df[["Código Nacional", "Estado", "Precio venta al público con IVA", "Precio de referencia", "Tratamiento de larga duración", "Especial control médico"]]
cleaned_df.to_csv("export.csv")



