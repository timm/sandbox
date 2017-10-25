(define-record-type table (fields
                           (mutable x)
                           y))

#|
(make-point x y)  ;constructor
(point? obj)  ;predicate
(point-x p)  ;accessor for field x
(point-y p)  ;accessor for field y
|#

;With this definition in place, we can use these
;procedures to create and manipulate records of the
;point type, as illustrated below.

(define (nth n l)
  (if (eq? n 0)
      (car l)
      (nth (- n 1) (cdr l))))

(define-record xy
  ((all 23)))

(define-record table
  name
  (rows (list))
  (cols 

(define weather
  (table
   fred
   (aa bb cc dd)
   (sunny 85 85 FALSE no)
   (sunny 80 90 TRUE no)
   (overcast 83 86 FALSE yes)
   (rainy 70 96 FALSE yes)
   (rainy 68 80 FALSE yes)
   (rainy 65 70 TRUE no)
   (overcast 64 65 TRUE yes)
   (sunny 72 95 FALSE no)
   (sunny 69 70 FALSE yes)
   (rainy 75 80 FALSE yes)
   (sunny 75 70 TRUE yes)
   (overcast 72 90 TRUE yes)
   (overcast 81 75 FALSE yes)
   (rainy 71 91 TRUE no)))

(define (table! name cols . rows)
  (let ((t (make-table)
    (table! 0
    (make-table 

          (length '(1 2 3))
          
