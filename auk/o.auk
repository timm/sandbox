# vim: ft=awk:ts=2 sw=2 sts=2 expandtab:cindent:formatoptions+=cro 

function nump(x) {
  return x=="" ? 0 : x == (0+strtonum(x))
}
function o(l,prefix,order,   indent,   old,i) {
  if(!order)
    for(i in l) {
      if (nump(i))
        order = "@ind_num_asc"
      else
        order = "@ind_str_asc"
      break
    }
   old = PROCINFO["sorted_in"]
   PROCINFO["sorted_in"]= order
   for(i in l)
     if (isarray(l[i])) {
       print indent prefix "[" i "]"
       o(l[i],"",order, indent "|   ")
     } else
       print indent prefix "["i"] = (" l[i] ")"
   PROCINFO["sorted_in"]  = old
}


