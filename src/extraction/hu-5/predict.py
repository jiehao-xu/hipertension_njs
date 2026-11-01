"""
Script para cargar los datos del archivo medicamentosHU4.csv y realizar una inferencia con un modelo KMeans de Scikit learn. 
Una vez hecha la inferencia, se añade una columna al dataset con los resultados del clustering.
"""
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import seaborn as sns
from sklearn.metrics import silhouette_score


def infer_and_add_cluster_column(file_path: str="data/raw/medicamentosHU4.csv"):
    
    df = pd.read_csv(file_path)
    figures_path = Path("data/figures")
    figures_path.mkdir(parents=True, exist_ok=True)


    features = ['Precio venta al público con IVA', 'dosis', 'num_palabras4.4', 
            'num_excipientes', 'indicador_riesgo_grave', 'num_tablas']
    
    df_num = df[features].copy()

    # Escalar los datos
    escalador = StandardScaler()
    datos_escalados = escalador.fit_transform(df_num)

    # Probar diferentes números de clusters
    valores_k = [2, 3, 4, 5, 6, 7, 8]
    fits = []
    score = []
    
    for k in valores_k:
        # Entrenar el modelo para el valor actual de k
        model = KMeans(n_clusters=k, random_state=42, n_init=10)
        model.fit(datos_escalados)
        etiquetas = model.labels_

        # Guardar el modelo entrenado
        fits.append(model)

        score.append(silhouette_score(datos_escalados, etiquetas, metric="euclidean"))

    # Imprimir las puntuaciones obtenidas
    for i in range(len(valores_k)):
        print("k =", valores_k[i], "-> Silhouette Score:", round(score[i], 4))


    # Graficar la puntuacion de Silhouette
    # Explicación puntuacion de Silhouette: Cuanto más cerca de 1, mejor definido está el cluster.
    # Un valor cercano a 0 indica que los clusters se superponen y un valor negativo indica que los puntos están mal asignados.
    figura_silueta = plt.figure(figsize=(8, 4))
    plt.plot(valores_k, score, marker="s", color="orange")
    plt.title("Coeficiente de Silhouette vs k")
    plt.xlabel("Numero de clusters (k)")
    plt.ylabel("Silhouette Score")
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.tight_layout()
    figura_silueta.savefig(figures_path / "silhouette_score.png")
    plt.show()
    plt.close(figura_silueta)

    # Añadir la columna de clusters al dataframe original
    # indice_mejor_k = score.index(max(score))
    # mejor_modelo = fits[indice_mejor_k]
    # print("El número óptimo de clusters es:", valores_k[indice_mejor_k])

    # Elegimos k=6 porque tiene un score bueno, pero no creamos microgrupos
    df["n_cluster"] = fits[4].labels_

    print("Numero de elementos por clúster:")
    print(df["n_cluster"].value_counts().sort_index())

    print("\nMedias de cada variable por clúster:")
    centroides = df.groupby("n_cluster")[features].mean().round(2)
    print(centroides)

    nombres_clusters = {
        0: "Fármacos de riesgo alto",
        1: "Fármacos de alta complejidad química",
        2: "Fármacos básicos y seguros",
        3: "Fármacos muy económicos",
        4: "Fármacos caros de riesgo muy alto",
        5: "Fármacos premium de dosis extrema"
    }

    df["cluster"] = df["n_cluster"].map(nombres_clusters)

    # Guardar el dataset con la nueva columna
    output_path = Path("data/raw/medicamentosHU5.csv")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)

    
infer_and_add_cluster_column()