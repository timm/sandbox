#  vim: set filetype=awk ts=2 sw=2 sts=2 expandtab: 

# num : numbers
    
function num(i) {
  i.hi  = -1e32
  i.lo  =  1e32
  i.bins= 5
  i.n   = i.mu = i.m2 = i.sd = 0
}
function numNorm(i,x) {
  return (x - i.lo)/(i.hi - i.lo + 1e-32)
}
function numSmall(i) {
}  
function numAdd(i,x,          delta) {
  x    += 0
  i.n  += 1
  i.lo  = x < i.lo ? x : i.lo
  i.hi  = x > i.hi ? x : i.hi
  delta = x - i.mu
  i.mu += delta/i.n
  i.m2 += delta*(x - i.mu)
  if (i.n > 1) 
    i.sd = (i.m2/(i.n-1))^0.5
  return x
}
function numStretch(i) {
  return i.sd
}
function numNorm(i,x) {
  return (x-i.lo)/(i.hi - i.lo + 1e-32)
}

