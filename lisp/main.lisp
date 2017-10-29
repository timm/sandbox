(progn
  (let (wants)
    (defun ith (&rest new )
      (if new (setf wants new))
      (handler-bind
          ((style-warning #'muffle-warning))
        (dolist (want wants 'LITHP-ITH-LITHTENING)
          (format t ";loading ~a ...~%" want)
          (load want)))))
  
  (ith "deftest"
       "lib"
       "fft")
)
