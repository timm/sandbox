;; (defun ndiv1 (lsts x y out)
;;   (let* ((cut)
;;          (n      (length lst))
;;          (best   most-positive-fixnum)         
;;          (belows (walk lsts))
;;          (aboves (walk (reverse lsts)))
;;          (i      0))
;;     (mapc #'(lambda (below above)
;;               (let ((here (+ (nsd below n) (nsd above n))))
;;                 (if (and (< here best)
;;                          (< (slot-value below 'mu)
;;                             (slot-value above 'mu)))
;;                     (setf best here
;;                           cut  (incf i)))))
;;             belows aboves)
;;     (cond ((cut (ndiv1 (subseq lsts 0 cut) x y out)
;;                 (ndiv1 (subseq lsts cut  ) x y out))
;;            (t   (push lsts out)))))) 

;; (deftest ndiv? ()
;;   (ndiv '(40 30 20 10) #'first #'first)) 



;;;;;;;;;;;;;;;;;
(defun ranges1 (lst &key  (n 20) (epsilon 1) (f #'identity))
  (let ((tmp)
        (first   (car lst))
        (counter n))
    (while (and lst (>= (decf counter) 0))
      (push (pop lst) tmp))
    (while (and lst
                (let ((first    (funcall f first))
                      (current  (funcall f (car tmp)))
                      (next     (funcall f (car lst))))
                  (or
                   (< (- current first) epsilon)
                   (eql current next))))
      (push (pop lst) tmp))
    (cond ((< (length lst) n)  (while lst
                                 (push (pop lst) tmp))
                               (list tmp))
          (t (cons tmp
                   (ranges1 lst :n n :epsilon epsilon :f f))))))

(defun ranges (lst &key  (n 20) (epsilon 1) (f #'identity))
  (ranges1
   (sort lst #'(lambda (a b)  (< (funcall f a) (funcall f b))))
   :n n :epsilon epsilon :f f))

(deftest ranges! ()
  "Want 3, then 5,  lists"
  (let* ((lst '(10 20 30 11 21 31 12 22
                32 13 23 33 14 24 34))
         (l5   (ranges lst :n  5))
         (l3   (ranges lst :n  3)))
    (print `(l5 ,l5))
    (print `(l3 ,l3))
    (test (length l5) 3)
    (test (length l3) 5)))

(defun ranges-cdf (ranges f)
  (let ((out)
        (sofar (make-instance 'num)))
    (dolist (range ranges (reverse out))
      (dolist (one range)
        (push (funcall f one) range))
      (push (copy sofar) out))))

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
(defun superranges1 (arr f epsilon &aux (out) )
  "split array at point that minimized expected value of sd"
  (macrolet ((at (n v) `(slot-value (aref arr ,n) ,v)))
    (labels
        ((sd  (b4 z)
           (* (at z 'sd)
              (/ (at z 'n) (at b4 'z))))                        
         (all (lo hi &aux (out (make-instance 'num)))
             (loop for j from lo to hi do
                  (adds out (aref arr j) f)
                return out))
         (argmin (lo hi &aux cut (best most-positive-fixnum))
           (if (< lo hi)
               (let ((b4 (all lo hi)))
                 (loop for j from lo to (1- hi) do
                      (let* ((l   (all 0      j))
                             (r   (all (1+ j) hi))
                             (now (+ (sd b4 l) (sd b4 r))))
                        (if (< now best)
                            (if (> (- (at r 'mu) (at l 'mu))
                                   epsilon)
                                (setf best now
                                      cut   j)))))))
           cut)
         (split (hi lo &aux (cut (argmin lo hi)))
           (cond (cut  (split 0        cut)
                       (split (1+ cut)  hi))
                 (t    (push (subseq arr lo hi) out)))))
      (split 0 (1- length arr))
      out)))

(defun superranges (lst &key (n 20) (xepsilon 0) (cohen 0.2)
                          (x #'first) (y #'second))
  "Split x-values in ranges; combine ranges that do not alter y.
   Returns an array of array of numbers"
  (let* ((arr      (l->a
                    (ranges lst :n n :epsilon xepsilon :f x)))
         (yepsilon (* cohen
                      (slot-value (num* lst y) 'sd))))
    (superranges1 arr y yepsilon)))

(deftest superranges! ()
  "Want 3, then 5,  lists"
  (let* ((lst '(10 20 30 11 21 31 12 22
                32 13 23 33 14 24 34))
         (l5   (superranges lst :n  5 :x #'identity :y #'identity))
         (l3   (superranges lst :n  3 :x #'identity :y #'identity)))
    (print `(l5 ,l5))
    (print `(l3 ,l3))
    (test (length l5) 3)
    (test (length l3) 5)))
  
