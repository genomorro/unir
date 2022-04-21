(define (domain emergency)
  (:predicates
   (ambulance ?a) ; Ambulancia
   (at ?a ?l)     ; Si la ambulancia/paciente está en un lugar
   (carry ?p ?a)  ; Si el paciente está en la ambulancia
   (current ?l)   ; La ubicación current de la ambulancua
   (free ?a)      ; Si está vacía la ambulancia
   (location ?l)  ; Los lugares
   (path ?f ?t)   ; Camino entre dos lugares
   (patient ?p))  ; Paciente
  (:action move
           :parameters (?from ?to)
           :precondition (and
                          (current ?from)
                          (location ?from)
                          (location ?to)
                          (path ?from ?to))
           :effect (and
                    (current ?to)
                    (not (current ?from))))                    
  (:action getinto
           :parameters (?p ?l ?a)
           :precondition (and
                          (ambulance ?a)
                          (at ?p ?l)
                          (current ?l)
                          (free ?a)
                          (location ?l)
                          (patient ?p))
           :effect (and
                    (carry ?p ?a)
                    (not (at ?p ?l))
                    (not (free ?a))))        
  (:action getout
           :parameters (?p ?l ?a)
           :precondition (and
                          (ambulance ?a)
                          (carry ?p ?a)
                          (current ?l)
                          (location ?l)
                          (patient ?p))
           :effect (and
                    (at ?p ?l)
                    (free ?a)
                    (not (carry ?p ?a)))))
