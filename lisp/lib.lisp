(defun nchars (&optional (n 40) (c #\Space))
  (with-output-to-string (s)
    (dotimes (i n)
      (format s "~a" c))))

(defmacro doitems ((one n list &optional out) &body body )
  "Set 'one' and 'n' to each item in a list, and its position."
  `(let ((,n -1))
     (dolist (,one ,list ,out)
       (incf ,n)
       ,@body)))

;(deftest nchars? ()  (test (nchars 3 ".") "..."))

(defun rslots-get (o l)
  (if (cdr l)
      (rslots-get (slot-value o (car l)) (cdr l))
      (slot-value o (car l))))

(defun rslots-set (o l z)
  (setf
   (slot-value o (car l)) 
   (if (cdr l)
       (rslots-set (slot-value o (car l)) (cdr l) z)
       z))
  o)

(defun rslots-push (o l z)
  (setf
   (slot-value o (car l))
   (if (cdr l)
       (rslots-push (slot-value o (car l)) (cdr l) z)
       (push z (slot-value o (car l)))))
  o)

(defmacro ?? (o   &rest l) `(rslots-get  ,o ',l   ))
(defmacro !! (o z &rest l) `(rslots-set  ,o ',l ,z))
(defmacro << (o z &rest l) `(rslots-push ,o ',l ,z))

(defstruct zzzz z1 (z2 0) (z3))
(defstruct yyyy y1 y2 (y3 (make-zzzz)))
(defstruct xxxx x1 x2 (x3 (make-yyyy)))

(defun xxyyzz ()
  (let ((tmp (make-xxxx)))
    (!! tmp 11 x3 y3 z2)
    (dotimes (i 5)
      (<< tmp (+ 100 (* 100 i))  x3 y3 z3))
    (print (?? tmp x3 y3 z3))
    tmp))

(defun make-accessor-field (name form)
  `(,name
    :initarg  ,(intern (symbol-name name) "KEYWORD")
    :initform ,form
    :accessor ,name))

(defmacro defklass (name slot-descriptions)
  `(defclass ,name ()
     ,(loop for (slot-name form) in slot-descriptions
         collect (make-accessor-field slot-name form))))
