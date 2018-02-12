#-base (load "base")
(pushnew :dont-test *features*)

(uses
  "listok"
  "stringok"
  "testok"
)
(tests t)
