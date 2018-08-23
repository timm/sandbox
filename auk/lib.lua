-- vim: ts=2 sw=2 sts=2 expandtab:cindent:formatoptions+=cro 

require "config"

do
  local seed0     = 10013
  local seed      = seed0
  local modulus   = 2147483647
  local multipler = 16807
  function rseed(n) seed = n or seed0 end 
  function rand() -- park miller
    seed = (multipler * seed) % modulus
    return seed / modulus end
end

find = string.find
match = function(s,p)  return string.match(s,p) ~= nil end

function ordered(t,  i,keys)
  i,keys = 0,{}
  for key,_ in pairs(t) do keys[#keys+1] = key end
  table.sort(keys)
  return function ()
    if i < #tmp then
      i=i+1; return keys[i], t[keys[i]] end end end

function split(s, sep,    t,notsep)
  t, sep = {}, sep or ","
  notsep = "([^" ..sep.. "]+)"
  for y in string.gmatch(s, notsep) do t[#t+1] = y end
  return t
end

function o(t,     go)
  go = function (x,       str,sep)
    if type(x) ~= "table" then return tostring(x) end
    for k,v in ordered(x) do
      str = str .. sep .. k .. ": " .. go(v, "{","")
      sep = ", " end
    return str .. '}'
  end
  return go(t,"{","") end

function data()
  return {w={}, lo={}, hi={}, rows={}, name={}, _use={}} end

function row(t, r, cells)
  if r==0 then
    for c0,x in pairs(cells) do
      if  not match(/%?/,x) then
        c= #t._use+1
        t._use[ c ] =  c0
        t.name[c] = x
        if  match(/<>%$/,x) then
          t.lo[c] = 10^32
          t.hi[c] = -10^32
          if match(/</, x) then t.w[c] =  1 end
          if match(/>/, x) then t.w[c] = -1 end  end end end
  else
    t.rows[ r ] = {}
    for c,c0 in pairs(t._use) do
       x = cells[c0]
       if x != "?" and t.hi[c] then 
          x = tonumber(x)
          if x > t.hi[c] then t.hi[c] = x end
          if x < t.lo[c] then t.lo[c] = x end end  
      t.rows[r][c] = x end end  end 

function csv(t, file, fun,      stream,txt,cells,r)
  fun    = fun or row
  stream = file and io.input(file) or io.input()
  r,line = -1,io.read()
  while line do
    line = line:gsub("[\t\r ]*","") -- no spaces
                :gsub("#.*","") -- no comments
    if #line > 0 then
      r = r + 1
      fun(line,r, split(line)) end 
    line = io.read() end end


function rogues(    ignore,match)
  ignore = {
           jit=true, math=true, package=true, table=true, coroutine=true,
           bit=true, os=true, io=true, bit32=true, string=true,
           arg=true, debug=true, _VERSION=true, _G=true }
  for k,v in pairs( _G ) do
    if type(v) ~= "function" and not ignore[k] then
       assert(match(k,"^[A-Z]"),"rogue local ["..k.."]") end end
end

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
