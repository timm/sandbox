# vim: ft=awk:tabstop=2:softtabstop=2:shiftwidth=2:expandtab

@include "lib"
NR==1 { print $0 }
END { 
  for(C in Hi) 
    if (C != NF)
      ranges(C,NF)
  dump(Data) 
}
function ranges(c,k,     d0,d,hi,swaps,our) {
  colget(c,k,d0)
  hi = xsort(d0,d)
  cuts(c,d,1,hi,swaps,hi^Enough)
  colput(c,swaps) 
}
function colget(c,k,d,   r,x,y) {
  fyi("\ncol " c)
  array(d)
  for(r in Data) {  
    x = Data[r][c]
    y = Data[r][k]
    if (x != "?")
      hAS(d,length(d) + 1,"xy",x, y) }
}
function xy(i,x,y) {
  array(i)
  i.x = x
  i.y = y
}

function colput(c,swaps,   r,x) {
  for(r in Data) {
    x = Data[r][c]
    if (x != "?") 
      Data[r][c] = swaps[x] }
}
function cuts(c,d,lo,hi,swaps,enough,     pre,r,cut,txt) {
  txt = pre d[lo].x " " d[hi].x
  cut = argmin(d,lo,hi,enough)
  if(cut) {
    fyi(txt)
    cuts(c, d, lo,   cut, swaps,enough,pre "|__ ")
    cuts(c, d, cut+1, hi, swaps,enough,pre "|__ ") 
  } else  {
    fyi( txt " ("hi - lo")")
    for(r=lo; r<=hi; r++) swaps[d[r].x] = d[lo].x 
  }
}
function argmin(d,lo,hi,enough,
                i,cut,
                x,xl,xr,xbest,xtmp,
                y,yl,yr,ybest,ytmp) {
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
	       if (xtmp < xbest) {
           ytmp = nxpect(yl,yr) *  Margin
	         if (ytmp < ybest) {
	           cut  = i
	           xbest = xtmp   
	           ybest = ytmp   
           }}}}}
  return cut 
}
