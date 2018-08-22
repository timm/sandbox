# vim: ft=awk:ts=2 sw=2 sts=2 expandtab:cindent:formatoptions+=cro 

@include "lib"

BEGIN {  rogues();  main() }

function main(   k,c,d,hi,rows) {
  data(d)
  csv(d)
  k = length(d.nam)
  print concat(d.name)
  for(c in d.hi) 
    if (c != width) { 
      hi = isort(c,d.rows)
      cuts(d.rows,c,1,hi,k,hi^The.enough) }
  dump(d.rows)
}
######### ######### ######### ######### ######### ######### 
function cuts(rows,c,lo,hi,k,enough,     pre,r,cut,txt) {
  txt = pre rows[lo][c] " " rows[hi][c]
  cut = argmin(rows,c,lo,hi,k,enough)
  if(cut) {
    fyi(txt)
    cuts(rows, c, lo,   cut, k,enough, pre "|__ ")
    cuts(rows, c, cut+1, hi, k,enough, pre "|__ ") 
  } else  {
    fyi(txt " (" hi-lo ")")
    for(r=lo; r<=hi; r++) rows[r][c] = rows[lo][c] }
}
######### ######### ######### ######### ######### ######### 
function argmin(rows,c,lo,hi,k,enough,   
                i,cut,
                x,xl,xr,xbest,xtmp,
                y,yl,yr,ybest,ytmp) {
  if (hi - lo > 2* enough) {
    num(xl); num(xr)
    num(yl); num(yr)
    for(i=lo; i<=hi; i++)  {
      x=d[i][c] ; ninc(xr, x)
      y=d[i][k] ; ninc(yr, y)
    }
    xbest = xr.sd
    ybest = yr.sd
    for(i=lo; i<=hi; i++) {
      x=d[i][c]
      y=d[i][k]
      ninc(xl, x); ndec(xr, x)
      ninc(yl, y); ndec(yr, y)
      if (xl.n >= enough)
	     if (xr.n >= enough)  {
         xtmp = nxpect(xl,xr) * The.margin
	       if (xtmp < xbest) {
           ytmp = nxpect(yl,yr) * The.margin
	         if (ytmp < ybest) {
	           cut  = i
	           xbest = xtmp   
	           ybest = ytmp   
           }}}}}
  return cut 
}
