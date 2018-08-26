#!/usr/bin/env lua
-- vim: ts=2 sw=2 sts=2 expandtab:cindent:formatoptions+=cro 
--------- --------- --------- --------- --------- ---------~

require "lib"

function numScore(t,c,y,lo,hi,   n) 
  n = num()
  for i=lo,hi do numInc(n,t[i][y]) end
  return {score=n.mu,c=c,lo=lo,hi=hi}
end


function bestSplit(t,s)
  all = {}
  y   = #t.name
  for c,name in pairs(t.name) do
    if indep(t,c) then
      if t.nums[c]  then
        rows = ksort(c,t.rows) 
        mid = #rows/2
        all[ #all+1 ] = numScore(rows,c,y,    1, mid)
        all[ #all+1 ] = numScore(rows,c,y,mid+1, #rows)
      else
        tmp={}
        for r,row in pairs(t.rows) do
          x = row[c]
          tmp[x] = tmp[x] or num()
          numInc( tmp[x], row[y] )
        end
        for v,n in pairs(tmp) do
          all[ #all+1 ] = {score=n.mu,c=c,lo=v,hi=v} end end end end
  return ksort("mu",all)[#all] 
end

function mainFft() o(bestSplit(rows())) end

return {main=mainFft}
