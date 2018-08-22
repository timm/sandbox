# vim: ft=awk:ts=2 sw=2 sts=2 expandtab:cindent:formatoptions+=cro 

@include "config"

BEGIN { srand(Seed ? Seed : 1)  }

######### ######### ######### ######### ######### ######### 
function data(i,file,          txt,txts,cells,c,r,x) {
  # slots ==  w lo hi rows name
  file = file ? file :  "/dev/stdin"
  has(i, "w" )
  has(i, "lo" )
  has(i, "hi" )
  has(i, "rows" )
  has(i, "name" )
  while((getline txt < file) > 0)  {
    gsub(/([ \t\r\n]|#.*)/, "", txt) # no comments,whitespace
    if (txt) {
      split(txt, cells, FS)
      r++
      for(c in cells) { 
        x = cells[c]
        if ( r==1 ) {
          i.name[c] = x
          if ( x ~ /[><\$]/) {
            i.lo[c] =  10^32 
            i.hi[c] = -10^32
            if ( x ~ /</ ) i.w[c] =  1
            if ( x ~ />/ ) i.w[c] = -1  }}
        else {
          i.rows[ r-1 ][c] = x
          if (x != "?") 
            if (c in i.hi) { 
              if(x > i.hi[c]) i.hi[c] = x
              if(x < i.lo[c]) i.lo[c] = x }}}}}
  close(file)
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
function dump(l,  line,i,j,sep) {
  for(i in l)  {
    line = sep = ""
    for(j in l[i]) { line = line sep l[i][j]; sep  = "," }
    print line }
}
function concat(a,sep,  sep1,i,s) {
  sep = sep ? sep : ","
  for(i=1; i<=length(a); i++) {
    s=s sep1 a[i]
    sep1 = sep }
  return s
}
function cmp(x,y) {
  if (x <  y) return -1
  if (x == y) return  0
  return  1
}
function xsort_cmp( k1,v1,k2,v2) { return cmp(v1.x,  v2.x)  }
function ysort_cmp( k1,v1,k2,v2) { return cmp(v1.y,  v2.y)  }
function musort_cmp(k1,v1,k2,v2) { return cmp(v1.mu, v2.mu) }
function isort_cmp(k1,v1,k2,v2,  i) { 
  i = _ISORTER
  return cmp( v1[i], v2[i] ) }

function xsort(a,b) { return asort(a,b,"xsort_cmp") }
function ysort(a,b) { return asort(a,b,"ysort_cmp") }
function musort(a,b) { return asort(a,b,"musort_cmp") }
function isort(i,a,b) { 
  _ISORTER=i
  return asort(a,b,"isort_cmp") }

######## ######### ######### ######### ######### ######### 
# numeric stuff

function rogues(    s) {
  for(s in SYMTAB) 
    if (s ~ /^[A-Z][a-z]/) print "Global " s
  for(s in SYMTAB) 
    if (s ~ /^[_a-z]/) print "Rogue: " s
}
function fyi(x) { print x >> "/dev/stderr" }
