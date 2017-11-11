(load "../src/boot")
(reload "../src/lib")

(deftest chars! ()
    "seeking 3 characters"
  (test (nchars 3 #\;) ";;;"))

(deftest doitems! ()
    (let* ((out)
           (lst '(a b c d)))
      (test '((3 . D) (2 . C) (1 . B) (0 . A))
            (doitems (one n lst out)
                (push (cons n one) out)))))


(deftest while! ()
    (let* ((out)
           (lst '(a b c d)))
      (while lst
        (push (cons 'aa (pop lst)) out))
      (test '((aa . D) (aa . C) (aa . B) (aa . A))
            out)))

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
    (with-place (slot tmp x3 y3 z2)
      (+ 21 slot))
    (with-place (slot tmp x3 y3 z3)
      (cons 5555 slot))
    (test '(5555 500 400 300 200 100) (? tmp x3 y3 z3))
    (test 121 (? tmp x3 y3 z2))))

(deftest r2! ()
    (test 0.13 (r2 0.127456)))

(defthing athing thing (a 1) (b 2))

(deftest athing! ()
    (let ((x (make-instance 'athing)))
      (setf (? x a) 2000)
      (test 2000 (? x a))))

(deftest randf! ()
  (let (one two)
    (reset-seed)
    (setf one (round-to (randf) 5))
    (reset-seed)
    (setf two  (round-to (randf) 5))
    (test one two)))
