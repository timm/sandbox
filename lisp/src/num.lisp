(load "../src/boot")
(reload "../src/col")

(defthing num col
  (mu 0) (m2 0) (sd 0) (rank 0)
  (lo most-positive-fixnum)
  (hi most-negative-fixnum))

(defmethod add1 ((x num) y &optional (f #'identity))
  (with-slots (hi lo n mu m2 sd) x
    (let* ((y     (funcall f y))
           (delta (- y mu)))
      (setf lo (min lo y)
            hi (max hi y)
            mu (+ mu (/ delta n))
            m2 (+ m2 (* delta (- y mu))))
      (if (> n 1)
          (setf sd (sqrt (/ m2 (- n 1))))))))

(defun num* (lst &optional (f #'identity))
  (adds (make-instance 'num) lst f))

(defmacro copier (old new &rest fields)
  `(with-slots ,fields ,old
     ,@(mapcar #'(lambda (slot)
                        `(setf (slot-value ,new ',slot) ,slot))
               fields)
     ,new))

(defmethod copy ((old num))
  (let ((new (make-instance 'num)))
    (copier old new n sd mu m2 lo hi)))
     
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

