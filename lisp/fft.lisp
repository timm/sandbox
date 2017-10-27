(let ((n 0))
  (defstruct num name pos (id (incf n)))
  (defstruct sym name pos (id (incf n))))

(defstruct cols (all)  (nums) (syms))
(defstruct tbl name rows
           (cols)
           (xy (make-cols))
           (x  (make-cols))
           (y  (make-cols))
           (klasses)
           (less)
           (more))

;(defmethod print-object ((x tbl) str)
 ; "Change the print method for a hash."
  ;(format str "(tbl ~a)" (length (tbl-rows x))))

(defun deftable1 (name cols rows)
  (let ((tb (make-tbl :name name :cols cols)))
    (doitems (col pos cols tb)
      (defcol tb col pos))))

(defmacro deftable (name (&rest cols) &body rows)
  `(deftable1 ',name ',cols ',rows))


(defun defcol (tb z pos)
  (labels
    ((num () (make-num :pos pos :name z))
     (sym () (make-sym :pos pos :name z))
     (what-paths ()
       (case (char (symbol-name z) 0)
         (> (values (num) '((xy all) (xy nums) (y all) (y nums) (more)   )))
         (< (values (num) '((xy all) (xy nums) (y all) (y nums) (less)   )))
         ($ (values (num) '((xy all) (xy nums) (x all) (x nums)          )))
         (! (values (sym) '((xy all) (xy syms) (y all) (y syms) (klasses))))
         (t (values (sym) '((xy all) (xy syms) (x all) (x syms)        ))))))
    (multiple-value-bind (what paths)
        (what-paths)
      (dolist (slots paths tb)
        (rslots-push tb slots what)))))

(deftest col1 ()
  (print (defcol1 '$x 0)))

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

    
   
        

