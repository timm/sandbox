#!/usr/local/bin/lua
-- vim: ts=2 sw=2 sts=2 expandtab:cindent:formatoptions+=cro 
--------- --------- --------- --------- --------- ---------~

require "lib"

function dom(d,r1,r2,     n,a,b,s1,s2)
  s1,s2,n = 0,0, #d.w
  for c,w in pairs(d.w) do
    a = norm( t.nums[c], d.rows[r1][c])
    b = norm( t.nums[c], d.rows[r2][c])
    s1 = s1 - 10^(w * (a-b)/n)
    s2 = s2 - 10^(w * (b-a)/n)
  end
  return s1/n < s2/n 
end

function doms(d,  n,c,r2)
  n= The.dom.samples
  c= #d.names + 1
  print(cat(d.name) .. ",>dom")
  for r1=1,#d.rows do
    for s=1,n do
     r2 = another(r1,d.rows) 
     if dom(d,r1,r2) then
       old = d.rows[row1][c] or 0
       d.rows[r1][c]= old + 1/n end end end
  dump(d)
end

doms(data())
