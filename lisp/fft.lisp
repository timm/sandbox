; # Head
; 
; Text to get is starated
#|
Here some more
|#

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;;; col

(defthing col thing
  (txt "") (pos 0) (n 0) (w 1))
 
(defmethod add1((x col) y)
  (assert nil () "add1 should be implemented by subclass"))

(defmethod norm1((x col) y)
  (assert nil () "norm1 should be implemented by subclass"))

;; vvariance(samples):
;;   M := 0
;;   S := 0
;;   for k from 1 to N:
;;     x := samples[k]
;;     oldM := M
;;     M := M + (x-M)/k
;;     S := S + (x-M)*(x-oldM)
;; return S/(N-1)

(defun ndiv (lst &optional (x #'first) (y x) &key (divs 32) (min 20))
  (let ((lst    (sort lst #'(lambda (a b) (< (funcall x a)
                                             (funcall x b)))))
        (size   (max min (floor (/ (length lst) divs))))
        (lsts   (msubs lst size))
        (out))
    (ndiv1 lsts x y out)
    out))

(defun walk (lsts y &aux out (summary (make-instance 'num)))
    (dolist (lst lsts out)
      (dolist (one list)
        (add summary (funcall y one)))
      (push (copy summary) out)))

(defun ndiv1 (lsts x y out)
  (let* (cut
         (n      (length lst))
         (best   most-positive-fixnum)         
         (belows (walk lsts))
         (aboves (walk (reverse lsts)))
         (i      0))
    (mapc #'(lambda (below above)
              (let ((here (+ (nsd below n) (nsd above n))))
                (if (and (< here best)
                         (< (slot-value below 'mu)
                            (slot-value above 'mu)))
                    (setf best here
                          cut  (incf i)))))
            belows aboves)
    (cond ((cut (ndiv1 (subseq lsts 0 cut) x y out)
                (ndiv1 (subseq lsts cut  ) x y out))
           (t   (push lsts out)))))) 

(deftest ndiv? ()
  (ndiv '(40 30 20 10) #'first #'first))

(defmethod add ((x col) y)
  (with-slots (n) x
    (when (not (eql y #\?))
      (incf n)
      (add1 x y))
    y))

(defmethod adds ((x col) ys)
  (dolist (y ys x) (add x y)))

(defmethod norm ((x col) y)
  (if (eql y #\?) y (norm1 x y)))

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;;; num

(defmethod add1 ((x num) y)
  (with-slots (hi lo n mu m2 sd) x
    (let ((delta (- y mu)))
      (setf lo (min lo y)
             hi (max hi y)
             mu (+ mu (/ delta n))
             m2 (+ m2 (* delta (- y mu))))
      (if (> n 1)
          (setf sd (sqrt (/ m2 (- n 1))))))))

(defthing num col
  (mu 0) (m2 0) (sd 0)
  (lo most-positive-fixnum)
  (hi most-negative-fixnum)) 

(defmacro copier (old new &rest fields)
  `(with-slots ,fields ,old
     ,@(mapcar #'(lambda (slot)
                        `(setf (slot-value ,new ',slot) ,slot))
               fields)
     ,new))

(defmethod copy ((old num))
  (let ((new (make-instance 'num)))
    (copier old new n sd mu m2)))
     
(defmethod print-object ((x num) src)
  (with-slots (n pos txt w mu m2 lo hi) x
    (format src "~a"
      `((n  . ,n) (pos . ,pos) (txt . ,txt) (w  . ,w)
        (mu . ,mu) (m2 . ,m2)  (lo  . ,lo)  (hi . ,hi)))))
  
(defmethod nsd ((x num) &optional (n 1))
  (* (slot-value x 'sd) (/ (slot-value x 'n) n)))

(defmethod any ((x num) &aux x1 x2 (w 1))
  (while (>= w 1)
      (setf x1 (- (* 2 (randf) 1))
            x2 (- (* 2 (randf) 1))
            w  (+ (* x1 x1) (* x2 x2))))
  (with-slots (mu sd) x
    (+ mu (* sd w x1 (sqrt (/ (* -2 (log w)) w))))))

(deftest col? ()
  (let ((x (make-instance 'num)))
    (adds x '(9 2 5 4 12 7 8 11 9 3 7 4 12 5 4 10 9 6 9 4))
    (test 3.06  (r2 (slot-value x 'sd)))
    (test 7.0   (r0 (slot-value x 'm)))))
        
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;;; deftable

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

    
   
        

