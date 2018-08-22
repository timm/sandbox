# vim: ft=awk:tabstop=2:softtabstop=2:shiftwidth=2:expandtab

@include "lib"
@include "o"

BEGIN { main() }

function main(  d) {
  data(d)
  print concat(d.name) ",>dom"
  doms(d, The.doms)
  dump(d.rows)
}
function doms(d,samples,       i,k,m,r) {
  k = length(d.name)+1
  for(r1 in d.rows) { 
    for(i=1; i<=samples; i++) { 
      r2 = anyOther(r1, d.rows)
      d.rows[r1][k] += dom(d,r1,r2) / samples }}
}
function dom(d,r1,r2,     w,n,c,a,b,s1,s2) {
  n = length(d.w) + 10^-32
  for (c in d.w) {
    w   = d.w[c]
    a   = d.rows[r1][c]
    b   = d.rows[r2][c]
    a   = (a - d.lo[c]) / (d.li[c] - d.lo[c] + 10^-32)
    b   = (b - d.lo[c]) / (d.li[c] - d.lo[c] + 10^-32)
    s1 -= 10^(w * (a - b) / n)
    s2 -= 10^(w * (b - a) / n)  }
  return s1 / n < s2 / n
}
