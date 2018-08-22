# vim: ft=awk:tabstop=2:softtabstop=2:shiftwidth=2:expandtab

@include "array"

BEGIN { 
  FS  = ","
  array(The)
  The.doms   = 100
  The.enough = 0.5 
  The.margin = 1.05
  The.cohen  = 0.2 
  The.dot    = "\56"
}
