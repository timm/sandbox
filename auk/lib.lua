-- vim: ts=2 sw=2 sts=2 expandtab:cindent:formatoptions+=cro 
--------- --------- --------- --------- --------- --------- 

require "config"

do
  local seed0     = the.seed
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
      i=i+1; return keys[i], t[keys[i]] end end 
end

function split(s, sep,    t,notsep)
  t, sep = {}, sep or ","
  notsep = "([^" ..sep.. "]+)"
  for y in string.gmatch(s, notsep) do t[#t+1] = y end
  return t
end

function o(t,     nl,go)
  go = function (x,       str,sep,pre)
    if type(x) ~= "table" then return tostring(x) end
    for k,v in ordered(x) do
      str = str .. pre .. sep .. k .. ": " .. 
            go(v, "{","", pre .. "|.. " )
      sep = ", " .. (nl and "\n" or "") end
    return str .. '}'
  end
  return go(t,"{","","") 
end

oo = function(t) return o(t,true) end

function data()
  return {w={}, lo={}, hi={}, rows={}, name={}, _use={}} 
end

function header(t,cells)
  for c0,x in pairs(cells) do
    if not true then --match(/%?/,x) then
      c = #t._use+1
      t._use[c] = c0
      t.name[c] = x
      if  match("[<>%$]",x) then
        t.lo[c] = 10^32
        t.hi[c] = -10^32
        if match("<", x) then t.w[c] =  1 end
        if match(">", x) then t.w[c] = -1 end  end end end
end

function row(t,r,cells)
  t.rows[ r ] = {}
  for c,c0 in pairs(t._use) do
    x = cells[c0]
    if x ~= "?" and t.hi[c] then 
      x = tonumber(x)
      if x > t.hi[c] then t.hi[c] = x end
      if x < t.lo[c] then t.lo[c] = x end 
    end  
    t.rows[r][c] = x 
  end 
end  

function csv(t, file, f0,f,      stream,txt,cells,r)
  f0 = f0 or header
  f  = f  or row
  stream = file and io.input(file) or io.input()
  r,line = -1,io.read()
  while line do
    line = line:gsub("[\t\r ]*","") -- no spaces
                :gsub("#.*","") -- no comments
    if #line > 0 then
      r = r + 1
      cells = split(line)
      if r==0 then f0(line,r,cells) else f(line,r,cells) end 
    end
    line = io.read() 
  end
end 

function nxpect(i,j,   n)  
  n = i.n + j.n +0.0001
  return i.n/n * i.sd+ j.n/n * j.sd
end

function num()  
  return {n=0, mu=0, m2=0, sd=0} 
end

function ninc(t,x,    d) 
  if x == "?" then return x end
  t.n = n + 1
  d = x - t.mu
  t.mu = t.mu + d/t.n
  t.m2 = t.m2 + d*(x- t.mu)
  if (t.n>=2) then 
    t.sd = (t.m2/(t.n - 1 + 10^-32))^0.5 end
  return x  
end

function ndec(t,x,    d) 
  if (x == "?") then return x end
  if (t.n == 1) then return x end
  t.n = t.n - 1
  d = x - t.mu
  t.mu = t.mu - d/t.n
  t.m2 = t.m2 - d*(x- t.mu)
  if (t.n>=2) then
    t.sd = (t.m2/(t.n - 1 + 10^-32))^0.5 end
  return x
end

function anyOther(x,l,     y)   
  y = int(rand() * #l) + 1 
  return x==y and anyOther(x,l) or y
end

cat = table.concat
function dump(a,sep) 
  for i=1,#a do cat(a[i],sep) end
end

function ksort(k,t) 
  return table.sort(a,function(x,y) return x[k] < y[k] end) 
end  

function fyi(x)  io.stderr:write(x .. "\n") end
