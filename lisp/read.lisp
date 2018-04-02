(defun circular (items)
  (setf (cdr (last items)) items)
  items)

(defun flatten (obj)
  (let (result)
    (labels (
       (grep (obj)
          (cond ((null obj) nil)
                ((atom obj) (push obj result))
                (t (grep (rest obj))
                   (grep (first obj))))))
      (grep obj)
      result)))

(defun pair (tag s &optional klass nl) 
  (if klass
    (if nl
      (format nil "~%<~a class=~a>~a~%</~a>" tag klass s tag)
      (format nil "<~a class=~a>~a</~a>"     tag klass s tag))
    (if nl
      (format nil "~%<~a>~a~%</~a>" tag s tag)
      (format nil "<~a>~a</~a>"     tag s tag))))

(defun pairln (tag s &optional klass) (pair tag s klass t))

(defmacro cat (&rest lst)
  `(concatenate 'string ,@lst))

(defun page (s)
  (format t "~{~a~}" (flatten s)))

(defun html (the-title s) 
  (pairln "html" 
        (cat (head (title the-title))
             (body (div (div s "main") "wrapper")))))

(defun head (s) (pairln "head" s))
(defun title (s) (pair "title" s))
(defun body (s) (pairln "body" s))
(defun div (s &optional klass) (pairln "div" s klass))
(defun h1 (s) (pairln "h1" s))
(defun h2 (s) (pairln "h2" s))
(defun h3 (s) (pairln "h3" s))
(defun p  (s) (pairln "p" s))
(defun em (s) (pair "em" s))
(defun b  (s) (pair "b"  s))
(defun li (s &optional klass) (pairln "li" s klass))
(defun odds (s) (li s "odd"))
(defun evens (s) (li s "even"))

(defun oul (what lst) 
  (let ((rows (circular (list #'odds #'evens))))
    (labels ((row (s) (funcall (pop rows) s)))
      (pairln what (mapcar #'row lst)))))

(defun ol (&rest lst) (oul "ol" lst))
(defun ul (&rest lst) (oul "ul" lst))
(defun href (url str) (format nil "<a href=\"~a\">~a</a>" url str))

(defun my-string-reader (stream char)
  (declare (ignore char))
  (let ((*readtable* (copy-readtable nil)))
    (setf (readtable-case *readtable*) :preserve)
    (read stream t nil t)))

(set-macro-character #\% #'my-string-reader )

(page  
  (html 
    %"My Home's Page"
    (list  
      (h1 %"ido drugs")
      (p %"I like traffic Light's")
      (ol %"One suff"
          %"Two Stuffer"
          %"Tthree Lover"
          ))))
