-- vim: ts=2 sw=2 sts=2 expandtab:cindent:formatoptions+=cro 
--------- --------- --------- --------- --------- ---------~

require "config"
require "rows"
require "num"
require "random"

--------- --------- --------- --------- --------- --------- 
-- ## List Stuff

function ksort(k,t) 
  return table.sort(a,function(x,y) return x[k] < y[k] end) 
end  

function ordered(t,  i,keys)
  i,keys = 0,{}
  for key,_ in pairs(t) do keys[#keys+1] = key end
  table.sort(keys)
  return function ()
    if i < #keys then
      i=i+1; return keys[i], t[keys[i]] end end 
end

function o(t,    indent,   formatting)
  indent = indent or 0
  for k, v in ordered(t) do
    formatting = string.rep("|  ", indent) .. k .. ": "
    if type(v) == "table" then
      print(formatting)
      o(v, indent+1)
    else
      print(formatting .. v) end end 
end

--------- --------- --------- --------- --------- --------- 
-- ## String Stuff

function split(s, sep,    t,notsep)
  t, sep = {}, sep or ","
  notsep = "([^" ..sep.. "]+)"
  for y in string.gmatch(s, notsep) do t[#t+1] = y end
  return t
end

cat = table.concat
function dump(a,sep) 
  for i=1,#a do print(cat(a[i],sep or ",")) end
end

function fyi(x) io.stderr:write(x .. "\n") end


--------- --------- --------- --------- --------- --------- 
-- ## Meta Stuff

function main(t)
  if type(t.main) == 'function' then
    t.main() end end


return {main=function() print("Lib loaded") end}
