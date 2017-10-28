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

(defun change (f obj slots)
  (setf (slot-value obj (car slots))
        (if (cdr slots)
            (change f (slot-value obj (car slots)) (cdr slots))
            (funcall f (slot-value obj (car slots)))))
  obj)

(defmacro ! (f obj &rest slots)
  `(change ,f ,obj ',slots))

(defmacro ? (obj first-slot &rest more-slots)
  "From https://goo.gl/dqnmvH"
  (if (null more-slots)
      `(slot-value ,obj ',first-slot)
      `(? (slot-value ,obj ',first-slot) ,@more-slots)))
  
(defmacro ?? (o   &rest l) `(rslots-get  ,o ',l   ))
(defmacro !! (o z &rest l) `(rslots-set  ,o ',l ,z))
(defmacro << (o z &rest l) `(rslots-push ,o ',l ,z))

(defstruct zzzz z1 (z2 0) (z3))
(defstruct yyyy y1 y2 (y3 (make-zzzz)))
(defstruct xxxx x1 x2 (x3 (make-yyyy)))

(defun xyx-demo ()
  (let ((tmp (make-xxxx)))
    (incf (? tmp  x3 y3 z2) 100)
    (dotimes (i 5)
      (push (+ 100 (* 100 i))  (? tmp x3 y3 z3)))
    (change (lambda (slot) (incf slot))
       tmp '(x3 y3 z2))
    (change (lambda (slot) (push 5555 slot))
       tmp '(x3 y3 z3))
    (print (? tmp x3 y3 z3))
    (print (? tmp x3 y3 z2))
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
