# vim: ft=awk:tabstop=2:softtabstop=2:shiftwidth=2:expandtab

@include "lib"
NR==1 { print $0 ",>dom" }
END {
  doms(NF+1, 20/Best) 
  dump(Data)
}
function doms(k,m,      r) {
  for(r in Data)  
    Data[r][k] = dom(r,m)/m
}
function dom(r,m,         i,n) {
  while(m-- > 0)
    n += dom1(r, anyOther(r,Data)) 
  return n   
}
function dom1(r1,r2,   w,n,c,a,b,s1,s2) {
  n = length(W) + 10^-32
  for (c in W) {
    w   = W[c]
    a   = Data[r1][c]
    b   = Data[r2][c]
    a   = (a - Lo[c]) / (Hi[c] - Lo[c] + 10^-32)
    b   = (b - Lo[c]) / (Hi[c] - Lo[c] + 10^-32)
    s1 -= 10^(w * (a - b) / n)
    s2 -= 10^(w * (b - a) / n)  }
  return s1 / n < s2 / n
}
