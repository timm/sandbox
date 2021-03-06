# vim: ft=awk:ts=2 sw=2 sts=2 expandtab:cindent:formatoptions+=cro 

@include "config"
@include "o"

BEGIN { srand(Seed ? Seed : 1)  }

######### ######### ######### ######### ######### ######### 
function data(i) {
  array(i)
  has(i, "w" )
  has(i, "lo" )
  has(i, "hi" )
  has(i, "rows" )
  has(i, "name" )
}
function Csv(i,file,fun,          txt,txts,cells,c,r,x) {
  fun  = fun  ? fun  : "dataInc"
  file = file ? file :  "/dev/stdin"
  print(file)
  while((getline txt < file) > 0)  {
    gsub(/([ \t\r\n]|#.*)/, "", txt) # no comments,whitespace
    if ( split(txt, cells, FS) )
      @fun(i,r++,cells) }
  close(file)
}
function dataInc(i,r,cells) {
  for(c in cells) { 
    x = cells[c]
    if ( r==0 ) {
      i.name[c] = x
      if ( x ~ /[><\$]/) {
        i.lo[c] =  10^32 
        i.hi[c] = -10^32
        if ( x ~ /</ ) i.w[c] =  1
        if ( x ~ />/ ) i.w[c] = -1  }}
    else {
      i.rows[ r ][c] = x
      if (x != "?") 
        if (c in i.hi) { 
          if(x > i.hi[c]) i.hi[c] = x
          if(x < i.lo[c]) i.lo[c] = x }}}
}
######### ######### ######### ######### ######### ######### 
# Num stuff

function nxpect(i,j,   n) { 
  n = i.n + j.n +0.0001
  return i.n/n * i.sd+ j.n/n * j.sd
}
function num(i) { 
  array(i) 
  i.n = i.mu = i.m2 = i.sd = 0
}
function ninc(i,x,    d) {
  if (x == "?") return x
  i.n++
  d = x - i.mu
  i.mu += d/i.n
  i.m2 += d*(x- i.mu)
  if (i.n>=2)
    i.sd = (i.m2/(i.n - 1 + 10^-32))^0.5
  return x
}
function ndec(i,x,    d) {
  if (x == "?") return x
  i.n--
  if (i.n <  1 ) return x
  d = x - i.mu
  i.mu -= d/i.n
  i.m2 -= d*(x- i.mu)
  if (i.n>=2)
    i.sd = (i.m2/(i.n - 1 + 10^-32))^0.5
  return 

}
######### ######### ######### ######### ######### ######### 
# List stuff

function push(a,x) {
  a[ length(a) + 1 ] = x
  return x
}
function anyOther(x,l,     y)  { 
  y = int(rand() * length(l)) + 1 
  return x==y ? anyOther(x,l) : y
}
function dump(a,sep,    i) {
  for(i=1; i<=length(a); i++) print contact(a[i])
}
function concat(a,sep,  s,i) {
  s=a[1]
  for(i=2; i<=length(a); i++)  s = s sep a[i]
  return s
}
function cmp(x,y) {
  if (x <  y) return -1
  if (x == y) return  0
  return  1
}
function ksort_cmp(k1,v1,k2,v2) { 
  return cmp( v1[The.?], v2[The.?] ) 
}
function ksort(k,a,b) { 
  The.?=k
  return asort(a,b,"ksort_cmp") 
}
######## ######### ######### ######### ######### ######### 
# numeric stuff

function rogues(    s) {
  for(s in SYMTAB) 
    if (s ~ /^[A-Z][a-z]/) print "Global " s
  for(s in SYMTAB) 
    if (s ~ /^[_a-z]/) print "Rogue: " s
}
function fyi(x) { print x >> "/dev/stderr" }
