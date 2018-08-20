# vim: ft=awk:tabstop=2:softtabstop=2:shiftwidth=2:expandtab

@include "lib"

END { tree(NF-2,NF) }

function tree(max,k,   ranges,r,c,n,sorted,i) {
  print("adads")
  array(ranges)
  for(r in Data)
    for(c in Data[r])
      if (c < max)
        keep(c,Data[r][c], Data[r][k],ranges)
  n=musort(ranges,sorted)
  for(i=n;i>=1;i--) {
    print("\n" i)
    o(sorted[i]) }
}

function range(i,c,v) {
  num(i)
  i.c=c
  i.v=v
}
function keep(c,v,k,ranges,   key) {
  key = c "=" v
  if (! (key in ranges))
    hAS(ranges, key, "range",c,v)
  ninc(ranges[key], k)
}
