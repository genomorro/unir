# Laboratorio: Eliminación de anomalías de la imagen

## Objetivos

El objetivo de esta actividad es familiarizarnos con las técnicas y herramientas básicas de procesado de imagen. Tras realizar esta actividad serás capaz de identificar anomalías (ruido o artefactos) en imágenes, así como de aplicar las operaciones necesarias para su eliminación.

## Descripción
Has de buscar y seleccionar las imágenes con las anomalías que vas a corregir. Describe qué anomalías o tipología de ruido afectan a dichas imágenes. Posteriormente, idea una solución para corregirlas. Puedes utilizar operaciones a nivel de píxel, lineales o basadas en histograma para resolver dichas anomalías. La solución se implementará en un notebook Python que describirá y mostrará en pantalla los resultados de los principales pasos. El notebook deberá constar de las siguientes secciones:

    1. Descripción del problema y/o anomalía.
    2. Al menos dos imágenes de ejemplo con la anomalía a eliminar.
    3. Solución propuesta.
    4. Ejecución comentada paso a paso del algoritmo.

El algoritmo propuesto no debe ser ad hoc, sino que debe poder extrapolarse a otras imágenes con la misma anomalía. Para aseguraros de que esto es así, debes aplicar el mismo algoritmo a al menos dos imágenes con la anomalía a corregir. 

La solución aportada no debe ser básica: repetición de una solución bien conocida o existente en una librería. Se pueden utilizar funcionalidades proporcionadas por las librerías, pero la implementación de la operación principal debe ser propia. No se permite copiar código de Internet. En caso de que se reutilicen ideas deberá referenciarse la fuente.

Extensión: el límite máximo son 6 páginas. [Ver Detalles](./mexmiart02_act1.docx "Ver archivo docx")

## Forma de entrega

Un notebook Python con la solución propuesta y los ficheros adicionales que se necesiten. Adjunta también un PDF donde aparezca toda la ejecución del notebook.

## HFS

- `apt.txt` configura dependencias a instalar sobre el contenedor, ubuntu por default para mybinder.org
- `requirements.txt` configura las dependencias de python sobre el contenedor, se instalan vía pip.
- La carpeta `im` contiene imágenes de ejemplo, se pueden agregar las necesarias.
- La carpeta `out` contendrá los archivos de salida.

## Instalación

Para la instalación local solo corre:

    pip install -r requirements.txt

## Uso

Ver: [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gl/genomorro%2Funir/PC-A1)

Cada proyecto usa archivos `ipynb` y `py` de forma indistinta, gracias a jupytext se pueden sincronizar. Para saber como hacerlo de momento lo mejor es consultar [jupytext](https://jupytext.readthedocs.io/en/latest/index.html "la documentación de jupytext"), después pondré aquí los comandos que use más comúnmente. 

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

