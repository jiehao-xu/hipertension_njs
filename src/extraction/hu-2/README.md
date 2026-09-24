# Scraping de fichas técnicas de medicamentos

Este script realiza un scraping de las fichas técnicas de medicamentos disponibles en CIMA (AEMPS) a partir de las URLs almacenadas en un fichero Excel.

El objetivo es obtener algunas características de las fichas para utilizarse en el siguiente paso de la extracción de datos.

## Ubicación

El script se encuentra en:

```text
src/extraction/hu-2/scrapping.py
```

El fichero de entrada esperado es:

```text
data/raw/medicamentos.xlsx
```

Y el resultado se guarda en:

```text
data/raw/medicamentosHU2.xlsx
```

## Requisitos

El script utiliza las siguientes librerías:

```text
requests
pandas
beautifulsoup4
openpyxl
```

Si alguna no está instalada, puede instalarse con:

```bash
uv pip install requests pandas beautifulsoup4 openpyxl
```

En particular, `openpyxl` es necesaria porque el fichero de entrada y salida está en formato `.xlsx`.

## Fichero de entrada

El fichero:

```text
data/raw/medicamentos.xlsx
```

debe contener una columna llamada:

```text
url_html_ficha_tecnica
```

Esta columna contiene las URLs de las fichas técnicas de los medicamentos.

Las filas que no tengan una URL se ignoran.

## Funcionamiento

Para cada medicamento, el script realiza los siguientes pasos:

1. Obtiene la URL de su ficha técnica.

2. Comprueba que exista una URL. Si está vacía o es `NaN`, se salta ese medicamento.

3. Realiza una petición HTTP a la URL utilizando `requests`.

4. Utiliza un `User-Agent` personalizado:

```python
headers = {
    "User-Agent": "EducationalScraper/1.0"
}
```

Esto identifica la petición como procedente de un scraper educativo.

5. Analiza el HTML descargado utilizando `BeautifulSoup`.

6. Extrae tres características de la ficha técnica:

   * Número de palabras de la sección 4.4.
   * Número de tablas de toda la ficha técnica.
   * Número de apariciones de la palabra `"grave"` en toda la ficha.

7. Añade estos valores a la fila correspondiente del DataFrame.

8. Finalmente, guarda el DataFrame completo en:

```text
data/raw/medicamentosHU2.xlsx
```

## Variables generadas

Se añaden tres columnas al fichero original.

### `num_palabras4.4`

Indica el número de palabras encontradas en la sección 4.4 de la ficha técnica.

El script busca el elemento:

```html
<h2 id="4.4">
```

y recoge el contenido posterior hasta encontrar el siguiente elemento `<h2>`.

Por tanto, el cálculo depende de que la estructura HTML de la ficha técnica mantenga esta organización.

Si no encuentra la sección 4.4, muestra un mensaje como:

```text
Section 4.4 not found for URL: ...
```

y mantiene el valor inicial `0`.

### `num_tablas`

Indica el número de elementos `<table>` encontrados en toda la ficha técnica.

Se obtiene mediante:

```python
tables = soup.find_all("table")
num_tablas = len(tables)
```

Este valor corresponde al número de tablas HTML de la página, no necesariamente al número de tablas visuales que pueda percibir un usuario.

### `indicador_riesgo_grave`

Cuenta cuántas veces aparece la palabra:

```text
grave
```

en el texto completo de la ficha técnica.

Para ello se extrae todo el texto de la página:

```python
text = soup.get_text(" ", strip=True)
```

y posteriormente:

```python
risk_indicator_count = text.lower().count("grave")
```

Por tanto, esta variable no identifica necesariamente un "indicador de riesgo grave" como elemento estructurado de la página. Simplemente cuenta las apariciones de la cadena de texto `"grave"`.

Por ejemplo, una frase que contenga:

```text
reacción adversa grave
```

contará como una aparición.


## Ejecución

Desde la raíz del proyecto:

```bash
python src/extraction/hu-2/scrapping.py
```

La estructura esperada del proyecto sería aproximadamente:

```text
hipertension_njs/
│
├── data/
│   └── raw/
│       ├── medicamentos.xlsx
│       └── medicamentosHU2.xlsx
│
└── src/
    └── extraction/
        └── hu-2/
            └── scrapping.py
```

## Resultado

Una vez terminado el proceso, se genera:

```text
data/raw/medicamentosHU2.xlsx
```

Este fichero mantiene las columnas originales de `medicamentos.xlsx` y añade:

```text
num_palabras4.4
num_tablas
indicador_riesgo_grave
```

Por ejemplo:

| Medicamento   | URL    | num_palabras4.4 | num_tablas | indicador_riesgo_grave |
| ------------- | ------ | --------------: | ---------: | ---------------------: |
| Medicamento A | URL... |             350 |          8 |                      4 |
| Medicamento B | URL... |             215 |          5 |                      2 |

## Consideraciones

El script depende de la estructura HTML de las páginas de CIMA. Si AEMPS modifica la estructura de las fichas técnicas, los selectores utilizados pueden dejar de funcionar.


El script utiliza un timeout de 30 segundos para cada petición:

```python
requests.get(url, headers=headers, timeout=30)
```

Si una página no responde dentro de ese tiempo, la petición generará un error.

Por último, el fichero de resultados se guarda al terminar de procesar cada medicamento. De esta forma, si el proceso se interrumpe después de haber procesado algunas filas, el fichero contendrá los resultados obtenidos hasta ese momento.

## Flujo general

```text
medicamentos.xlsx
       |
       v
Leer URLs de fichas técnicas
       |
       v
Descargar HTML de cada ficha
       |
       v
Analizar HTML con BeautifulSoup
       |
       +--> Palabras sección 4.4
       |
       +--> Número de tablas
       |
       +--> Apariciones de "grave"
       |
       v
Añadir resultados al DataFrame
       |
       v
medicamentosHU2.xlsx
```
