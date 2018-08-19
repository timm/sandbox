# vim: set filetype=awk et sts=2 sw=2 ts=2  :
 
@include "config.awk"

BEGIN { srand(Seed ? Seed : 1) 
	split("",W,"")
	FS   = "," }
      { update( NR-1 )
        if (NR==1) { print $0 ",dom"; next }  }
END   { finale() }

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
function push(x,a) {
  l[ length(a) + 1 ] = x
  return x
}

function array(a) { split("",a,"") }

function xpect(i,j,   n) {
  n = i["n"] + j ["n"] +0.0001
  return i["n"]/n * i["sd"] + j["n"]/n * j["sd"]
}
function ninc(i,x,    d) {
  if (x == "?") return x
  i["n"]++
  d = x - i["mu"]
  i["mu"] += d/i["n"]
  i["m2"] += d*(x- i["mu"])
  if (i["n"]>=2)
    i["sd"] = (i["m2"]/(i["n"] - 1 + 10^-32))^0.5
  return x
}
function ndec(i,x,    d) {
  if (x == "?") return x
  i["n"]--
  d = x - i["mu"]
  i["mu"] -= d/i["n"]
  i["m2"] -= d*(x- i["mu"])
  if (i["n"]>=2)
    i["sd"] = (i["m2"]/(i["n"] - 1 + 10^-32))^0.5
  return x
}
function anyBut(x,l,     y)  { 
  y = int(rand() * length(l)) + 1 
  return x==y ? anyBut(x,l) : y
}
function dump(l,  line,i,j,sep) {
  for(i in l)  {
    line = sep = ""
    for(j in l[i]) { line = line sep l[i][j]; sep  = "," }
    print line }
}
function rogues(    s) {
  for(s in SYMTAB) 
    if (s ~ /^[A-Z][a-z]/) print "Global " s
  for(s in SYMTAB) 
    if (s ~ /^[_a-z]/) print "Rogue: " s
}
