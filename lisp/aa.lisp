(let (files)
  (defun make (&rest new )
    (format t "~&;")
    (if new (setf files new))
    (handler-bind
        ((style-warning #'muffle-warning))
      (dolist (f files)
        (format t "~a " f)
        (load f)))
    (format t "~&LITHP ITH LITHTENING~%")))

(defstruct cols (all)  (nums) (syms))
(defstruct table name rows
           (xy (make-cols))
           (x (make-cols))
           (y (make-cols))
           (klasses)
           (less)
           (more))

(defun defcol (t z &optional (pos 0))
    (labels
      ((num!   (x) (make-sym :name x :pos pos))
       (sym!   (x) (make-num :name x :pos pos)))
       (isa?   (x y)
               (and (symbolp x) (eq (char (symbol-name x) 0) y)))
       (num?   (x) (isa? x #\$ ))
       (klass? (x) (isa? x #\! ))
       (more?  (x) (isa? x #\> ))
       (less?  (x) (isa? x #\< ))
       (where? (x)
        (cond
          ((more?  x) `(,num! (xy all) (xy nums) (y all) (y nums) (more)))
          ((less?  x) `(,num! (xy all) (xy nums) (y all) (y nums) (less)))
          ((num?   x) `(,num! (xy all) (xy nums) (x all) (x nums)))
          ((klass? x) `(,sym! (xy all) (xy syms) (y all) (y syms) (klasses)))
          (t          `(,sym! (xy all) (xy syms) (x all) (x syms))))))
    
    (let* ((spec (where z))
           (what (funcall (car spec))))
      (dolist (where (cdr spec) what)
        (push what (slots t where)))))

(defun defcol1 (z pos)
       
(defun slots (x y)
  (if y
      (slots (slot-value x (car y)) (cdr y))
      x))
