# -*- coding: utf-8 -*-
# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.13.5
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %% [markdown]
# # Análisis: Abstract data set for Credit card fraud detection
#
# ## Carga de bibliotecas
#
# En este análisis se usará la biblioteca `SciPy` para realizar un agrupamiento jerárquico y `scikit-learn` para realizar un modelo de detección de anomalías. En ambos casos se persigue detectar de forma automática valores inusuales dentro de un conjunto de datos.

# %%
from scipy.cluster.hierarchy import dendrogram, linkage, cophenet, fcluster
from scipy.spatial.distance import pdist
from sklearn import metrics
from sklearn.ensemble import IsolationForest
import copy
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# %% [markdown]
# ## Carga de dataset y resumen de datos
#
# Se usará un _dataset_~\citep{Joshi_2018} el cual corresponde al _dataframe_ que se usará durante el análisis.

# %%
df = pd.read_csv("./ds/creditcardcsvpresent.csv")

# %% [markdown]
# Este dataframe contiene once columnas. Las primeras dos de ellas serán borradas porque una corresponde a un índice de datos y la otra es una columna completamente vacía, por lo tanto irrecuperable.

# %%
df.info()

# %% [markdown] tags=[]
# ### Eliminación de columnas
#
# Primero será necesario guardar la columna objetivo `isFraudulent` en una nueva variable, pues será borrada del dataframe de trabajo debido a que utilizaremos métodos de análisis no supervisados.

# %%
ideal_results = df["isFradulent"]

# %% [markdown]
# Ahora es posible borrar todas las columnas que no son necesarias para el análisis a realizar.

# %%
df = df.drop(["Merchant_id", "Transaction date", "isFradulent"], axis=1)

# %%
df.info()

# %% [markdown]
# Este dataframe contiene nueve columnas, las cuales no son descritas en la fuente original, por lo que solo es posible intuir su significado, por supuesto, esto podría condicionar la discusión producto del análisis. Es importante hacer énfasis en proporcionar metadatos sobre cualquier conjunto de datos computables: texto, audio, video, dataset, etc.
#
# Seis de esas columnas son de tipo numérico y las tres restantes son categóricas, enseguida se muestra su descripción general.

# %%
df.describe().transpose()

# %%
df.describe(include='object').transpose()

# %%
for o in ["Is declined", "isForeignTransaction","isHighRiskCountry"]:
    print("-----")
    print(df[o].value_counts())

# %% [markdown]
# ### Tratamiento de variables categóricas
#
# Se crean variables  separadas, para no usar  variables categóricas. La variable  categórica `Is declined` que toma  valores `Y`  o `N`  en `df["Is declined"]`  se puede  sustituir por  dos variables  _dummy_, booleanas, que son `Is declined_Y` e `Is declined_N`. Es posible tomar ambas variables o solo una de ellas, tal y como se hará en este análisis. Posteriormente se borra la variable original y se adjuntas las nuevas variables al dataframe.

# %%
df = pd.get_dummies(df,columns=["Is declined", "isForeignTransaction","isHighRiskCountry"],drop_first=True)

# %%
df.info()

# %% [markdown]
# ## Matriz de correlación
#
# Con la matriz de correlación es posible observar similitudes entre diferentes datos. Es posible observar que la matriz tiene zonas de colores similares, por ejemplo la parte central tiene tres variables que posiblemente sirvan para crear un grupo del cual quizá se construya una categoría, o bien termine por ser un grupo de datos poco relevantes para la clasificación.

# %%
plt.figure(figsize=(20,8),dpi=80)
corrmat = df.corr()
sns.heatmap(corrmat, vmax=.8, fmt='.1f', annot=True)

# %% [markdown]
# De esta forma, en este momento se hará la siguiente predicción:
#     
# - Existen al menos dos grupos de datos: Datos más relevantes para la clasificación y datos menos relevantes para la clasificación.
# - Las columnas `isForeignTransaction_Y`, `isHighRiskCountry_Y`, `Transaction_amount` y `Total Number of declines/day` parecen formar uno de esos grupos.
# - Las columnas `Daily_chargeback_avg_amt`, `6_month_avg_chbk_amt`, `6-month_chbk_freq` y `Is declined_Y` forman el segundo grupo.
# - No hay evidencia para la columna `Average Amount/transaction/day`.
#
# Está predicción solo se convertiría en una hipótesis si fuera confirmada con una matriz de distancias. En este análisis se procederá directamente a implementar un método de clustering.

# %% [markdown]
# ## Clustering jerárquico
#
# Un _cluster_ jerárquico categoriza las entradas en grupos. Es un método no supervisado, por lo tanto no se usarán datos de entrenamiento, sino que todos los datos serán utilizados para crear una clasificación.

# %%
# method=single, complete, average, weighted, centroid, median, ward
Z = linkage(df, "centroid")

# %% [markdown]
# Es necesario tener una métrica de evaluación del método. Por lo tanto se obtendrá una distancia de correlación _cophenetic_ (c) y una matriz de distancias _cophenetic_ condensada. Esto nos da una idea de cuán similares son los objetos agrupados.\citep{The_SciPy_community_2022a}

# %%
c, d = cophenet(Z, pdist(df))
print(c)

# %% [markdown]
# La matriz _Z_ se compone de cuatro elementos:
#
# - Primer elemento a agrupar
# - Segundo elemento a agrupar
# - Distancia entre elementos
# - Número total de elementos operados

# %%
Z[1000:1010]

# %% [markdown]
# Ahora se mostrará un dendrograma truncado de la matriz `Z`. En este caso se mostrarán los diez elementos. En el eje de las ordenadas aparecerán las distancias de agrupación, en el eje de las abscisas aparecen dos posibles datos: entre paréntesis el número de elementos incluidos en la hoja, sin paréntesis el índice del elemento que se integra al cluster. Esto nos permite saber el tamaño de los clusters creados y visualizarlos mejor.

# %%
plt.figure(figsize=(10,10))
plt.title("Dendrograma de clustering jerárquico")
plt.ylabel("Distancias calculadas")
plt.xlabel("Elementos agrupados")
dendrogram(Z, leaf_rotation=90.,leaf_font_size=10, truncate_mode="lastp", p=10, show_leaf_counts=True, show_contracted=True)
plt.savefig('im/dendrograma_jerarquico.png', format='png', bbox_inches='tight')

# %% [markdown] tags=[]
# ### Recuperar clusters

# %% tags=[]
#clusters = fcluster(Z,40000,criterion="distance")
clusters = fcluster(Z,2,criterion="maxclust")

# %% [markdown]
# Es momento de observar el comportamiento como clasificador binario.

# %%
print(pd.crosstab(ideal_results, clusters, colnames=["Predicted"], rownames=["Real"]))
real = copy.deepcopy(ideal_results)
real.replace(to_replace={'N':2,'Y':1},inplace=True)
print("Accuracy: ", metrics.accuracy_score(clusters, real))

# %% [markdown]
# Como puede observarse, este método falla al detectar aquellos casos en los que hay fraude. Es necesario tomar en cuenta que este cluster solo agrupa los datos, su objetivo directo no es identificar el fraude, por lo que es posible que las agrupaciones correspondan a criterios distintos. Es posible probar la predicción hecha anteriormente sobre la matriz de correlación, para ello se harán dos nuevos clusters con los conjuntos de datos listados entonces.

# %%
Z1 = linkage(df[["isHighRiskCountry_Y","Transaction_amount","Total Number of declines/day"]], "centroid")
Z2 = linkage(df[["Daily_chargeback_avg_amt","6_month_avg_chbk_amt","6-month_chbk_freq","Is declined_Y"]], "centroid")

# %% [markdown]
# Es posible ver que ambos modelos son más favorables al obtener la distancia de correlación _cophenetic_. En el caso del conjunto 2 esta distancia es bastante alentadora aunque la proporción de verdaderos positivos y verdaderos negativos (_accuracy_) podría ser mejor. Es posible considerar al modelo obtenido de `Z2` como favorable.

# %%
c1, d1 = cophenet(Z1, pdist(df[["isHighRiskCountry_Y","Transaction_amount","Total Number of declines/day"]]))
c2, d2 = cophenet(Z2, pdist(df[["Daily_chargeback_avg_amt","6_month_avg_chbk_amt","6-month_chbk_freq","Is declined_Y"]]))
print("Distancia de correlación cophenetic Z1: ",c1,"\nDistancia de correlación cophenetic Z2: ",c2)

# %%
clusters2 = fcluster(Z2,2,criterion="maxclust")
print(pd.crosstab(ideal_results, clusters2, colnames=["Predicted"], rownames=["Real"]))
print("Accuracy: ", metrics.accuracy_score(clusters2, real))

# %% [markdown] tags=[]
# ## Isolation forest
#
# Es turno de implementar un algoritmo que crea un prototipo de aquello considerable como "normal" en un dataset para luego identificar anomalías.

# %%
ifc=IsolationForest(n_jobs=1,n_estimators=10000)
ifc.fit(df)
anomaly=ifc.predict(df)

# %% [markdown]
# Es destacable que se usó todo el dataframe para entrenar el modelo, esto ocurre así porque al analizar los valores de una característica, se pretende encontrar valores (o pequeños grupos de valores) que se apartan claramente del resto.~\citep{Duboue_2020}

# %%
real.replace(to_replace={2:1,1:-1},inplace=True)
print(pd.crosstab(ideal_results, anomaly, colnames=["Predicted"], rownames=["Real"]))
print("Accuracy: ", metrics.accuracy_score(anomaly, real))

# %% [markdown]
# Es posible observar una buena precisión en este método. Ha hecho un mejor trabajo al detectar los casos en los que efectivamente se espera un fraude.

# %% [markdown]
# ## Reconstrucción del dataset
#
# Ahora se procederá a guardar en un nuevo dataset toda la información resultante de la aplicación de los algoritmos anteriormente expuestos. Dicho dataset quedará almacenado en la carpeta `out` del proyecto.

# %%
df["isFradulent"] = ideal_results
df["Clustering prediction_Y=1"] = clusters2
df["Isolation Forest prediction_N=1"] = anomaly
df.to_csv('out/creditcardcsvpresent_test_complete.csv')

# %% [markdown]
# ## Conclusión
#
# En este análisis se examinó un dataset correspondiente a información financiera que en algunos casos corresponden a fraudes. Se realizó una descripción general de los datos, se hizo tratamiento en las variables categóricas y se obtuvo una matriz general de correlaciones. Es dicha matriz se observaron relaciones entre datos que podrían ayudar a formar grupos de entrada para el entrenamiento de un cluster. Esta idea, sin embargo, puede deberse solo a una coincidencia más que a una regla.
#
# Se creó un cluster jerárquico con todos los datos disponibles en el dataframe y se recuperaron los dos grupos más grandes formados. Es posible observar que el cluster simplemente hace grupos, pero no distingue _a priori_ aquellas cosas que el analista pudiera estar buscando. El modelo obtenido puede tener numerosas ramas y es responsabilidad del analista saber en que nivel o altura cortarlo. También parece que el algoritmo usado funciona mejor con conjuntos de datos de entrada específicos más pequeños o focalizados.
#
# Posteriormente se implementó un algoritmo de detección de anomalías. El _isolation forest_ aísla aquellos datos que se alejan de una norma establecida por el mismo modelo. Su implementación es muy similar a la de otros bosques probados en [otras prácticas](https://gitlab.com/genomorro/unir/-/blob/AA-A1) y se pudo probar que siempre que los parámetros de iteración sean adecuados puede ofrecer resultados bastante confiables.
#
# El algoritmo de _clustering_ es mejor detectando grupos de mayor tamaño mientras que el isolation forest tiene mejor precisión cuando se trata preservar los grupos más pequeños, mejor dicho, puede descartar valores atípicos siempre que exista un conjunto histórico que pueda asegurarle cuales observaciones no son válidas dentro de un dominio determinado.
