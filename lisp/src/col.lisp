(load "../src/boot")
(reload "../src/lib")

(defthing col thing
  (txt "") (pos 0) (n 0) (w 1))
 
(defmethod add1((x col) y &optional f)
  (declare (ignore x y f))
  (assert nil () "add1 should be implemented by subclass"))

(defmethod norm1((x col) y)
  (declare (ignore x y))
  (assert nil () "norm1 should be implemented by subclass"))

(defmethod add ((x col) y &optional (f #'identity))
  (with-slots (n) x
    (when (not (eql y #\?))
      (incf n)
      (add1 (funcall f x) y ))
    y))

(defmethod adds ((x col) (ys cons) &optional (f #'identity))
  (dolist (y ys x)
    (add x y f)))

(defmethod adds ((x col) (ys simple-vector) &optional (f #'identity))
  (loop for y across ys do 
        (add x y f)))
  
(defmethod norm ((x col) y)
  (if (eql y #\?) y (norm1 x y)))
