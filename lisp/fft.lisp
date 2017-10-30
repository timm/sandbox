; # Head
; 
; Text to get is starated
#|
Here some more
|#
(defthing col
  (txt "") (pos 0) (n 0) (w 1))



(defmethod add ((x col) y)
  (when (not (eql y #\?))
    (incf (slot-value x) 'n)
    (add1 y)
    y))

(defmethod adds ((x col) ys) (dolist (y ys y) (add y)))

(defmethod norm ((x col) y)
  (if (eql y #\?)
      y
    (norm1 x y)))

(defklass num col
  (mu 0) (m2 0)
  (lo most-positive-fixnum)
  (hi most-negative-fixnum))

(defmethod add1 ((x num) y)
  (with-slots  (hi lo n mu m2) x
    (let ((delta (- y mu)))
      (setf lo (min lo y)
            hi (max hi y)
            mu (+ mu (/ delta n))
            m2 (+ m2 (* delta (- x mu))))
      (if (> n 1)
          (setf sd (/ m2 (- n 1)))))))
          


(let ((n 0))
  (defstruct num name pos (n 0) (mu 0) (m2 0) (id (incf n)))
  (defstruct sym name pos (id (incf n))))

(defmethod add ((i num) y)
  (with-slots (n mu m2) i
    (incf n)))
    
  
(defstruct cols (all)  (nums) (syms)) 
(defstruct tbl name rows
           (cols)
           (xy (make-cols))   
           (x  (make-cols))
           (y  (make-cols)) 
           (klasses) 
           (less)
           (more))

; # More Test
;
; and more
; asas

;(defmethod print-object ((x tbl) str)
 ; "Change the print method for a hash."
  ;(format str "(tbl ~a)" (length (tbl-rows x))))

                                        ; # FFT
; Stuff to tell
(defun deftable1 (name cols rows)
  (let ((tb (make-tbl :name name :cols cols)))
    (doitems (col pos cols tb)
      (defcol tb col pos))))

(defmacro deftable (name (&rest cols) &body rows)
  `(deftable1 ',name ',cols ',rows))

(defun defcol (tb name pos &aux (num #'make-num) (sym #'make-sym))
  (labels
      ((doit (maker list-of-slots)
         (let ((col (funcall maker :name name :pos pos)))
           (dolist (slots list-of-slots)
             (change
              (lambda (slot) (cons col slot))
              tb slots)))))
    (case
        (char (symbol-name name) 0)
      (#\> (doit num '((xy all) (xy nums) (y all) (y nums) (more)   )))
      (#\< (doit num '((xy all) (xy nums) (y all) (y nums) (less)   )))
      (#\$ (doit num '((xy all) (xy nums) (x all) (x nums)          )))
      (#\! (doit sym '((xy all) (xy syms) (y all) (y syms) (klasses))))
      (t (doit sym '((xy all) (xy syms) (x all) (x syms)       ))))))

(deftest col1 ()
  (let ((tb (make-tbl)))
    (print (defcol tb '$x 0))
    tb))

(deftest defcol? ()
  (let* ((tb   (make-tbl))
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

    
   
        

