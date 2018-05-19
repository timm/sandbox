from lib import *

def filep(x): return os.path.isfile(x)

ABOUT = dict( 
  why  = "4mo: for making multi-objective rules",
  who  = "Tim Menzies, MIT license (2 clause)",
  when = 2018,
  how  = "pypy3 smore.py",
  what = dict(
    cohen=    dict(why  = "define small changes",
                what = [0.2,0.3,0.5],
                want = float)
    ,DATA=     dict(why  = "input data csv file",
                what = 'auto.csv',
                make = str,
                want = filep)
    ,decimals= dict(why= "decimals to display for floats",
                what = 3,
                want = int)
    ,few=      dict(why  = "min bin size = max(few, N ^ power)", 
                what = 4,
                want = int)
    ,MAIN=     dict(why  = "start up action",
                what = "FORMO",
                want = same)
    ,power=    dict(why  = "min bin size = max(few, N ^ power)", 
                what = 0.5,
                want = float)
    ,undoubt=  dict(why = "doubt reductions must be larger than x*undoubt",
                what = 1.01,
                want = float)
    ,verbose=  dict(why = "trace all calls",
                what = False,
                want = bool)
))

@demo
def FORMO(): print(ABOUT["why"])

#-------------
   
@demo
def CSV(): 
  for r in data(rows("auto.csv")): print(r)

class Row(o):
  def __init__(i,x,y): 
    i.x,i.y,i.dom = x,y,0
  def __lt__(i,j):
    return i.dom < j.dom
  def dominates(i,j,weights,lows,highs):
    s1,s2,n,e,z = 0,0,len(i.y),10,10**-32
    for a,b,w,lo,hi in zip(i.y, j.y,
                           weights, lows, highs):
      a   = (a - lo) / (hi - lo + z)
      b   = (b - lo) / (hi - lo + z)
      s1 -= e**( w * (a-b)/n )
      s2 -= e**( w * (b-a)/n )
    return s1/n < s2/n
 
@demo
def CSV(): 
  for r in data(rows("auto.csv")): print(r)

class Table:
  def __init__(i,row):
    i.hdr  = row
    i.rows = []
    objs   = [n for n,x in enumerate(i.hdr) if x[0] in '<>']
    decs   = [n for n,x in enumerate(i.hdr) if not n in objs]
    i.x    = o(n=decs)
    i.y    = o(n=objs, 
               weights = [1 if i.hdr[n][0]==">" else -1 for n in objs],
               lo      = [ 10**32 for _ in objs],
               hi      = [-10**32 for _ in objs])
  def __add__(i,row):
    def update(now,b4,f): 
      return b4 if now=="?" else f(now,b4)
    decs    = [ row[n] for n in i.x.n ]
    objs    = [ row[n] for n in i.y.n ]
    i.rows += [ Row(decs,objs) ]
    i.y.lo  = [ update(now, b4, min) for now,b4 in zip(objs, i.y.lo) ]
    i.y.hi  = [ update(now, b4, max) for now,b4 in zip(objs, i.y.hi) ]
  def doms(i):
    for row1 in i.rows:
      for row2 in i.rows:
        if row1.dominates(row2, i.y.weights, i.y.lo, i.y.hi):
          row1.dom += 1

def tree(t):
  if t:
    yield t
    for u in tree(t.left): yield u
    for v in tree(t.right): yield v

def supertree(t):
  if t:
    yield t
    if t._up:
      for u in supertree(t._up): yield u

def subtree(t):
  if t:
    for u in subtree(t.left): yield u
    for v in subtree(t.right): yield v
    yield t

def leaves(t):
  for u in subtree(t):
    if not u.left and not u.right: yield u

def table(file):
  t=None
  for row in data(rows(file)):
    if t: t + row
    else: t = Table(row)
  t.doms()
  return t

@demo
def TABLE():
  t=table("auto.csv")
  t.rows = sorted(t.rows)
  for row in t.rows[:10]: print("<", row.y,row.dom)
  for row in t.rows[-10:]: print(">",row.y,row.dom)

class Thing(o):
  def __init__(i, inits=[],f=lambda z:z):
    i.locals()
    i.n, i._f = 0, f
    #[i + x for x in inits]
    [i+x for x in inits]
  def __add__(i,x):
    if x != None:
      i.n += 1
      i._add( i._f(x) )
  def simpler(i,j,k):
    return i.doubt() > THE.undoubt * (
                           j.doubt() * j.n/i.n + 
                           k.doubt() * k.n/i.n ) 

class Num(Thing):
  def locals(i): 
    i.mu = i.m2 =  0
    i.hi = -10**32
    i.lo =  10**32
  def doubt(i): return i.sd()
  def _add(i,x):
    i.hi = max(i.hi,x)
    i.lo = min(i.lo,x)
    delta  = x - i.mu
    i.mu  += delta/i.n
    i.m2  += delta*(x - i.mu)
  def sd(i): return (i.m2/(i.n - 1))**0.5
  def __repr__(i):
    return 'Num'+kv(dict(lo=i.lo,hi=i.hi,mu=i.mu, sd=i.sd(), n=i.n))

class Sym(Thing):
  def locals(i): i.seen, i._ent = {}, None
  def doubt(i): return i.ent()
  def _add(i,x):
    i.seen[x] = i.seen.get(x,0) + 1
    i._ent = None
  def ent(i):
    if i._ent == None:
      i._ent = 0
      for _,v in i.seen.items():    
        p= v/i.n
        i._ent -= p*math.log(p,2)
    return i._ent
  def __repr__(i):
    return 'Sym'+kv(dict(seen=i.seen, ent=i.ent(), n=i.n))
@demo
def SUBTREE():
  t=_grow()
  for b in subtree(t):
    print(b.level, b.x.n, id(b))

def grow(lst, epsilon=None, few=None, x=same, y=same):
  "returns nil if nothing"
  def makeNode(lst, lvl=0, up=None):
    return o(x= Num( lst, f=x ), y= Num( lst, f=y ),
             level= lvl,
             _up  = up, 
             simpler=False, left = None, right= None) 
  X = lambda j:  x( lst[j] )
  def mid(lo,hi):
    m = m1 = m2 = int(lo +(hi-lo)/2)
    while m1 < hi-1 and X(m1-1) == X(m1)  : m1 += 1
    while m2 > 0   and X(m2)   == X(m2-1): m2 -= 1
    m = m2 if (m-m2) < (m1-m) else m
    return m
  def recurse(lo=0, hi=len(lst), up=None, lvl=0):
    node = makeNode(lst[lo:hi], lvl=lvl, up=up) if lvl else up
    m = mid(lo,hi)
    if hi - m > few:
      if m - lo > few:
        if X(m) - X(lo) > epsilon:
          if X(hi-1) - X(m) > epsilon:
             node.left = recurse(lo=lo,  hi=m,  up=node,  lvl=lvl+1)
             node.right= recurse(lo=m,   hi=hi, up=node, lvl=lvl+1)
    return node
  lst     = sorted(lst, key=x)
  root    = makeNode(lst)
  epsilon = epsilon or root.x.sd()*THE.cohen
  few     = max(few or len(lst)**THE.power, THE.few)
  return recurse(up=root)

def showt(t, tab="|.. ", pre="",lvl=0,val=lambda z: ""):
  if t:
    if lvl==0: print("")
    print(tab*lvl + pre + str( val(t) ))
    if t.left:
      showt(t.left,  tab, "< ", lvl+1, val)
    if t.right:
      showt(t.right, tab, "> ", lvl+1, val)

def _grow(X=same,Y=same,N=1000):
  def show(z): return [X(z), X(0 if z<27 else z)]
  #(z)]
  seed(1)
  _show = lambda z:  '%s to %s (%.1f) # %s : %s' %(
                       z.x.lo, z.x.hi, z.x.mu,z.x.n,z.simpler)
  print("\n--------------------------")
  tree = grow( [show(int(100*r())) for _ in range(N)],
               x=first,
               y=last)
  showt( tree, val=_show )
  prune( tree )
  showt( tree, val=_show )
  return tree

def prune(t):
  for u in subtree(t):
    #if not u.simpler:
      if u.left and u.right:
        if u.y.simpler(u.left.y, u.right.y):
          for v in supertree(u.left) : v.simpler = True
          for w in supertree(u.right): w.simpler = True

@demo
def GROW0(): 
  _grow()

@demo
def GROW1(): 
  _grow(X=lambda x : 0 if x <40 else x,N=256)

@demo
def GROW2():
  def xx(x):
    if x < 10: return x
    if x < 40: return 40
    if x < 70: return x
    return 70
  _grow(X=xx,N=256)

if __name__ == "__main__":
   THE = main(ABOUT)
   DECIMALS=THE.decimals
   demo(act=THE.MAIN)
