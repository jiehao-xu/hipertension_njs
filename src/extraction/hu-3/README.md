# Downloading medicine data from the Ministry of Health (sanidad.gob.es)

This script enriches the medicine dataset produced in the previous step (HU-2) with data from the Ministry of Health's webpage, using each medicine's National Code (`cn`) as the lookup key.

The goal is to add pricing and dispensing attributes (status, retail price, reference price, long-term treatment and special medical control) for use in later analysis.

## Location

The script is located in:

```text
src/extraction/hu-3/
```

The expected input file is:

```text
data/raw/medicamentosHU2.xlsx
```

And the result is saved to:

```text
data/raw/medicamentosHU3.xlsx
```

## Requirements

The script uses the following libraries:

```text
requests
pandas
io
```

If any of them is missing, it can be installed with:

```bash
uv pip install requests pandas openpyxl
```

`io` is required to generate the dataframe from a CSV-string-style result

## Input file

The file:

```text
data/raw/medicamentosHU2.xlsx
```

is the output of the HU-2 scraping step and must contain a column named:

```text
cn
```

This column holds the National Code (`cn`) of each medicine.

## How it works

1. Reads `medicamentosHU2.xlsx` into a DataFrame.

2. Takes the `cn` column as the list of codes to query.

3. For each CN, sends a `GET` request to the web search endpoint:

```text
https://www.sanidad.gob.es/profesionales/nomenclator.do?6578706f7274=1&codnacional={cn}&metodo=buscarProductos&priact_cuatro=&d-4015021-e=1&buscar=Buscar
```

The website returns a CSV containing a row for the requested medication. Although the complete CSV could have been downloaded from the website, this method was chosen to avoid downloading unnecessary rows for the medications that are not wanted. In this way, it is ensured that only the necessary medications are downloaded.

4. Wraps the response text in a `StringIO` object so it can be read as a file, and parses it with `pd.read_csv`.

5. If the response is empty (no product found for that CN), it prints:

```text
[X] ERROR [cn = ...]: Empty row
```

   and continues with the next code.

6. Concatenates all the individual results into a single DataFrame.

7. Keeps only the relevant columns and renames `Código Nacional` to `cn`.

8. Performs a left join with the original DataFrame on `cn`. This retains all the medications that appeared in the original XLSX file, even if the search yielded no results for them. In that case, no value is saved in the XLSX file; instead, null/empty values ​​are recorded.

9. Saves the result to:

```text
data/raw/medicamentosHU3.xlsx
```

## Generated variables

Five columns are added to the original file, taken as-is from the export.


## Result

Once finished, the following file is generated:

```text
data/raw/medicamentosHU3.xlsx
```

It keeps all the original columns of `medicamentosHU2.xlsx` and adds:

```text
Estado
Precio venta al público con IVA
Precio de referencia
Tratamiento de larga duración
Especial control médico
```

Medicines whose CN returned no data keep empty (`NaN`) values in these columns, because the merge is a left join.
