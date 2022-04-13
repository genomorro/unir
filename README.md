# Actividad: Clasificación con máquina de vectores de soporte y redes de neuronas

## Objetivos 

Mediante esta actividad se pretende que pongas en práctica la creación de modelos basados en máquinas de vector de soporte y redes de neuronas. El objetivo es que comprendas de forma práctica, con un problema determinado, las diferencias que existen a la hora de entrenar los diferentes modelos.

## Pautas de elaboración

El [conjunto de datos](https://www.kaggle.com/iabhishekofficial/mobile-price-classification#train.csv) contiene la información necesaria; la variable respuesta es «price_range»

- Análisis descriptivo de los datos:
  + De las variables numéricas, halla datos estadísticos.
  + De las variables categóricas, lista las diferentes categorías y halla la frecuencia de cada una de ellas. 
  + Crea matriz de correlaciones existentes entre las variables numéricas del conjunto de datos, analiza los resultados. 
- Aplica máquina de vectores de soporte y redes neuronales. 
- Compara, mediante las medidas que te parezcan adecuadas, la capacidad predictiva de ambos métodos. 
- Comenta las ventajas y desventajas de cada modelo. De acuerdo con los resultados, ¿son realmente útiles los modelos creados para el conjunto de datos propuesto?
- Otros comentarios que consideres adecuados.

### Extensión y formato 

Extensión máxima de la actividad: 25 páginas. Formato: Calibri 12, interlineado 1,5 puntos.


## FHS

- `apt.txt` configura dependencias a instalar sobre el contenedor, ubuntu por default para mybinder.org
- `requirements.txt` configura las dependencias de python sobre el contenedor, se instalan vía pip.
- La carpeta `writing` contiene el trabajo escrito en formato pdf en el archivo [main.pdf](writing/main.pdf).
- La carpeta `im` contiene imágenes de ejemplo, se pueden agregar las necesarias.
- La carpeta `out` contendrá los archivos de salida.
- La carpeta `ds` contendrá los archivos datasets de entrada.

## Instalación

Para la instalación local solo corre:

    pip install -r requirements.txt

## Uso

Ver en línea: [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gl/genomorro%2Funir/AA-A3) o bien [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/genomorro/unir/AA-A3)

Ver código fuente: [gitlab](https://gitlab.com/genomorro/unir/-/tree/AA-A3)

Cada proyecto usa archivos `ipynb` y `py` de forma indistinta, gracias a jupytext se pueden sincronizar. Para saber como hacerlo de momento lo mejor es consultar [jupytext](https://jupytext.readthedocs.io/en/latest/index.html "la documentación de jupytext"), después pondré aquí los comandos que use más comúnmente. 

Si inicio con un `ipynb` lo convierto a `py`:

    jupytext --to py:percent test.ipynb

De otra forma:

    jupytext --to notebook test.py
	
Después de eso hacer algo como:

    jupytext --update --to notebook test.py
    
Generar la imagen desde el archivo `.dot`:

    dot -Tpng -o im/<nombre>.png out/<nombre>.dot

### unir.patch

Este parche integra el formato UNIR en un archivo LaTeX:

    patch writing/main.tex unir.patch

Hay que tener cuidado con cambiar el nombre de la actividad dentro o posterior al parche.
## Licencia
This repo is part of Actividades escolares UNIR

Copyright (C) 2021, Edgar Uriel Domínguez Espinoza

Actividades escolares UNIR is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 2 of the License, or (at your option) any later version.

Actividades escolares UNIR is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with Actividades escolares UNIR; if not, see <http://www.gnu.org/licenses/> or write to the Free Software Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301 USA

