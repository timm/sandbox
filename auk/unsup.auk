# vim: ft=awk:tabstop=2:softtabstop=2:shiftwidth=2:expandtab

@include "lib"
 NR==1{ print $0 }
END { 
  for(C in Hi) {ranges(C)}
  dump(Data) 
}

function ranges(c,     d,hi,swaps) {
  colget(c,d)
  hi = asort(d)
  cuts(c,d,1,hi,swaps,hi^Enough)
  colput(c,swaps) 
}
function colget(c,d,   r,x) {
  fyi("\ncol " c)
  array(d)
  for(r in Data) {  
    x = Data[r][c]
    if (x != "?")
      d[ length(d) + 1 ] = x }
}
function colput(c,swaps,   r,x) {
  for(r in Data) {
    x = Data[r][c]
    if (x != "?") 
      Data[r][c] = swaps[x] }
}
function cuts(c,d,lo,hi,swaps,enough,     pre,r,cut,txt) {
  txt = pre d[lo] " " d[hi]
  cut = argmin(d,lo,hi,enough)
  if(cut) {
    fyi(txt)
    cuts(c, d, lo,   cut, swaps,enough,pre "|__ ")
    cuts(c, d, cut+1, hi, swaps,enough,pre "|__ ") 
  } else  {
    fyi(txt  " ("hi-lo")")
    for(r=lo; r<=hi; r++) swaps[d[r]] = d[lo] }
}
function argmin(d,lo,hi,enough,
                l,r,i,cut,best,tmp) {
  if (hi - lo > 2* enough) {
    num(l)
    num(r)
    for(i=lo; i<=hi; i++) ninc(r, d[i])
    best = r.sd
    for(i=lo; i<=hi; i++) {
      ninc(l, d[i])
      ndec(r, d[i])
      if (l.n >= enough)
	     if (r.n >= enough)  {
         tmp = nxpect(l,r) *  Margin
	       if (tmp < best) {
	         cut  = i
	         best = tmp   }}}}
  return cut 
}
