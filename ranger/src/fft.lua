#!/usr/bin/env lua
-- vim: ts=2 sw=2 sts=2 expandtab:cindent:formatoptions+=cro 
--------- --------- --------- --------- --------- ---------~

require "lib"

function numScore(t,c,y,lo,hi,   n) 
  n = num()
  for i=lo,hi do numInc(n,t[i][y]) end
  return {mu=n.mu,c=c,lo=t[lo][c],hi=t[hi][c]}
end

function rowMedian(a,c,      mid,i,j)
  mid=#a//2
  i=mid; while i < #a and a[i][c] == a[i+1][c] do i=i+1 end
  j=mid; while j > 1  and a[j][c] == a[j-1][c] do j=j-1 end
  mid=  i - mid < mid - j and i or j
  return mid
end

function bestSplit(t)
  all = {}
  y   = #t.name
  for c,name in pairs(t.name) do
    if indep(t,c) then
      if t.nums[c]  then
        rows = ksort(c,t.rows) 
        mid = rowMedian(rows, c)
        all[ #all+1 ] = numScore(rows,c,y,  1, mid-1)
        all[ #all+1 ] = numScore(rows,c,y,mid, #rows)
      else
        tmp={}
        for r,row in pairs(t.rows) do
          x = row[c]
          tmp[x] = tmp[x] or num()
          numInc( tmp[x], row[y] )
        end
        for v,n in pairs(tmp) do
          all[ #all+1 ] = {mu=n.mu,c=c,lo=v,hi=v} end end end end
  all=ksort("mu", all)
  return all[#all] 
end

function fft(t,d,  pre,d,split,t1,x)
  d     = d or 4
  if d <=0 then return true  end
  pre   = pre or "if  "
  split = bestSplit(t,s)
  print(pre,t.name[split.c],">=",split.lo, t.name[split.c],"<=", split.hi)
  t1    = data()
  header(t1, t.name)
  for _,r in pairs(t.rows) do
    x= r[split.c]
    if x <= split.hi and x >= split.lo then row(t1,r) end end
  return fft(t1,d-1,"else")
end

function mainFft() fft(rows()) end

return {main=mainFft}
