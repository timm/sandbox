--vim: ts=2 sw=2 sts=2 expandtab:cindent:formatoptions+=cro 
--------- --------- --------- --------- --------- --------- 

function num(w)  
  return {n=0, mu=0, m2=0, sd=0, 
          lo=10^32, hi=-10^32, 
          w=(w or 1)}
end

function nxpect(i,j,   n)  
  n = i.n + j.n +0.0001
  return i.n/n * i.sd+ j.n/n * j.sd
end

function ninc(t,x,    d) 
  if x == "?" then return x end
  t.n = t.n + 1
  d = x - t.mu
  t.mu = t.mu + d/t.n
  t.m2 = t.m2 + d*(x- t.mu)
  if x > t.hi then t.hi = x end
  if x < t.lo then t.lo = x end
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


