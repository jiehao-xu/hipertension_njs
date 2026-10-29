

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
	"pactivos",			# Will be done by Samu
	"dosis",			# DONE
	"estado_aut",		# DONE
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

def split_active_ingredients(values):
	result = []

	for value in values:
		if pd.isna(value):
			result.append([])
			continue

		ingredients = []

		for ingredient in str(value).split(","):
			ingredient = ingredient.strip()

			if ingredient:
				ingredients.append(ingredient)

		result.append(ingredients)

	return result

def clean_pactivos(df):
	active_ingredients = split_active_ingredients(df["pactivos"])
	unique_ingredient_names = []

	# Se crea una lista de nombres de ingredientes activos únicos
	for ingredients in active_ingredients:
		for ingredient in ingredients:
			if ingredient not in unique_ingredient_names:
				unique_ingredient_names.append(ingredient)

	# Para cada ingrediente activo único, se crea una nueva columna en el DataFrame
	for ingredient in unique_ingredient_names:
		column_name = f"pactivo_{ingredient}"
		values = []
		# Se recorre la lista de listas de ingredientes activos y se asigna 1 si el ingrediente está presente, 0 si no lo está
		for ingredients in active_ingredients:
			if ingredient in ingredients:
				values.append(1)
			else:
				values.append(0)

		df[column_name] = values

	return df


def clean_dosis(dosis):
	d = re.search(r"^(\d|,)+", dosis).group()
	return d.replace(",", ".")

def clean_estadoAut(estado_aut):
	year = int(estado_aut.split("/")[2])
	if year <= 26:
		year += 2000
	else:
		year += 1900
	return year

def clean_tratamiento(df):
	df.replace("SI", 1, inplace=True)
	df.replace("NO", 0, inplace=True)
	return df.fillna(0)
	

def clean(df):
	df.drop(columns=delete, inplace=True)
	df.drop(columns=identifier, inplace=True)
	df["dosis"] = df["dosis"].apply(clean_dosis)
	df["estado_aut"] = df["estado_aut"].apply(clean_estadoAut)
	df["Tratamiento de larga duración"] = clean_tratamiento(df["Tratamiento de larga duración"])

	# OneHot Encoding
	df = pd.get_dummies(df, columns=['forma_farmaceutica_simplificada', 'vias_administracion', 'Estado'], drop_first=True, dtype=int)

	df = clean_pactivos(df)
	df.drop(columns="pactivos", inplace=True)

	df.to_csv("data/raw/medicamentosHU4.csv")






if __name__ == "__main__":
	df = pd.read_excel("data/raw/medicamentosHU3.xlsx")
	clean(df)