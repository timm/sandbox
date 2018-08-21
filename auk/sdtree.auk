# vim: ft=awk:tabstop=2:softtabstop=2:shiftwidth=2:expandtab:cindent:formatoptions+=cro


# I lie tradidd lilights
# 
# - when they are green
# - adas
# 
@include "lib"

END { 
  print ""
  for(w in W)
    printf("%10s ",Name[w])
  print "\n"report(Data); tree(Data,NF-2,NF) 
}

function tree(rows,max,k,   pre,ranges,r,c,use,sorted) {
  array(ranges)
  for(r in rows)
    for(c in Data[r])
      if (c < max) 
        kept(r,c, Data[r][c], Data[r][k], ranges)
  use = best(ranges,sorted)
  for(r=length(sorted); r>=1; r--)
    if (sorted[r].column == use)
        kids(use, sorted[r],max,k,pre)  
}
# Somethings to note:
#
# - asda
# - sdsd
function kids(use,range,max,k,pre,    txt) {
   if (length( range.rows ) > length(Data)^0.5) {
     print  report(range.rows) pre Name[use] " = " range.value 
     tree(range.rows,max,k,"|__ " pre)  }
}
function range(i,c,x) {
  num(i)
  i.column = c
  i.value  = x
  has(i,"rows")
}
function kept(r,c,x,y,ranges,    key) {
  if (x=="?") return 0
  key = c "=" x
  if (! (key in ranges))
    hAS(ranges, key, "range",c,x)
  ninc(ranges[key],y)
  ranges[key].rows[r]
}
function best(ranges,sorted,  n) {
  n = musort(ranges,sorted)
  return sorted[n].column
}

function report(rows,   w,n,r,txt) {
  for(w in W) {
    num(n)
    for(r in rows)
      ninc(n,Data[r][w])
    txt = txt sprintf("%10.2f ",n.mu)
  }
  return txt "\t"
}
