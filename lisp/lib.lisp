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


;;;; Simple access/update to recursive slots in LISP
;;;; Tested on defstructs. Should also work on instances.
;;;; Tim@menzies.us, Oct 2017 
;;;; Builds on some excellent code from "Barmar", https://goo.gl/SQtNHd
(defun change (f obj slots)
  "Use case 1: access path for slots not known till runtime.
   In this case, pass in a function 'f' that will be used to
   update the slot found after travesing all the slots."
  (if (cdr slots)
      (change f (slot-value obj (car slots)) (cdr slots))
      (setf (slot-value obj (car slots))
            (funcall f (slot-value obj (car slots))))))

(defmacro ? (obj first-slot &rest more-slots)
  "From https://goo.gl/dqnmvH.
   Use case 2: access path known at load time.
   In this case, pre-compute the access path as a macro."
  (if (null more-slots)
      `(slot-value ,obj ',first-slot)
      `(? (slot-value ,obj ',first-slot) ,@more-slots)))

;;; Test code

;; "(make-xxxx)" creates a recursive set of structs.
(defstruct zzzz z1 (z2 0) (z3))
(defstruct yyyy y1 y2 (y3 (make-zzzz)))
(defstruct xxxx x1 x2 (x3 (make-yyyy)))

(defun xyz-demo ()
  (let ((tmp (make-xxxx)))
    (incf (? tmp  x3 y3 z2) 100)
    (dotimes (i 5)
      (push (+ 100 (* 100 i))  (? tmp x3 y3 z3)))
    (change (lambda (slot) (1+ slot))
       tmp '(x3 y3 z2))
    (change (lambda (slot) (cons 5555 slot))
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
