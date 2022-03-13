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

# %%
import pandas as pd

# %% [markdown]
# ## Carga de datasets

# %%
mainpath = "./ds/"
train = "housing_train.csv"
test = "housing_test.csv"
df_train = pd.read_csv(mainpath + train)
df_test = pd.read_csv(mainpath + test)

# %% [markdown]
# ## Resumen de datos
#
# Las dimensiones del data frame, filas y columnas, se obtiene con la propiedad `shape`, los valores de las cabeceras se obtienen con la propiedad `columns.values`.

# %%
df_train.shape

# %% [markdown]
# La función `describe()` devuelve el conteo de campos no nulos, media, desviación estándar y cuantiles para columnas númericas. En las columnas son objetos (categóricas) devolverá el conteo de campos no nulos, número de valores posibles, el valor más repetido y su frecuencia. Si se desea saber el tipo de datos que tienen las columnas se usa la propiedad `dtypes`.

# %%
df_train.describe().transpose()

# %%
df_train.describe(include='object').transpose()

# %%
df_train.dtypes

# %% [markdown]
# ## Valores perdidos
#
# Para ubicar si una celda tiene un valor vacío se usa la función `isnull()`, si se prefiere lógica inversa se usa `notnull`. Es posible  obtener un vector  de estos  valores con la  propiedad `values`, transformarlo  a un array con la función `ravel()` y sumar los valores verdaderos con la función `sum()`.

# %%
pd.isnull(df_train["Alley"]).values.ravel().sum()


# %% [markdown]
# En  el ejemplo  de  arriba, el  valor es  el  número de  valores  vacíos, si  usamos la  función `notnull()` sería el número de valores no vacíos, la suma de ambos debe ser el número total de filas obtenido anteriormente.
#
# Hay dos razones para la falta de valores en los data sets:
#
# - Recolección de datos: No se consiguieron los datos.
# - Extracción de datos: Los datos están en la  DB original pero no se extrajeron correctamente al data set.
#
# Se deben evitar datos vacíos para no tener problemas de manejo de información. Se tienen dos opciones:
#
# - Borrar las filas donde falten valores en alguna de las columnas
# - Borrar las columnas donde no se tenga suficiente información
#
# En nuestro caso es posible observar que las columnas `MiscFeature, Fence, PoolQC, FirePlaceQu y Alley` tienen muy pocos valores proporcionados y no vale la pena conservarlas. El criterio será: Si una columna no contiene más del 55 por ciento de los datos, está será descartada.

# %%
def DetectNull(df):
    candidates = []
    for col in df.columns.values:
        nv = pd.isnull(df[col]).values.ravel().sum()
        if nv > 0:
            candidates.append((col, df[col].dtype))
    return candidates


# %%
print(DetectNull(df_train))


# %%
def toDel(df):
    for col in df.columns.values:
        nv = pd.isnull(df[col]).values.ravel().sum()
        if nv > df.shape[0] * 0.45:
            print("Deleting: "+col)
            del df[col]
    return df


# %%
df_train = toDel(df_train)
df_train.shape


# %% [markdown]
# ## Creación de categorías de SalesPrice

# %%
def SalePriceGroupValue(x):
    if x >= 500001:
        return 3
    elif x <= 100000:
        return 1
    return 2


# %%
df_train["SalePriceGroup"] = df_train["SalePrice"].apply(SalePriceGroupValue)

# %%
df_train.tail(15)

# %%
