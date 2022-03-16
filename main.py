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
# # Árboles de regresión y random forest para regresión y clasificación
#
# ## Librerías a utilizar
#
# Para el tratamiento se han agregado principalmente cinco bibliotecas. En el caso de `sklearn`, se tuvo la necesidad de hacer importaciones parciales para que ciertas funciones y métodos sean detectados correctamente.

# %% tags=[]
from sklearn import metrics
from sklearn import tree
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.model_selection import train_test_split, KFold, cross_val_score
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor, export_graphviz
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import seaborn as sns
import sklearn as sl

# %% [markdown]
# ## Carga de datasets
#
# Se usarán dos datasets~\citep{housing_2018} los cuales serán cargados en dos dataframes. Aquel identificado como `test` solo será usado al final para completar el dataset con el modelo.

# %%
df_train = pd.read_csv("./ds/housing_train.csv")
df_test = pd.read_csv("./ds/housing_test.csv")

# %% [markdown]
# ## Resumen de datos
#
# Las dimensiones del dataframe, filas y columnas, se obtiene con la propiedad `shape`, los valores de las cabeceras se obtienen con la propiedad `columns.values`.

# %%
df_train.shape

# %% [markdown]
# La función `describe()` devuelve el conteo de campos no nulos, media, desviación estándar y cuantiles para columnas númericas. En las columnas identificadas como objetos (categóricas) devolverá el conteo de campos no nulos, número de valores posibles, el valor más repetido y su frecuencia. Si se desea saber el tipo de datos que tienen las columnas se usa la propiedad `dtypes`.

# %%
df_train.describe().transpose()

# %%
df_train.describe(include='object').transpose()

# %%
df_train.dtypes

# %% [markdown]
# Para obtener detalles por columna podemos usar `df_train['Nombre de columna'].describe()`, también es posible obtener por columna los posibles valores posibles y sus respectivas frecuencias, como en el siguiente ejemplo.

# %%
df_train["SaleType"].value_counts()

# %% [markdown] tags=[]
# ### Matriz de correlación
#
# La matriz de correlación indicará que tan fuerte o débil es la relación entre dos variables. Puede leerse por columnas o por filas. En la siguiente imagen se eliminó la columna `Id`, porque no será relevante para el análisis. La claridad de la celda es directamente proporcional a una mayor correlación.

# %%
df_train = df_train.drop(columns = ['Id'])
plt.figure(figsize=(20,8),dpi=80)
corrmat = df_train.corr()
sns.heatmap(corrmat, vmax=.8, fmt='.1f', annot=True)

# %% [markdown]
# De esta forma podemos saber que variables están más relacionadas con otras. en el caso de la variable `SalePrice` las diez variables más útiles serán aquellas con mayor índice de correlación, mismas que se usarán posteriormente para las predicciones.

# %%
df_train.corr()['SalePrice'].sort_values(ascending=False)[1:11]

# %% [markdown]
# ## Valores perdidos
#
# Trabajar con los valores perdidos requiere primero su ubicación, posteriormente se seleccionará que debe ser borrado y luego que debe ser sustituido con un nuevo valor, por supuesto habrá que decidir cual será dicho valor nuevo.
#
# ### Eliminar campos
#
# Para ubicar si una celda tiene un valor vacío se usa la función `isnull()`, si se prefiere lógica inversa se usa `notnull`. Es posible  obtener un vector  de estos  valores con la  propiedad `values`, transformarlo  a un array con la función `ravel()` y sumar los valores verdaderos con la función `sum()`. También es posible obtener una lista ordenada de las columnas con más valores vacíos.

# %%
df_train.isnull().sum().sort_values(ascending=False)[0:19]


# %% [markdown]
# En  el ejemplo  de  arriba, el  valor es  el  número de  valores  vacíos, si  usamos la  función `notnull()` sería el número de valores no vacíos, la suma de ambos debe ser el número total de filas obtenido anteriormente.
#
# Hay dos razones para la falta de valores en los datasets:
#
# - Recolección de datos: No se consiguieron los datos.
# - Extracción de datos: Los datos están en la  DB original pero no se extrajeron correctamente al dataset.
#
# Se deben evitar datos vacíos para no tener problemas de manejo de información. Se tienen dos opciones:
#
# - Borrar las filas donde falten valores en alguna de las columnas
# - Borrar las columnas donde no se tenga suficiente información
#
# En este ejercicio es posible observar que las columnas `MiscFeature, Fence, PoolQC, FirePlaceQu y Alley` tienen muy pocos valores proporcionados (menos del 55 por ciento)y no vale la pena conservarlas. Otro criterio para asegurar un buen curso de acción es revisar las correlaciones con la columna `SalePrice`.
#
# Como el razonamiento es el correcto se procede al borrado de columnas.

# %%
def toDel(df):
    for col in df.columns.values:
        nv = pd.isnull(df[col]).values.ravel().sum()
        if nv > df.shape[0] * 0.45:
            print("Deleting: "+col)
            del df[col]
    return df
df_train = toDel(df_train)


# %% [markdown]
# ### Llenar campos
#
# Es necesario detectar nuevamente que columnas tienen valores vacíos. Esta vez se reemplazarán esos valores. Hay valores númericos y categóricos vacíos; los numéricos serán reemplazados por el promedio original de la columna, los categóricos serán remplazados por el valor no nulo más cercano puede ser el valor que va antes (`ffill`) o el que va después (`bfill`), en este análisis será el segundo.
#
# Es necesario señalar que el procedimiento más preciso para las columnas categóricas sería colocar el valor de mayor frecuencia relacionado con el valor de la columna objetivo, por ejemplo: Si la columna `Y` del dataframe es la variable dependiente y `X` es una columna categórica con valores perdidos; dichos valores se llenarán por aquel de mayor frecuencia en `X` tomando en cuenta solo aquellos con los que coincidan en `Y`. Más adelante se retomará la justificación de porque no se ha hecho de esta forma.

# %%
def DetectNull(df):
    candidates = []
    for col in df.columns.values:
        nv = pd.isnull(df[col]).values.ravel().sum()
        if nv > 0:
            candidates.append((col, df[col].dtype, nv))
    return candidates


# %%
def FillNull(df, list):
    for col in list:
        if col[1] == 'float64':
            df[col[0]] = df[col[0]].fillna(df[col[0]].mean())
        else:
            df[col[0]] = df[col[0]].fillna(method="bfill")
    return df


# %%
df_test = FillNull(df_test, DetectNull(df_test))
df_train = FillNull(df_train, DetectNull(df_train))
df_train.isnull().sum().sort_values(ascending=False)

# %% [markdown]
# ## Problema de regresión

# %% [markdown] tags=[]
# ### Árboles de decisión
#
# Primero serán creados los conjuntos de prueba y entrenamiento. Serán usados para el modelo solo aquellos campos que tengan un alto índice de correlación en la matriz de correlaciones mostrada anteriormente.

# %%
train, test = train_test_split(df_train, test_size=0.2)
predictors = ['OverallQual', 'GrLivArea', 'GarageCars', 'GarageArea', 'TotalBsmtSF', '1stFlrSF', 'FullBath', 'TotRmsAbvGrd', 'YearBuilt', 'YearRemodAdd']
target = ['SalePrice']

# %% [markdown]
# A continuación se entrena el árbol de regresión y se ingresan los datos para probar la predicción del mismo.

# %%
dtr = DecisionTreeRegressor(max_depth=15, min_samples_split=20, random_state=99)
dtr.fit(train[predictors], train[target])
prediction = dtr.predict(test[predictors])

# %% [markdown]
# Ahora se muestran los resultados: una comparación entre los datos originales y las predicciones, además, el árbol obtenido, mismo que fue guardado en la carpeta `out` del proyecto en formato graphviz y como imagen.~\citep{Galarnyk_2021}

# %% tags=[]
test['preds'] = prediction
test[['SalePrice','preds']]

# %% [markdown]
# En la tabla se observa que muchos valores de predicción están repetidos, esto se debe a que entran en la misma lógica de predicción. Debe recordarse que el árbol funciona decidiendo con valores preestablecidos.

# %%
with open('out/dtr.dot','w') as dotfile:
    export_graphviz(dtr, out_file=dotfile, feature_names=predictors)
    dotfile.close()

# %%
tree.plot_tree(dtr);

# %% [markdown]
# Para validar el modelo se usará un método de validación cruzada, un método estadístico para evaluar y comparar algoritmos de aprendizaje dividiendo datos en dos segmentos: entrenamiento y prueba. Típicamente, ambos conjuntos deben cruzarse en rondas sucesivas de modo que cada punto de datos tenga la posibilidad de ser validado. La forma básica es la validación cruzada k-fold.~\citep{Refaeilzadeh_Tang_Liu_2018}

# %%
dtr = DecisionTreeRegressor(max_depth=15, min_samples_split=20, random_state=99)
dtr.fit(train[predictors], train[target])
cv = KFold(n_splits = 20, shuffle = True, random_state = 1)
score = np.mean(cross_val_score(dtr, train[predictors], train[target], scoring = "neg_mean_squared_error", cv = cv, n_jobs = 1))
score

# %% [markdown]
# El modelo es muy deficiente según el error cuadrático medio de pérdida. Este error es muy grande, debería ser cercano a cero. Sería mejor probar un modelo lineal, los árboles de regresión son útiles si es necesario estimar un modelo no lineal. Para confirmar se realizará este modelo bajo diferentes profundidades del árbol, de esta forma se podría encontrar un mejor conjunto de parámetros, no sucede en este caso.

# %%
for i in range(1,21):
    dtr = DecisionTreeRegressor(max_depth=i, min_samples_split=20, min_samples_leaf=5,random_state=99)
    dtr.fit(train[predictors], train[target])
    cv = KFold(n_splits = 20, shuffle = True, random_state = 1)
    score = np.mean(cross_val_score(dtr, train[predictors], train[target], scoring = "neg_mean_squared_error", cv = cv, n_jobs = 1))
    print("Score para i=",i,": ",score)

# %% [markdown] tags=[]
# ### Random Forest
#
# Al igual que en la sección anterior, se entrena el modelo con los mismos conjuntos definidos anteriormente y se hace una predicción.

# %%
rfr = RandomForestRegressor(n_jobs = 1, oob_score=True, n_estimators=10000)
rfr.fit(train[predictors], train[target].values.ravel())
prediction = rfr.predict(test[predictors])
test['preds'] = prediction
test[['SalePrice','preds']]

# %% [markdown]
# Como puede verse, un bosque de diez mil árboles las estimaciones los valores se acercan notablemente. Esto puede confirmarse con la puntuación propia del bosque, la cual funciona como el coeficiente de determinación de un modelo de regresión.

# %%
rfr.oob_score_

# %% [markdown]
# La conclusión es que sería mejor usar un modelo de regresión que un modelo de decisión porque pese a la mejora sustancial respecto al árbol anterior, el bosque no alcanza un 0.9 en la puntuación, condición que se le exigiría a un modelo lineal. Debido a que este es el mejor modelo obtenido, lo usaremos para `df_test`.

# %%
df_test['SalePrice'] = rfr.predict(df_test[predictors])
df_test.to_csv('out/housing_test_complete.csv')


# %% [markdown] tags=[]
# ## Problema de clasificación
# ### Creación de categorías de SalesPrice
#
# Ahora se procederá a crear categorías con la columna `SalePrice`. Para ello se ha escrito una función y una nueva columna dentro del dataframe.

# %%
def SalePriceGroupValue(x):
    if x >= 500001:
        return 'G3'
    elif x <= 100000:
        return 'G1'
    return 'G2'
df_train["SalePriceGroup"] = df_train["SalePrice"].apply(SalePriceGroupValue)
df_train["SalePriceGroup"].value_counts()

# %% [markdown]
# Aquí es posible observar que la gran mayoria de los datos se encuentran en la categoría `G2`. Esto confirma que la opción antes seleccionada para llenar datos perdidos es buena debido a que binda una posibilidad de preservar datos las otras categorías.

# %% [markdown]
# ### Árboles de decisión
#
# Se repetirá el procedimiento visto anteriormente, la diferencia es que ahora usará `DecisionTreeClassifier`.~\citep{Navlani_2018}

# %%
train, test = train_test_split(df_train, test_size=0.2)

# %%
colnames = df_train.columns.values.tolist()
predictors = ['OverallQual', 'GrLivArea', 'GarageCars', 'GarageArea', 'TotalBsmtSF', '1stFlrSF', 'FullBath', 'TotRmsAbvGrd', 'YearBuilt', 'YearRemodAdd']
target = colnames[75]
dtc = DecisionTreeClassifier(criterion="entropy", max_depth=3, min_samples_split=20, random_state=99)
dtc.fit(train[predictors], train[target])
prediction = dtc.predict(test[predictors])

# %% [markdown]
# Se ha creado una tabla cruzada que logra visualizar los resultados, además es posible usar metricas simples para verificar la exactitud del árbol.

# %%
pd.crosstab(test[target], prediction, colnames=["Predictions"], rownames=["Real"])

# %%
print("Accuracy: ", metrics.accuracy_score(prediction, test[target]))

# %%
with open('out/dtc.dot','w') as dotfile:
    export_graphviz(dtc, out_file=dotfile, feature_names=predictors)
    dotfile.close()

# %% [raw]
# file = open('out/dtc.dot', 'r')
# text = file.read()
# Source(text)

# %%
tree.plot_tree(dtc);

# %% [markdown] tags=[]
# Al usar nuevamente validación cruzada se observa que una buena clasificación esta entre `i=3` e `i=6`, lo que significa que si se deja crecer el árbol desde el nodo raíz con estas profundidades es posible obtener clasificaciones óptimas. También podemos ver que las variables de mayor importancia clasificatoria son `TotalBsmtSF` y `GrLivArea`.

# %%
for i in range(1,10):
    dtc = DecisionTreeClassifier(criterion="entropy", max_depth=i, min_samples_split=20, random_state=99)
    dtc.fit(train[predictors], train[target])
    cv = KFold(n_splits = 20, shuffle = True, random_state = 1)
    score = np.mean(cross_val_score(dtc, train[predictors], train[target], scoring = "accuracy", cv = cv, n_jobs = 1))
    print("Score para i=",i,": ",score)
    print("Importancia de variables: \n\t",dtc.feature_importances_)

# %% [markdown]
# ### Random Forest
#
# En la implementación de este bosque se usa el mismo procedimiento visto anteriormente, es importante poner atención en los cambios de los argumentos de cada árbol, cada implementación dependerá del problema.

# %%
rfc = RandomForestClassifier(n_jobs = 1, oob_score=True, n_estimators=10000)
rfc.fit(train[predictors], train[target])
prediction = rfc.predict(test[predictors])
test['preds'] = prediction
test[['SalePriceGroup','preds']]

# %% [markdown]
# En esta ocasión se ha aumentado la exactitud del árbol, es posible decir que se ha creado un modelo confible. Debido a que este es el mejor modelo obtenido, lo usaremos para `df_test`.  

# %%
rfc.oob_score_

# %%
df_test['SalePriceGroup'] = rfc.predict(df_test[predictors])
df_test.to_csv('out/housing_test_complete.csv')

# %% [markdown]
# ## Conclusión

# %% [markdown]
# En esta actividad se retomó el [USA Housing Dataset](https://www.kaggle.com/gpandi007/usa-housing-dataset), el cual presenta datos sobre la venta de casas en Estados Unidos. Se describieron los datos y se creó una matriz de corelaciones para obtener aquellos más importantes para el análisis. Como segundo paso se realizó una limpieza de datos, se eliminaron columnas innecesarias y llenaron valores perdidos bajo criterios claros. Una vez realizadas dichas operaciones fue posible entrenar árboles de desición y random forest.
#
# El dataset no tiene una descripción clara de los datos proporcionados, aunque es posible analizarlos e inferir algunos de los significados, una de los requisitos más importantes para el análisis siempre será una descripción inicial clara de los mismos, incluso la interpretación de los resultados depende de ello.
#
# Para entrenar los modelos se usaron variables númericas, con esto se obtuvieron resultados positivos en lo general. Si se hubieran usado variables categóricas habría la necesidad de procesarlas y crear varibles separadas (variables dummy, con la función `pd.get_dummies`). Es importante decir que el árbol de regresión obtuvo un mal modelo, sin embargo, el bosque de regresión presentó resultados mucho mejores, aunque sería interesante compararlo con un modelo lineal en un trabajo futuro. Si el problema se convierte en categórico los resultados mejoran notablemente, la principal razón es que las hojas de los árboles siempre corresponden a una categoría, incluso en regresión, por lo tanto, el árbol de regresión será una opción si otros modelos de regresión no tuvieron resultados satisfactorios.
#
# Otro punto a mencionar es que los modelos probados son ajustables mediante muchos parámetros, su ajuste dependerá del problema que se enfrenta y hasta cierto punto es un proceso de ajuste a prueba y error. Además el proceso de validación cruzada es de gran ayuda para evitar el crecimiento excesivo de los árboles.
#
# Finalmente, decir que algunos de los resultados pueden inspeccionarse a mayor detalle en la carpeta `out` anexa a este documento.
#
#
