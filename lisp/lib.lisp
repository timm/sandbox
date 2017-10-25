(defun nchars (&optional (n 40) (c #\Space))
  (with-output-to-string (s)
    (dotimes (i n)
      (format s "~a" c))))

(deftest nchars? ()
  (test (nchars 3 ".") "..."))


(defun make-accessor-field (name form)
    `(,name
           :initarg  ,(intern (symbol-name name) "KEYWORD")
	       :initform ,form
	           :accessor ,name))

(defmacro defclass-with-accessors (name slot-descriptions)
    `(defclass ,name ()
            ,(loop for (slot-name form) in slot-descriptions
		               collect (make-accessor-field slot-name form))))
