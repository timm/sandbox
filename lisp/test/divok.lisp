(load   "../src/boot")
(reload "../src/div")

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
  
