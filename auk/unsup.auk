# vim: ft=awk:ts=2 sw=2 sts=2 expandtab:cindent:formatoptions+=cro 

@include "lib"

BEGIN {  rogues();  main() }

function main(   c,d,hi,rows) {
  data(d)
  csv(d)
  print concat(d.name)
  for(c in d.hi) { 
    hi = isort(c,d.rows)
    cuts(d.rows,c,1,hi,hi^The.enough) }
  dump(d.rows)
}
######### ######### ######### ######### ######### ######### 
function cuts(rows,c,lo,hi,enough,     pre,r,cut,txt) {
  txt = pre rows[lo][c] " " rows[hi][c]
  cut = argmin(rows,c,lo,hi,enough)
  if(cut) {
    fyi(txt)
    cuts(rows, c, lo,   cut, enough, pre "|__ ")
    cuts(rows, c, cut+1, hi, enough, pre "|__ ") 
  } else  {
    fyi(txt " (" hi-lo ")")
    for(r=lo; r<=hi; r++) rows[r][c] = rows[lo][c] }
}
######### ######### ######### ######### ######### ######### 
function argmin(rows,c,lo,hi,enough,   
                l,r,i,cut,best,tmp,x) {
  if (hi - lo > 2* enough) {
    num(l)
    num(r)
    for(i=lo; i<=hi; i++) 
      ninc(r, rows[i][c])
    best = r.sd
    for(i=lo; i<=hi; i++) {
      x = rows[i][c]
      ninc(l, x)
      ndec(r, x)
      if (l.n >= enough)
	     if (r.n >= enough)  {
         tmp = nxpect(l,r) *  The.margin
	       if (tmp < best) {
	         cut  = i
	         best = tmp   }}}}
  return cut 
}
