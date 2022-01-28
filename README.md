# Actividad: Usos de filtros espaciales y morfológicos

## Objetivos

El  objetivo  de  este  trabajo  es  buscar  y  analizar  los  filtros  espaciales  y  morfológicos más habitualmente usados en la literatura. Esto permitirá consolidar los conceptos y operaciones sobre imágenes aprendidas en teoría.

## Descripción

Las  operaciones  espaciales  tienen  en  cuenta  las  relaciones  de  vecindad  entre  los píxeles para aplicar diferentes tipos de mejoras a la imagen. Las operaciones morfológicas simplifican imágenes y conservan las principales características de los objetos. Los estudiantes deben analizar los filtros estudiados en clase y compararlos con  otros  que  se  estén  usando  actualmente  para  resolución  de  problemas  reales. Pueden  buscar  e  investigar  en  paquetes  de  imagen  de  Python  como  Skimage, OpenCV, Mahotas, PIL, etc. La solución se implementará en un notebook Python que describirá y mostrará en pantalla los resultados de los principales pasos. En caso de que se utilice partes de un software existente, deberá referenciarse la fuente.  La solución aportada no debe ser básica: repetición de una solución bien conocida o existente en una librería. Se pueden utilizar funcionalidades proporcionadas por las librerías,  pero  la  implementación  de  la  operación  principal  debe  ser  propia.  No  se permite  copiar  código  de  Internet.  En  caso  de  que  se  reutilicen  ideas  deberá referenciarse la fuente.

[Ver Rúbrica](./mexmiart02_act2.docx "Ver archivo docx")

## Forma de entrega

Han de entregarse dos documentos. Primero, un notebook de Jupyter con la solución propuesta  y  los  ficheros  adicionales  que  se  necesiten  para  ejecutarlo.  Segundo,  un informe donde se explique el problema o contexto donde se han implementado los diferentes filtros, cuáles de estos filtros (LP, HP, detección de bordes, morfológicos, diferentes combinaciones de los anteriores, etc.) han sido empleados y por qué, los resultados obtenidos y unas conclusiones. Se puede incluir bibliografía. 

Extensión máxima del informe: 6/8 páginas.

## FHS

- La carpeta `im` contiene imágenes de ejemplo, se pueden agregar las necesarias.
- La carpeta `out` contendrá los archivos de salida al correr el código Python.
- La carpeta `writing` contiene el trabajo escrito: [main.pdf](./writing/main.pdf).
- `apt.txt` configura dependencias a instalar sobre el contenedor, ubuntu por default para mybinder.org
- `main.ipynb` contiene el código modificable que sustenta el trabajo.
- `requirements.txt` configura las dependencias de python sobre el contenedor, se instalan vía pip.

## Instalación

Para la instalación local solo corre:

    pip install -r requirements.txt

## Uso

Ver en línea: [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gl/genomorro%2Funir/PC-A2)

[Ver solo el código fuente en línea](https://gitlab.com/genomorro/unir/-/tree/PC-A2)

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

