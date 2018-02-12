(pushnew :base *features*)

(let ((seen))
  (defun uses (&rest lst)
    (labels (
      (load1 (f g)
          (format t ";;; ~a~%" g)
          (load g)
          (push f seen))

      (use1 (f)
            (dolist (path +paths+)
              (let* ((g (format nil "~a/~a" path f))
                     (h (format nil "~a.lisp" g)))
                (when (probe-file h)
                  #-sbcl
                  (load1 f g))
                  #+sbcl
                  (handler-bind
                    ((style-warning #'muffle-warning))
                    (load1 f g))
                  (return-from use1)))))))
      (dolist (f lst)
        (when (not (member f seen :test #'equalp))
          (use1 f))))))
