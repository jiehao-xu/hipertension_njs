from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[3]
input_path = Path("data/raw/medicamentosHU3.xlsx")
output_path = Path("data/raw/medicamentosHU3_clean.xlsx")


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


def main() -> None:
    df = pd.read_excel(input_path)

    if "pactivos" not in df.columns:
        raise ValueError(f"La columna 'pactivos' no existe en {input_path}")

    active_ingredients = split_active_ingredients(df["pactivos"])
    ingredient_names = []

    for ingredients in active_ingredients:
        for ingredient in ingredients:
            if ingredient not in ingredient_names:
                ingredient_names.append(ingredient)

    for ingredient in ingredient_names:
        column_name = f"pactivo_{ingredient}"
        values = []

        for ingredients in active_ingredients:
            if ingredient in ingredients:
                values.append(1)
            else:
                values.append(0)

        df[column_name] = values

    df.to_excel(output_path, index=False)
    print(f"Archivo creado: {output_path}")


if __name__ == "__main__":
    main()