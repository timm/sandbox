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

(defmacro while (test &body body)
  `(do ()
       ((not ,test))
     ,@body))

(defmacro slots (obj &rest names)
  `(mapcar #'(lambda (name) (cons name (slot-value ,obj name))) ',names))

; (msubs '(1 2 3 4 4 5 5 5 5 5 8 9 0 10 11 12 13 14 16 17 18) 3 10)
; need to make sins different
(defun msubs (lst &optional (m 20) (epsilon 0) (f #'identity))
  (msubs1 (sort lst #'(lambda (a b)
                        (< (funcall f a)  (funcall f b))))
          m epsilon f))

(defun msubs1 (lst m epsilon f) 
  (let ((tmp)
        (first (car lst))
        (counter m))
    (while ; pop m items items
        (and (>= (decf counter) 0) lst)
      (push (pop lst) tmp))
    (while 
        (let ((first   (funcall f first))
              (current (funcall f (car tmp)))
              (next    (funcall f (car lst))))
          (or
           (< (- current first) epsilon)
           (eql current next)))
      (push (pop lst) tmp))
    (cond  ((< (length lst) m) (while lst
                                 (push (pop lst) tmp))
                               (list tmp))
           (t  (cons tmp
                     (msubs1 lst m epsilon f))))))
    
(defun round-to (number precision &optional (what #'round))
    (let ((div (expt 10 precision)))
      (float (/ (funcall what (* number div)) div))))

(defun r2 (n) (round-to n 2))

(defun r0 (n) (round-to n 0))

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

(defmacro dochange ((slot obj &rest slots) &rest body)
  `(changex #'(lambda (,slot) ,@body)
            ,obj ',slots))

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


(defun defslot  (name form)
  `(,name
    :initarg  ,(intern (symbol-name name) "KEYWORD")
    :initform ,form
    :accessor ,name))

(defclass thing () ())

(defmacro  defthing (x parent &rest slots)
  `(defclass ,x (,parent)
     ,(loop for (x form) in slots collect (defslot x form))))

(let* ((seed0      10013)
       (seed       seed0)
       (multiplier 16807.0d0)
       (modulus    2147483647.0d0))
  (defun reset-seed ()  (setf seed seed0))
  (defun randf      (&optional (n 1)) (* n (- 1.0d0 (park-miller-randomizer))))
  (defun randi      (&optional (n 1)) (floor (* n (/ (randf 1000.0) 1000))))
  (defun park-miller-randomizer ()
    "cycle= 2,147,483,646 numbers"
    (setf seed (mod (* multiplier seed) modulus))
    (/ seed modulus))
)

