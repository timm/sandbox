# vim: ft=awk:ts=2 sw=2 sts=2 expandtab:cindent:formatoptions+=cro 

@include "lib"

BEGIN { 
  data(d) 
  Csv(d,"data/weather" The.dot "csv")
  _ISORTER=3
  asort(d.rows,_,"isort_cmp")
  o(d.rows)
}

