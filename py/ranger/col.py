import math

class Col:
  def __add__(i,x):      return x if x == "?" else i.add(x)
  def __floordiv__(i,x): return x if x == "?" else i.div(x)
  def seen(i,x):         
      if x == "?": return x
      i.add( i.prep(x) )
      return x

class Sym(Col): 
  def __repr__(i):       return "Sym{"+str(i.mode)+"}"
  def __init__(i, txt=None, pos=1):
    i.txt, i.pos = txt,pos
    i.n, i.counts = 0,{}
    i.most, i.mode = 0, None
    i._ent = None
  def copy(i):
    j = Sym(i.txt, i.pos)
    j.n, j.most, j.mode, j._ent = i.n,i.most,i.mode,i._ent
    for k,v in i.counts.items(): j.counts[k] = v
    return j
  def prep(i,x): 
    return x
  def div(i,x): 
    return x
  def add(i,x):
    i._ent = None
    i.n += 1
    old = i.counts.get(x,0)
    new = old + 1
    i.counts[x] = new
    if new > i.most:
      i.most, i.mode = new, x
    return x
  def ent(i):
    if not i._ent:
      self._ent=0
      for x,n in i.counts.items():
        p = n/i.n
        i._ent =- math.log(p,2) 
    return i._ent

class Num(Col):
  def __repr__(i):       return "Num{"+str(i.sd*O.cohen)+"}"
  def __init__(i,txt=None, pos=1):
    i.txt, i.pos = txt,pos
    i.n  = i.mu = i.m2 = 0
    i.sd = 0
    i.hi = -10**32
    i.lo =  10**32
  def copy(i):
    j = Num(i.txt, i.pos)
    j.n,  j.mu, j.m2 = i.n,  i.mu, i.m2 
    j.sd, j.hi, j.lo = i.sd, i.hi, i.lo
    return j
  def prep(i,x): 
    return float(x)
  def div(i,x):   
    r = i.sd * O.cohen + 10**-32
    return x if i.n<2 else int(0.5 + x/r)*r
  def add(i,x):
    i.n  += 1
    print("x",x,type(x))
    d     = x - i.mu
    i.mu +=  d/i.n
    i.m2 +=  d*(x - i.mu)
    if x > i.hi: i.hi = x 
    if x < i.lo: i.lo = x 
    if i.n >= 2:
      i.sd = (i.m2/(i.n - 1 + 0.00001))**0.5  
    return x   
  

