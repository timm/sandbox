; # Head
; 
; Text to get is starated
#|
Here some more
|#

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;;; col

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;;; num

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;;; defcol


;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;;; deftable

(defthing  cols thing
  (all) (nums) (syms))

(defthing table thing
  (xy (make-instance 'cols))
  (x  (make-instance 'cols))
  (y  (make-instance 'cols)))
  
(defun deftable1 (name cols rows)
  (let ((tb (make-instance 'tbl :name name :cols cols)))
    (doitems (col pos cols tb)
      (defcol tb col pos))))

(defmacro deftable (name (&rest cols) &body rows)
  `(deftable1 ',name ',cols ',rows))

(defun defcol (tb name pos)
  (labels
   ((num () (make-instance 'num :name name :pos pos))
    (sym () (make-instance 'sym :name name :pos pos))
    (doit (col list-of-slots)
          (dolist (slots list-of-slots)
            (change
             (lambda (slot) (cons col slot))
             tb slots))))
   (case
        (char (symbol-name name) 0)
      (#\> (doit (num) '((xy all) (xy nums) (y all) (y nums) (more)   )))
      (#\< (doit (num) '((xy all) (xy nums) (y all) (y nums) (less)   )))
      (#\$ (doit (num) '((xy all) (xy nums) (x all) (x nums)          )))
      (#\! (doit (sym) '((xy all) (xy syms) (y all) (y syms) (klasses))))
      (t   (doit (sym) '((xy all) (xy syms) (x all) (x syms)       ))))))

;(deftest col1 ()
 ; (let ((tb (make-tbl)))
  ; (print (defcol tb '$x 0))
   ; tb))

(deftest defcol? ()
  (let* ((tb   (make-instance 'table))
         (eg  `((aa    $bb $cc dd !ee)
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
         (cols  (car eg)))
    (doitems (z pos cols tb)
      (defcol tb z pos))))

    
   
        

