(defun nchars (&optional (n 40) (c #\Space))
  (with-output-to-string (s)
    (dotimes (i n)
      (format s "~a" c))))

(deftest nchars? ()
  (test (nchars 3 ".") "..."))
