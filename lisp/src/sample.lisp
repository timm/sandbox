#|

## Loading

|#
(load "../src/boot")
(reload "../src/col")
#|

## Samples

RLeservoir sampling.

|#

(let ((max 256))
  (defthing sample thing
    (now   -1)
    (sorted nil)
    (most   max)
    (all    (make-array max :initial-element nil))))

(defmethod add1 ((x sample) y &optional (f #'identity))
  (with-slots (size max all sorted) x
    (let ((pos (cond
                 ((< size (1- max))      (incf size))
                 ((< (randf) (/ size n)) (randi max)))))
      (setf (aref all pos) (funcall f y)
            sorted nil))))

(defun sample* (lst &optional (f #'identity))
  (adds (make-instance 'sample) lst f))

(defmethod copy ((old num))
  (let ((new (make-instance 'sample)))
    (copier old new max n)
    (setf (slot-value new 'all)
          (copy-list (slot-value old 'all)))))
     
(defmethod print-object ((x sample)  src)
  (with-slots (n pos txt w mu m2 lo hi) x
    (format
     src "~a"
     `(sample (n   . ,(? x n))
              (all . ,(length (? x all)))))))

(defmethod any ((x sample))
  (aref (? x all)
        (random (length *list*)) *list*))  
  (while (>= w 1)
      (setf x1 (- (* 2 (randf) 1))
            x2 (- (* 2 (randf) 1))
            w  (+ (* x1 x1) (* x2 x2))))
  (with-slots (mu sd) x
    (+ mu (* sd w x1 (sqrt (/ (* -2 (log w)) w))))))

