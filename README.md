# Actividad 1: Conceptos generales de redes neuronales

- Objetivos

En esta actividad aprenderemos cómo programar redes neuronales con Keras y TensorFlow y pondremos en práctica varios de los conceptos avanzados de entrenamiento de redes neuronales profundas vistos en clase. Para ello, utilizaremos el dataset de Fashion MNIST, un problema sencillo con imágenes pequeñas de prendas de ropa. 

- Descripción

La práctica consta de nueve preguntas con sus subapartados (en caso de que los tengan). En cada una de ellas se repasarán uno o varios conceptos importantes de las redes neuronales que servirán para mejorar el entendimiento del alumno de la asignatura y de las propias redes neuronales, su funcionamiento y los posibles errores que puedan aparecer.

## FHS

- `Actividad_1_master_IA_SCA.ipynb` contiene el notebook de la actividad.
- `apt.txt` configura dependencias a instalar sobre el contenedor, ubuntu por default para mybinder.org
- `requirements.txt` configura las dependencias de python sobre el contenedor, se instalan vía pip.
- La carpeta `writing` contiene el trabajo escrito en formato pdf en el archivo [main.pdf](writing/main.pdf).
- La carpeta `im` contiene imágenes de ejemplo, se pueden agregar las necesarias.
- La carpeta `out` contendrá los archivos de salida.

## Instalación

Para la instalación local solo corre:

    pip install -r requirements.txt

## Uso

Ver en línea: [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gl/genomorro%2Funir/SCA-A1?labpath=Actividad_1_master_IA_SCA.ipynb)

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

Copyright (C) 2022, Edgar Uriel Domínguez Espinoza

Actividades escolares UNIR is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 2 of the License, or (at your option) any later version.

Actividades escolares UNIR is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with Actividades escolares UNIR; if not, see <http://www.gnu.org/licenses/> or write to the Free Software Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301 USA

