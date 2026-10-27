

import pandas as pd
import re

identifier = {
	"nregistro",
	"nombre",
	"cn",
	"url_html_ficha_tecnica",
	"url_foto_materiales"
}

predictors = {
	"comercializado",
	"requiere_receta",
	"generico",
	"afecta_conduccion",
	"triangulo_negro",
	"medicamento_huerfano",
	"biosimilar",
	"num_principios_activos",
	"num_excipientes",
	"num_palabras4.4",
	"num_tablas",
	"indicador_riesgo_grave",
	"Precio venta al público con IVA",
	"Tratamiento de larga duración"
}

work = {
	"pactivos",
	"dosis",
	"estado_aut",
	"estado_rep"		# If there is a value 1, if not 0
}

short_groups = {
	"forma_farmaceutica_simplificada",
	"vias_administracion",
	"Estado"
}

long_groups = {
	"labtitular"
}

delete = {
	"estado_rev",
	"labcomercializador",
	"Precio de referencia",
	"num_registros_atc",
	"Especial control médico"
}

def clean_dosis(dosis):
	return re.search(r"^(\d|,)+", dosis).group()

def clean(df):
	df.drop(columns=delete, inplace=True)
	df.drop(columns=identifier, inplace=True)
	df["dosis"] = df["dosis"].apply(clean_dosis)
	df.to_excel("data/raw/medicamentosHU4.xlsx")






if __name__ == "__main__":
	df = pd.read_excel("data/raw/medicamentosHU3.xlsx")
	clean(df)