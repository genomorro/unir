# Actividad: Evaluación de la segmentación

## Objetivo

El objetivo de este trabajo es aprender a construir y evaluar el rendimiento de uno o 
más segmentadores. Esta actividad permitirá consolidar los conceptos sobre 
segmentación de imágenes aprendidos.

## Descripción

Nos vamos a enfrentar a un verdadero problema de segmentación. La segmentación, 
como se ha visto, consiste en detectar regiones homogéneas y aislar/detectar objetos 
dentro de una imagen. Estas regiones habitualmente corresponden a los objetos que 
se están queriendo identificar. 
Existen muchas maneras de enfocar este problema y puedes hacer uso de las técnicas 
de  segmentación  que  consideres  para  resolverlo.  Una  vez  elegidas  estas  técnicas, 
debes evaluar su rendimiento frente a imágenes de ground truth. En caso de que se 
utilicen  partes  de  un  software  existente,  deberá  referenciarse  la  fuente.  Debes 
mostrar en pantalla los resultados de los principales pasos. 
Escoge  una  o  dos  imágenes  que  consideres  representativas  de  un  determinado 
problema y aplica varios segmentadores sobre ellas para evaluar cuál de ellos ofrece 
el mejor resultado.

Forma de entrega: debes adjuntar la memoria y el código fuente usado. La extensión 
máxima del informe ha de ser 6/8 páginas.

[Ver rúbrica](./mexmiart02_act3.docx "Instrucciones")

## FHS

- `apt.txt` configura dependencias a instalar sobre el contenedor, ubuntu por default para mybinder.org
- `requirements.txt` configura las dependencias de python sobre el contenedor, se instalan vía pip.
- La carpeta `im` contiene imágenes de ejemplo, se pueden agregar las necesarias.
- La carpeta `out` contendrá los archivos de salida.
- La carpeta `writing` contendrá los archivos con el trabajo escrito: [main.pdf](writing/main.pdf "Trabajo escrito").

## Instalación

Para la instalación local solo corre:

    pip install -r requirements.txt

## Uso

Ver en línea: [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gl/genomorro%2Funir/PC-A3)

[Ver solo el código fuente en línea](https://gitlab.com/genomorro/unir/-/tree/PC-A3)


Para el uso en una máquina local simplemente abre el archivo `main.ipynb` o `main.py`. Cada proyecto usa archivos `ipynb` y `py` de forma indistinta, gracias a jupytext se pueden sincronizar. Para saber como hacerlo de momento lo mejor es consultar [jupytext](https://jupytext.readthedocs.io/en/latest/index.html "la documentación de jupytext"), después pondré aquí los comandos que use más comúnmente. 

Si inicio con un `ipynb` lo convierto a `py`:

    jupytext --to py:percent test.ipynb

De otra forma:

    jupytext --to notebook test.py
	
Después de eso hacer algo como:

    jupytext --update --to notebook test.py

## Licencia
This repo is part of Actividades escolares UNIR

Copyright (C) 2021, Edgar Uriel Domínguez Espinoza

Actividades escolares UNIR is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 2 of the License, or (at your option) any later version.

Actividades escolares UNIR is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with Actividades escolares UNIR; if not, see <http://www.gnu.org/licenses/> or write to the Free Software Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301 USA

<!-- ## Otros detalles -->

<!-- ### Referencias cruzadas en MD -->

<!-- Por favor ver [Tabla 1](#tbl:1) y [Imágenes a utilizar](#Imágenes-a-utilizar) -->


<!-- \begin{align} -->
<!--     g &= \int_a^b f(x)dx \label{eq1}\tag{1} \\ -->
<!--     a &= b + c \label{eq2}\tag{2} -->
<!-- \end{align} -->

<!-- See (\ref{eq1}) and (\ref{eq2}) -->

<!-- See (\ref{eq1}) and (\ref{eq2}) does not work from another cell. -->
<!-- See ([1](#mjx-eqn-eq1)) and ([2](#mjx-eqn-eq2)) does work from another cell. -->
