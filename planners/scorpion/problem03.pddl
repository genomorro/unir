(define (problem original)
  (:domain emergency)
  (:objects ambulance hospital L2 L3 L4 L5 L6 L7 patient1 patient2)
  (:init
   (ambulance ambulance)
   (at patient1 L5)
   (at patient2 L6)
   (current hospital)
   (free ambulance)
   (location L2)
   (location L3)
   (location L4)
   (location L5)
   (location L6)
   (location L7)
   (location hospital)
   (path L2 L3)
   (path L2 L4)
   (path L2 L5)
   (path L2 hospital)
   (path L3 L2)
   (path L4 L6)
   (path L5 L7)
   (path L6 L3)
   (path L7 L3)
   (path hospital L2)
   (patient patient1)
   (patient patient2))
  (:goal (and
          (at patient1 hospital)
          (at patient2 hospital))))