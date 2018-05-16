import math,time
from random import random as r, choice as any, seed as seed
import auto 

class o(object):
  "Javascript envy. Now 'o' is like a JS object."
  def __init__(i, **kv):    i.__dict__.update(kv)
  def __getitem__(i, k):    return i.__dict__[k]
  def __setitem__(i, k, v): i.__dict__[k] = v
  def __repr__(i): return i.__class__.__name__ + kv(i.__dict__, i._has())
  def _has(i):     return [k for k in sorted(i.__dict__.keys()) if k[0] != "_"]

#-------------------------------------
THE = o(decimals   = 3,
        undoutable = 1.05,
        cohen      = 0.2,
        power      = 0.5,
        few        = 4
       )

#-------------------------------------
def same(x): return x
def first(l): return l[0]
def second(l): return l[1]
def last(l): return l[-1]

def kv(d,keys=None, decimals=None):
   "print dictionary, in key sort order"
   decimals = decimals or THE.decimals
   keys = keys or sorted(list(d.keys()))
   pretty = lambda x: round(x,decimals) if isinstance(x,float) else x
   return '{'+', '.join(['%s: %s' % (k, pretty(d[k]))for k in keys])+'}'

def timeit(f):
  t1=time.perf_counter()
  f()
  return time.perf_counter() - t1

#-------------
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

def nodes(t):
  if t:
    if t.left:
      for t1 in nodes(t.left):
        yield t1
    if t.right:
      for t2 in nodes(t.right):
        yield t2
    yield t

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
    return i.doubt > THE.undoubtable * (
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

def splits(lst, epsilon=None, few=None, x=same, y=same):
  "returns nil if nothing"
  def makeNode(lst, lvl=0, up=None):
    return o(x= Num( lst, f=x ),
             y= Num( lst, f=y ),
             level= lvl,
             _up  = up, 
             simplifies=False,
             left = None, 
             right= None) 
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
    #if lo < m < hi-1:
    if hi - m > few:
        if m - lo > few:
          if X(m) - X(lo) > epsilon:
            if X(hi-1) - X(m) > epsilon:
                node.left=recurse(lo=lo,  hi=m,  up=node,  lvl=lvl+1)
                node.right=recurse(lo=m,   hi=hi, up=node, lvl=lvl+1)
    return node
  # main ------------------
  lst     = sorted(lst, key=x)
  root    = makeNode(lst)
  epsilon = epsilon or root.x.sd()*THE.cohen
  few     = max(few or len(lst)**THE.power, THE.few)
  print(dict(e=epsilon, few=few,bins=int(len(lst)/few)))
  return recurse(up=root)
  #return root

def showt(t, tab="|.. ", pre="",lvl=0,val=lambda z: ""):
  if t:
    if lvl==0: print("")
    print(tab*lvl + pre + str( val(t) ))
    if t.left:
      showt(t.left,  tab, "< ", lvl+1, val)
    if t.right:
      showt(t.right, tab, "> ", lvl+1, val)

def _split1(z,X,Y): return [X(z),Y(z)]

def _split(X=same,Y=same,N=1000):
    seed(1)
    _show = lambda z:  '%s to %s (%.1f) # %s' %(
                       z.x.lo, z.x.hi, z.x.mu,z.x.n)
    print("\n--------------------------")
    tree  = splits( [_split1(int(100*r()),X,Y) for _ in range(N)],
                     x=first,
                     y=last)
    showt( tree, val=_show )

def xx(x):
    if x < 10: return x
    if x < 40: return 40
    if x < 70: return x
    return 70

_split()
_split(X=lambda x : 0 if x <40 else x,N=256)
_split(X=xx,N=256)

#Table(auto.data[0], auto.data[1:])

# #rows have id and objs and __lt__
# def chunkify(lst):
#   a,b,c = 0, len(lst), int(len(lst))/chunks
#   while a < b:
#     yield lst[a:a+c]
#     a += c
# 
## def best(d, nth): 
#   some = int( len(d.keys()) * nth )
#   return sorted(list(d.values))[-some:]
# 
# # use Dom(lst);sorted(lst) and you'll e god
# # level defaults to zerp
# def dombig(lst, ws, nth=3, p=0.5, small=100)
#   def chunkify(lst):
#     a,b,c = 0, len(lst), int(len(lst))/chunks
#     while a < b:
#       yield lst[a:a+c]
#       a += c
# 
#     return sorted(list(d.values))[-some:]
# 
#   def dom(x,y):
#     s1, s2, n, z = 0, 0, len(x.objs), 10**-32
#     for a,b,w,lo,hi in zip(x.objs,y.objs,ws,lows,highs):
#         a   = (a - lo) / (hi - lo + z)
#         b   = (b - lo) / (hi - lo + z)
#         s1 -= e**( w * (a-b)/n )
#         s2 -= e**( w * (b-a)/n )
#     return s1/n < s2/n
# 
#   def doms(lst, doms):
#     for x in lst:
#       for y in lst:
#         if dom(x, y):
#           doms[x.id] = doms[x.id] if x.id in doms else x
#           one.dom += 1
#     return doms
# 
#   def step(pop, level):
#     for chunk in chunkify( pop ) :
#       for one in bore( doms(chunk,{}), 0.5)
#         one.level = level
#         yield one
# 
#   lows,highs = ranges(lst, {}, {})
#   if len(lst) < small:
#     doms( lst,{} )
#     for one in lst:
#       one.level = one.dom
#   else:
#     chunks = len(lst)**0.5
#     level = 0
#     pop   = random.shuffle(lst)
#     while len(pop) > chunks:
#       level += 1
#       pop = [ one for one in step(pop,level) ]
#   return sorted(lst, key=lambda z: z.level)
