

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
	"estado_aut",
	"comercializado",
	"requiere_receta",
	"generico",
	"afecta_conduccion",
	"triangulo_negro",
	"medicamento_huerfano",
	"biosimilar",
	"num_registros_atc",
	"num_principios_activos",
	"num_excipientes",
	"num_palabras4.4",
	"num_tablas",
	"indicador_riesgo_grave",
	"Precio venta al público con IVA"
}

work = {
	"pactivos",
	"dosis"
}

short_groups = {
	"forma_farmaceutica_simplificada",
	"vias_administracion",
	"Estado",
	"Tratamiento de larga duración",
	"Especial control médico"
}

long_groups = {
	"labtitular"
}

delete = {
	"estado_rev",
	"labcomercializador",
	"Precio de referencia"
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