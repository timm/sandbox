(load "../src/boot")
(reload "../src/num")


(deftest num! ()
  "numbers to statistical summary"
  (let ((x (make-instance 'num)))
    (adds x '(9 2 5 4 12 7 8 11 9 3
              7 4 12 5 4 10 9 6 9 4))
    (test 3.06  (r2 (slot-value x 'sd)))
    (test 7.0   (r0 (slot-value x 'mu)))))

(deftest num*! ()
  "convenient summmary of list of numbers"
  (let ((x (num* '(9 2 5 4 12 7 8 11 9 3 7
                   4 12 5 4 10 9 6 9 4)))
        y)
    (test 7.0   (r0 (slot-value x 'mu)))
    (setf y (copy x))
    (adds x '(9 2 5 4 12 7 8 11 9 3
              7 4 12 5 4 10 9 6 9 4))
    (test 40 (slot-value x 'n))
    (test 20 (slot-value y 'n))))


(deftest any! ()
  "checking sampling methods"
  (labels ((srt (lst) (sort lst #'<)))
    (let* ((lst (srt '(9 2 5 4 12 7 8 11 9 3 7
                       4 12 5 4 10 9 6 9 4)))
           (x   (num* lst))
           (y   (srt (loop for i from 1 to 20
                        collect (any x))))
           (z   (srt (loop for i from 1 to 20
                        collect (any x)))))
      (print y)
      (print z))))
    
    
