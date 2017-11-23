(princ "<!----")
(load "~/quicklisp/setup.lisp")
  (ql:quickload "markdown.cl")
(princ "--->")
#|

# here we go

asdasds

- asdas
- asdas



|#
;; (defun string-reader (stream char)
;;    (declare (ignore char))
;;    (let ((*readtable* (copy-readtable)))
;;      (setf (readtable-case *readtable*) :preserve)
;;      (markdown.cl:parse (read-preserving-whitespace stream t nil t))))

;; (set-macro-character #\@ #'string-reader)

;; (print @"

;; # asdas

;; sadassasassassdassa
;; asdas
;; as
;; asd
;; asas

;;      sdfsd
;;      sdfsdfdf


;; bye")
;; (print 1)

(defmacro while (test &body body)
  `(do ()
       ((not ,test))
     ,@body))

(defun header (title)
   (format t
   "<html>
   <head>
   <title>~a</title>
   <script type=\"text/javascript\" src=\"highlight-lisp.js\"></script>
   <link rel=\"stylesheet\" href=\"github.css\">
   </head>
   <body>
   <div class=body>
   " title))

(defun footer ()
  (format t "</div></body></html>"))

(defun render (filename &aux cache finale line)
  (when (probe-file filename)
      (header "title")
      (with-open-file (stream filename)
        (labels ((prefixp (line str &aux (max (length str)))
                   (and (>= (length line) max)
                        (string= str (subseq line 0 max))))
                 (prune (lst)
                   (while (and lst (zerop (length (car lst))))
                     (pop lst))
                   lst)
                 (prep (lst)
                   (prune  lst)
                   (prune (reverse lst))
                   (reverse lst))
                 (code ()
                   (when cache
                     (format t
                        "<div class=lispcode>
                         <pre class=lisp>~{~A~^~%~}</pre></div>~%" 
                        (prep cache))
                     (setf finale #'text
                           cache  nil)))
                 (text ()
                   (when cache
                     (princ
                      (markdown.cl:parse 
                       (format nil "~{~a~%~}~%" (prep cache))))
                     (setf finale #'code
                           cache  nil))))
          (setf finale #'code)
          (while (setf line (read-line stream nil))
            (cond ((prefixp line "#|")  (code))
                  ((prefixp line "|#")  (text))
                  (t                    (push line cache))))
          (funcall finale))
        (footer))))
  

(render "code1.lisp")
