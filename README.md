# UNIR

Esquema de trabajo para proyectos de la UNIR. En cada rama hay un trabajo nuevo, en `main` las plantillas para cada uno de ellos.

Esta rama contiene un ejercicio de openCV:
```
El Reto  consiste en:

Instalar Anaconda (https://www.anaconda.com/products/individual (Enlaces a un sitio externo.) )
Instalar OpenCV en Anaconda (https://anaconda.org/conda-forge/opencv (Enlaces a un sitio externo.) )
Abrir un Notebook de Jupyter
Importar una imagen con OpenCV (220px-Lenna_(test_image).png)
Convertir la imagen a escala de grises (puedes utilizar la función de OpenCV o implementar algún algoritmo)
Desplegar la imagen original
Desplegar la imagen en escala de grises
Aplicar el algoritmo del filtro de mediana sin utilizar bibliotecas (algoritmo implementado por ti mismo)
Desplegar la imagen con el filtro aplicado.
Seleccionar dos imágenes de tu elección y aplicar tu algoritmo del filtro de mediana.
En el Foro colocar las imágenes que seleccionaste y las imágenes con los filtros. No es necesario compartir el notebook de Jupyter solo las imágenes a las cuales le aplicaste el algoritmo. Recuerda documentar tu notebook. 
Puedes usar Colab (basado en Notebook de Jupyter) y compartir el link si así lo deseas (no es necesario).

 

  

  Si hay dudas consulten lo siguiente:

  https://visionyrobotica.com/convertir-imagen-rgb-escala-de-grises/ (Enlaces a un sitio externo.)

   

   https://docs.opencv.org/4.x/d6/d00/tutorial_py_root.html (Enlaces a un sitio externo.)

    

    Rafael C. González, Richard E. Woods 1996 Tratamiento digital de imágenes, (Addison-Wesley Iberoamericana S.A. y Ediciones Días de Santos S.A.)  
```


## Nombre

Cada rama se compone por las iniciales de una materia, sigue un guion y las iniciales de una actividad. Por ejemplo:

    PC-R1 = Percepción Computacional, Reto 1

## Descripción

- `apt.txt` configura dependencias a instalar sobre el contenedor, ubuntu por default para mybinder.org
- `requirements.txt` configura las dependencias de python sobre el contenedor, se instalan vía pip.
- La carpeta `im` contiene imágenes de ejemplo, se pueden agregar las necesarias.
- La carpeta `out` contendrá los archivos de salida.
- La carpeta `ds` contendrá los archivos datasets de entrada.

## Instalación

Para la instalación local solo corre:

    pip install -r requirements.txt

## Uso

Ver: [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gl/genomorro%2Funir/PC-R1)

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

