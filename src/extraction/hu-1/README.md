## Ejecución

El script debe ejecutarse desde la raíz del proyecto:

```bash
python src/extraction/hu-1/rest_api.py
```


## Proceso de extracción

En primer lugar se realiza una petición `POST` al endpoint de búsqueda de CIMA:

```python
response = requests.request(
    "POST",
    url_ficha_tecnica,
    headers=headers,
    data=payload
)
```

De la respuesta se extraen los números de registro de los medicamentos:

```python
nregistros = []

for resultado in lista_medicamentos["resultados"]:
    nregistros.append(resultado["nregistro"])
```

Posteriormente se realiza una petición individual para cada medicamento:

```python
url_medicamento = (
    f"https://cima.aemps.es/cima/rest/medicamento?nregistro={nregistro}"
)

response = requests.request("GET", url_medicamento)
medicamento = response.json()
```

Finalmente, los datos seleccionados se almacenan en una lista de diccionarios y se transforman en un `DataFrame`:

```python
df = pd.DataFrame(medicamentos)
```
## Salida

El resultado de la extracción se almacena en:

```text
data/raw/medicamentos.xlsx
```

El directorio se crea automáticamente si no existe:

```python
output_path = Path("data/raw/medicamentos.xlsx")
output_path.parent.mkdir(parents=True, exist_ok=True)

df.to_excel(output_path, index=False)