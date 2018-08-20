# vim: ft=awk:tabstop=2:softtabstop=2:shiftwidth=2:expandtab

@include "lib"
NR==1 { print $0 }
END { 
  for(C in Hi) 
    if (C != NF)
      ranges(C,NF)
  dump(Data) 
}
function ranges(c,k,     d,hi,swaps,our) {
  array(d)
  colget(c,k,d)
  hi = xsort(d)
  cuts(c,d,1,hi,swaps,hi^Enough)
  colput(c,swaps) 
}
function colget(c,k,d,   r,x) {
  for(r in Data) {  
    x = Data[r][c]
    if (x != "?")
      hAS(d,length(d) + 1,"xy",x, Data[r][k]) }
}
function colput(c,swaps,   r,x) {
  for(r in Data) {
    x = Data[r][c]
    if (x != "?") 
      Data[r][c] = swaps[x] }
}
function cuts(c,d,lo,hi,swaps,enough,     pre,r,cut) {
  print pre lo, hi
  cut = argmin(d,lo,hi,enough)
  if(cut) {
    cuts(c, d, lo,   cut, swaps,enough,pre "|__ ")
    cuts(c, d, cut+1, hi, swaps,enough,pre "|__ ") 
  } else 
    for(r=lo; r<=hi; r++) swaps[d[r]] = d[lo] 
}
function argmin(d,lo,hi,enough,
                x,y,xl,xr,yl,lr,i,cut,xbest,ybest,xtmp,ytmp) {
  if (hi - lo > 2* enough) {
    num(xl); num(xr)
    num(yl); num(yr)
    for(i=lo; i<=hi; i++) {
      ninc(xr, d[i].x)
      ninc(yr, d[i].y)
    }
    xbest = xr.sd
    ybest = yr.sd
    for(i=lo; i<=hi; i++) {
      x=d[i].x
      y=d[i].y
      ninc(xl, x); ndec(xr, x)
      ninc(yl, y); ndec(yr, y)
      if (xl.n >= enough)
	     if (xr.n >= enough)  {
         xtmp = nxpect(xl,xr) *  Margin
	       if (rtmp < xbest) {
           xtmp = nxpect(yl,yr) *  Margin
	         if (ytmp < ybest) {
	           cut  = i
	           xbest = xtmp   
	           ybest = ytmp   
           }}}}}
  return cut 
}
