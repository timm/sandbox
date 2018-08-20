# vim: ft=awk:tabstop=2:softtabstop=2:shiftwidth=2:expandtab

@include "config"

BEGIN { srand(Seed ? Seed : 1) 
        split("",W,"")
        FS   = "," }
      {  gsub(/[ \t\r]*/, "", $0) # no whitespce:
         gsub(/#["*"]$/,  "", $0) # no comments
         update( NR-1 ) }

######### ######### ######### ######### ######### ######### 
function update(r,   c) { 
  for(c=1; c<=NF; c++) { 
    if (NR==1) 
       header(c,$c) 
    else {
       Data[r][c] = $c 
       if (($c != "?") && (c in Hi)) {
   Hi[c] = $c > Hi[c] ? $c : Hi[c]
   Lo[c] = $c < Lo[c] ? $c : Lo[c] }}}
}
func header(c,s) {
  if ( s ~ /</ ) W[c] = -1
  if ( s ~ />/ ) W[c] =  1
  if ( s ~ /[<>\$]/ ) { Hi[c]= -10^32; Lo[c]=  10^32 }
}

######### ######### ######### ######### ######### ######### 
# Object stuff

function array(i) { split("",i,"") }
function Any(i)   { array(i); i["oid"] = ++OID }

function has0(lst,key) {
  lst[key][SUBSEP]
  split("",lst[key],"")
}
function has(lst,key,fun) { 
  has0(lst, key); if (fun) @fun(lst[key])
}
function haS(lst,key,fun,x) {
  has0(lst,key); if (fun) @fun(lst[key],x)
}
function hAS(lst,key,fun,x,y) {
  has0(lst,key); if (fun) @fun(lst[key],x,y)
}

######### ######### ######### ######### ######### ######### 
# Num stuff

function nxpect(i,j,   n) {
  n = i.n + j.n +0.0001
  return i.n/n * i.sd+ j.n/n * j.sd
}
function num(i) { Any(i) }
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
function xsort_cmp(k1,v1 k2,v2) {
    if   (v1.x    <  v2.x) return -1
    else if (v1.x == v2.x) return 0
    else return 1
}
function ysort_cmp(k1,v1 k2,v2) {
    if   (v1.y    <  v2.y) return -1
    else if (v1.y == v2.y) return 0
    else return 1
}
function xsort(a) { return asort(a,"xsort_cmp") }
function ysort(a) { return asort(a,"ysort_cmp") }

function xy(i,x,y) {
  array(i)
  i.x = x
  i.y = y
}
######### ######### ######### ######### ######### ######### 
# numeric stuff

function nump(x) {
  return x=="" ? 0 : x == (0+strtonum(x))
}
function o(l,prefix,order,   indent,   old,i) {
  if(!order)
    for(i in l) {
      if (nump(i))
        order = "@ind_num_asc"
      else
        order = "@ind_str_asc"
      break
    }
   old = PROCINFO["sorted_in"]
   PROCINFO["sorted_in"]= order
   for(i in l)
     if (isarray(l[i])) {
       print indent prefix "[" i "]"
       o(l[i],"",order, indent "|   ")
     } else
       print indent prefix "["i"] = (" l[i] ")"
   PROCINFO["sorted_in"]  = old
}

function rogues(    s) {
  for(s in SYMTAB) 
    if (s ~ /^[A-Z][a-z]/) print "Global " s
  for(s in SYMTAB) 
    if (s ~ /^[_a-z]/) print "Rogue: " s
}

function fred(i) {
  Any(i)
  has(i,"now","num")
  has(i,"then","num")
}

