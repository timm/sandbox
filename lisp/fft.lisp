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
  (let ((pos -1)
        (tbl (make-tbl :name name :cols cols)))
    (labels
        ((one (col) (defcol tbl col (incf pos))))
      (mapc #'one cols)
      tbl)))

(defmacro deftable (name (&rest cols) &body rows)
  `(deftable1 ',name ',cols ',rows))

(defun defcol1 (z pos)
  (labels
      ((num (y) (cons (make-num :name z :pos pos) y))
       (sym (y) (cons (make-sym :name z :pos pos) y))
       (is  (y) (eq (char (symbol-name z) 0) y)))
    (cond
      ((is #\>) (num '((xy all) (xy nums) (y all) (y nums) (more)    )))
      ((is #\<) (num '((xy all) (xy nums) (y all) (y nums) (less)    )))
      ((is #\$) (num '((xy all) (xy nums) (x all) (x nums)           )))
      ((is #\!) (sym '((xy all) (xy syms) (y all) (y syms) (klasses) )))
      (t        (sym '((xy all) (xy syms) (x all) (x syms)        ))))))

(deftest col1 () (print (defcol1 '$x 0)))

(defun defcol (tbl z pos)
  (let* ((spec (defcol1 z pos))
         (obj  (car spec))
         (path (cdr spec)))
    (dolist (slots path tbl)
      (let ((place tbl))
        (dolist (slot slots)
          (print slot)
          (setf place (slot-value place slot)))
        (push obj place)))))

