# Actividad grupal: Resolución de un problema mediante búsqueda heurística

- Objetivos de la actividad.
  - Implementar la estrategia de búsqueda heurística A* para la resolución de un problema real.
  
## Descripción de la actividad y pautas de elaboración.

La empresa Amazon desea utilizar un robot para ordenar el inventario de su almacén. Amazon cuenta con tres inventarios (mesa con suministros para vender) localizados en unas posiciones específicas del almacén. El robot se debe encargar de mover los tres inventarios a una posición objetivo.

El robot puede moverse horizontal y verticalmente, y cargar o descargar un inventario. Un ejemplo del robot, moviendo el inventario, se puede observar [en vídeo](https://youtu.be/UtBa9yVZBJM).

## FHS

- La carpeta `writing` contiene el algoritmo seguido a mano.
- Los archivos con nombre `mexmiart04t6actgr` contiene el reporte de la actividad en distintos formatos. El archivo fuente es `mexmiart04t6actgr.org`, desde él se puede incluso ejecutar el código fuente si la configuración de Org-babel es correcta. Se recomienda `mexmiart04t6actgr.pdf` para la lectura.
- `a-star.lisp` contiene el programa hecho en Common Lisp.
- `a-star.out` contiene un log de la ejecución completa del programa.

## Replicar el ejercicio

### Instalación

#### En un sisitema *nix like (GNU/Linux, FreeBSD, MacOS, etc)

1. Instalar desde el gestor de paquetes de su preferencia una implementación de Lisp, por ejemplo SBCL o CLisp. Ejemplo:

	apt install sbcl

2. Instalar Quicklisp tal cual indica su [página de instalación](https://www.quicklisp.org/beta/)

	curl -O https://beta.quicklisp.org/quicklisp.lisp
	sbcl --load quicklisp.lisp
	
Y dentro de sbcl:

	(quicklisp-quickstart:install)

3. (Opcional) Instalar Emacs, configurar la variable `inferior-lisp-program`. Presione las teclas **Alt - :**, verá en la parte inferior de la pantalla el texto **Eval:** y presione:

	(setq inferior-lisp-program "sbcl")
	
	- Abrir el archivo `a-star.lisp`. Presione las teclas **Ctrl - x** seguido de  **Ctrl - f**, al seleccionar el archivo presione **Enter** y verá su contenido.
	
	- Podrá dividir en dos la pantalla (**Ctrl - x 3**) y ejecutar el intérprete de Lisp (**Ctrl - c** y luego **Ctrl - z**).
		
	- Coloque el cursor sobre el nombre de cada instrucción del archivo de Lisp y presione **Ctrl - c** seguido de **Ctrl - e** para ejecutarlo. Verá el nombre de la instrucción reflejada en el intérprete, lo cual indicará que se ha ejecutado correctamente. Un ejemplo de ejecución puede ser visto en `a-star.out`.

## Licencia
This repo is part of Actividades escolares UNIR

Copyright (C) 2021, Edgar Uriel Domínguez Espinoza

Actividades escolares UNIR is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 2 of the License, or (at your option) any later version.

Actividades escolares UNIR is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with Actividades escolares UNIR; if not, see <http://www.gnu.org/licenses/> or write to the Free Software Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301 USA

