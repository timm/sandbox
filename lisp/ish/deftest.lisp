(defvar *tests* nil)

(defmacro deftest (name params  &optional (doc "") &body body)
  "Create a defun, adding it name to the list of *tests*."
  (pushnew name *tests*)
  `(defun ,name ,params ,doc
     (format t "~&~%;;; ~a~%" ',name )
     (format t "; ~a~%" ,doc)
     ,@body
     (terpri)))

(let ((pass 0) (fail 0))
  (defun test (want got)
    (cond ((equalp want got) (incf pass))
          (t (incf fail)
             (format t "~&; fail : expected ~a~%" want))))

  (defun tests ()
    (when *tests*
      (print *tests*)
      (mapc #'funcall  (reverse *tests*))
      (format t "~&~%; pass : ~a = ~5,1f% ~%; fail : ~a = ~5,1f% ~%"
         pass (* 100 (/ pass (+ 0.0001 pass fail)))
         fail (* 100 (/ fail (+ 0.0001 pass fail)))))))
