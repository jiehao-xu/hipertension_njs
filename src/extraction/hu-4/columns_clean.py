from pathlib import Path

import pandas as pd


# PROJECT_ROOT = Path(__file__).resolve().parents[3]
# input_path = Path("data/raw/medicamentosHU3.xlsx")
# output_path = Path("data/raw/medicamentosHU3_clean.xlsx")


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




def pactivos_cleaning(input_path="data/raw/medicamentosHU3.xlsx", output_path: str = "data/medicamentosHU3_cleaned.xlsx") -> None:
    df = pd.read_excel(input_path)

    if "pactivos" not in df.columns:
        raise ValueError(f"La columna 'pactivos' no existe en {input_path}")

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

    df.to_excel(output_path, index=False)
    print(f"Archivo creado: {output_path}")


# pactivos_cleaning(input_path="data/raw/medicamentosHU3.xlsx", output_path="data/raw/medicamentosHU3_cleaned.xlsx")