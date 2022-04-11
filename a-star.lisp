;; Instalar  un intérprete  de  Common-Lisp.  Posteriormente seguir  los  pasos  de instalación  de
;; quicklisp y ejecutar el código bloque por bloque.

;; Bloque 1: Preparar el entorno instalar bibliotecas externas
(eval-when (:load-toplevel :compile-toplevel :execute)
  (ql:quickload '("pileup" "iterate")))
;; Bloque 2: Definir el paquete (workspace)
(defpackage :a*-search (:use :common-lisp :pileup :iterate))
;; Bloque 3: Trabajar sobre el paquete
(in-package :a*-search)
;; Bloque 4: Definir el área de trabajo
(defvar *size* 4 "Esta será el tamaño del área, el valor es el lado de un cuadrado.")
;; Bloque 5: Definir la posición de las paredes
(defvar *barriers* '((0 . 1) (1 . 1)) "Esta variable es una lista de cons (X . Y). La posición 0
es la esquina inferior izquierda.")
;; Bloque 6: Que las paredes funcionen como tal
(defvar *barrier-cost* 100 "No es posible evitar que  se inspeccione una pared, pero se eleva el
coste, así se impide su elección.")
;; Bloque 7: Definir los movimientos posibles
(defvar *directions* '((0 . -1) (0 . 1) (1 . 0) (-1 . 0)) "Agregar aquí los posibles movimientos
posibles, de 1 a 8 elementos.")
;; Bloque 8: Definir la carga
(defvar *load* 0 "Si *LOAD* es 0 no hay carga sobre el robot")
;; Bloque 9: Definir nodo
(defstruct (node (:constructor node))
  "Estructura de datos para un nodo de un grafo."
  (pos (cons 0 0) :type cons)
  (path nil)
  (cost 0 :type fixnum)                 ; Coste
  (f-value 0 :type fixnum)              ; Valor de la heurística
  )
;; Bloque 10: Imprime la ruta final
(defun print-path (path start end &optional (barriers *barriers*)
                   &aux (size (+ 2 *size*)))
  "Imprime el área de trabajo.  Identifica PATH por medio de un punto (.),  START con una r, END
con una m y las paredes con una X. Cualquier otro elemento quedará en blanco."
  (format t "~v@{~A~:*~}~%" size "-") ; Borde superior
  ; Área disponible, imprime línea a línea
  (iter (for y from (1- *size*) downto 0)
        (format t "|") ; Margen izquierdo
        ; Columnas
        (iter (for x from 0 below *size*)
              (format t "~A"
                      (cond ((member (cons y x) barriers :test #'equal) "X")
                            ((equal (cons y x) start) "r")
                            ((equal (cons y x) end) "m")
                            ((Member (cons y x) path :test #'equal) ".")
                            (t " "))))
        (format t "|~%")) ; Margen derecho
  (format t "~v@{~A~:*~}~%" size "-") ; Borde inferior
  (iter
    (for position in path)
    (format t "(~D,~D)" (car position) (cdr position))
    (finally (terpri))))
;; Bloque 11: Valida que una posición exista.
(defun valid-position-p (position)
  "Regresa T si POSITION es un punto válido en el mapa."
  (let ((x (car position))
        (y (cdr position))
        (max (1- *size*)))
    (and (<= 0 x max)
         (<= 0 y max))))
;; Bloque 12: Movimiento en una dirección
(defun move (position direction)
  "Regresa un nuevo punto cuando se mueve POSITION en una DIRECTION. Asume posiciones válidas."
  (let ((x (car position))
        (y (cdr position))
        (dx (car direction))
        (dy (cdr direction)))
    (format t "Posición posible: (~D . ~D)~%" (+ x dx) (+ y dy))
    (cons (+ x dx) (+ y dy))))
;; Bloque 13: Determina posiciones posibles dada la posición actual
(defun next-positions (current-position)
  "Regresa una lista con los posibles posiciones siguientes."
  (remove-if-not #'valid-position-p
                 (mapcar (lambda (d) (move current-position d)) *directions*)))
;; Bloque 14: La heurística
(defun distance (current-position goal)
  "Calcula la distancia Manhattan existente desde CURRENT-POSITION hasta GOAL."
  (+ (abs (- (car goal) (car current-position)))
     (abs (- (cdr goal) (cdr current-position)))))
;; Bloque 15: Algoritmo A*
(defun a* (start goal heuristics next &optional (information 0))
  "Calcula la ruta más corta de START a GOAL usando HEURISTICS. Genera la lista de caminos
usando NEXT. Si INFORMATION es 1 se imprimirán detalles de cada iteración."
  (let ((visited (make-hash-table :test #'equalp))) ; Crea la lista cerrada. Nodos visitados
    (flet ((pick-next-node (queue)
             ; Obtiene el primer elemento que forma la cola
             (heap-pop queue))
           (expand-node (node queue)
             ; Expande los nodos de posible avance y los agrega a la cola si no han
             ; sido visitados.
             (iter
               (with costs = (node-cost node))
               (for position in (funcall next (node-pos node)))
               (for cost = (1+ costs))
               (for f-value = (+ cost (funcall heuristics position goal)
                                 (if (member position *barriers* :test #'equal)
                                     100
                                     0)))
               ; Revisa si el nodo ha sido visitado
               (unless (gethash position visited)
               ; Agrega el nodo a la cola
               (heap-insert
                (node :pos position :path (cons position (node-path node))
                      :cost cost :f-value f-value)
                queue)))))
      ; La búsqueda algoritmica
      (iter
        ;; Crea la cola
        (with queue = (make-heap #'<= :name "queue" :size 1000 :key #'node-f-value))
        (with initial-cost = (funcall heuristics start goal))
        (initially (heap-insert (node :pos start :path (list start) :cost 0
                                      :f-value initial-cost)
                                queue))
        (for counter from 1)
        (for current-node = (pick-next-node queue))
        (for current-position = (node-pos current-node))
        ; Imprime información sobre la iteración
        (when (and (not (zerop information))
                   (zerop (mod counter information)))
          (format t "Nodo ~D, tamaño de la lista abierta: ~D, coste actual: ~D~%"
                  counter (heap-count queue)
                  (node-cost current-node)))
        ; Si la posición actual no es GOAL continua
        (until (equalp current-position goal))
        ; Agrega el nodo actual a la lista de visitados
        (setf (gethash current-node visited) t)
        ; Expande el nodo actual
        (expand-node current-node queue)
        (finally (return (values (nreverse (node-path current-node))
                                 (node-cost current-node)
                                 counter)))))))
;; Bloque 16: El robot
(defun robot (start package goal &key (heuristics #'distance))
  "Define el movimiento de un robot el cual se ubica en START, se mueve y recoge un inventario
en PACKAGE y lo lleva hasta GOAL."
  (multiple-value-bind (path cost steps)
      (a* start package heuristics #'next-positions 1)
    (format t "La ruta entre el punto inicial (r) al punto final (m) en ~D pasos con coste: ~D~%" steps cost)
    (print-path path start package))
  (setq *load* 1)
  (format t "Carga del robot: ~D~%" *load*)
  (multiple-value-bind (path cost steps)
      (a* package goal heuristics #'next-positions 1)
    (format t "La ruta entre el punto inicial (r) al punto final (m) en ~D pasos con coste: ~D~%" steps cost)
    (print-path path package goal))
  (setq *load* 0)
  (format t "Carga del robot: ~D~%" *load*)  
  )
;; Bloque 17: Ejecución, cada instrucción se debe a un problema, evaluar línea por línea
(robot '(2 . 2) '(0 . 0) '(3 . 3)) ; P1: 4 + 6

(robot '(2 . 2) '(2 . 0) '(3 . 2)) ; P2: 2 + 3

(robot '(2 . 2) '(0 . 3) '(3 . 1)) ; P3: 3 + 5
