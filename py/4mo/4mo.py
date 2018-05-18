from lib import *

ABOUT = dict( 
  why  = "4mo: for making multi-objective rules",
  who  = "Tim Menzies, MIT license (2 clause)",
  when = 2018,
  how  = "pypy3 smore.py",
  what = dict(
    cohen=    dict(why  = "define small changes",
                what = [0.2,0.3,0.5],
                want = float),
    DATA=     dict(why  = "input data csv file",
                what = 'auto.csv',
                make = str,
                want = lambda x:os.path.isfile(x)),
    decimals= dict(why= "decimals to display for floats",
                what = 3,
                want = int),
    few=      dict(why  = "min bin size = max(few, N ^ power)", 
                what = 4,
                want = int),
    MAIN=     dict(why  = "start up action",
                what = "FORMO",
                want = same),
    power=    dict(why  = "min bin size = max(few, N ^ power)", 
                what = 0.5,
                want = float),
    undoubt=  dict(why = "doubt reductions must be larger than x*undoubt",
                what = 1.05,
                want = float)))

@demo
def FORMO(): print(ABOUT["why"])

#-------------
def csv(file, doomed=r'([\n\r\t]|#.*)', sep=",", skip="?"):
  "World's smallest csv reader?"
  use,rows,ako,hdr = [],[],[],None
  with open(file) as fs:
    for n,lst in enumerate(fs):
      lst = re.sub(doomed, "", lst)
      row = [z.strip() for z in lst.split(sep)]
      if len(row) > 0:
        use = use or [n for n,x in enumerate(row) if x[0] != skip]
        row = [row[n] for n in use]
        if n==0:
          hdr     = row
          objs    = [n for n,x in enumerate(hdr) if x[0] in '<>']
          decs    = [n for n,x in enumerate(hdr) if not n in objs]
          weights = [-1 if hdr[n][0]=="<" else 1 for n in objs]
          ako     = [float if row[n][0] in "$<>" else lambda z:z for n in use]
          lo      = [ 10**32 for _ in objs]
          hi      = [-10**32 for _ in objs]
        if n > 0:
          row     = [x if x[0]==skip else p(x) for x,p in zip(row,ako)]
          lo      = [min(row[n], b4) for n,b4 in zip(objs,lo)]
          hi      = [max(row[n], b4) for n,b4 in zip(objs,hi)]
          rows   += [row]
    return o(file=file, ako=ako, head=hdr, 
             objs=objs, y=o(lo=lo, hi=hi),
             decs=decs, weights=weights, rows=rows)

@demo
def CSV(): 
  t=csv("auto.csv")
  print(t.y.lo,t.y.hi)

class Row(o):
  def __init__(i,x,y,w): 
    i.w,i.x,i.y,i.dom = w,x,y,0
  def __lt__(i,j):
    return i.dom < j.dom
  def dominates(i,j,lows,highs):
    s1,s2,n,e,z = 0,0,len(i.y),10,10**-32
    for a,b,w,lo,hi in zip(i.y, j.y,
                           i.w, lows, highs):
      a   = (a - lo) / (hi - lo + z)
      b   = (b - lo) / (hi - lo + z)
      s1 -= e**( w * (a-b)/n )
      s2 -= e**( w * (b-a)/n )
    return s1/n < s2/n
  
class Table:
  def __init__(i,head,rows):
    objs,decs,weights = i.meta(head)
    rows = [ Row([ row[n] for n in decs ], 
                 [ row[n] for n in objs ], 
                 weights) for row in rows ]
    lows, highs = i.ranges(rows)
    i.doms(rows, lows, highs)
    i.report(sorted(rows))
  def meta(i, head):
    objs = [n for n,x in enumerate(head) if x[0] in '<>']
    decs = [n for n,x in enumerate(head) if not n in objs]
    weights =  [-1 if head[n][0]=="<" else 1 for n in objs]
    return objs,decs,weights
  def doms(i,lst, lows, highs):
    for row1 in lst:
      for row2 in lst:
        if row1.dominates(row2,lows,highs): 
          row1.dom += 1
  def ranges(i,lst):
    lo = [ 10**32 for _ in lst[0].y]
    hi = [-10**32 for _ in lst[0].y]
    for r1 in lst:
      for n,x in enumerate(r1.y):
        lo[n] = min(x, lo[n])
        hi[n] = max(x, hi[n])
    return lo,hi  
  def report(i, rows):
    for x in rows[:10]: print("<",x.y, x.dom)
    for x in rows[-10:]: print(">",x.y, x.dom)

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
  def simpler(i):
    return i.doubt > THE.undoubted * (
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

def tree(t):
  if t:
    yield t
    if t.left:
      for t1 in tree(t.left): yield t1
    if t.right:
      for t2 in tree(t.right): yield t2

def supertree(t):
  if t:
    yield t
    if t._up:
      for t1 in supertree(t._up): yield t1

def bottomUp(t):
  return sorted( [t for t in tree(t)], 
                 key= lambda z:z.level, 
                 reverse= True)

@demo
def UP():
  t=_grow()
  seen={}
  for b in bottomUp(t):
    for u in supertree(b):
      if not id(u) in seen:
        seen[id(u)]= True
        print(id(b), u.level)

def grow(lst, epsilon=None, few=None, x=same, y=same):
  "returns nil if nothing"
  def makeNode(lst, lvl=0, up=None):
    return o(x= Num( lst, f=x ), y= Num( lst, f=y ),
             level= lvl,
             _up  = up, 
             simplifies=False, left = None, right= None) 
  def X(j): 
    return x( lst[j] )
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
  def show(z): return [X(z),Y(z)]
  seed(1)
  _show = lambda z:  '%s to %s (%.1f) # %s' %(
                       z.x.lo, z.x.hi, z.x.mu,z.x.n)
  print("\n--------------------------")
  tree = grow( [show(int(100*r())) for _ in range(N)],
               x=first,
               y=last)
  showt( tree, val=_show )
  return tree

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
