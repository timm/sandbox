banner="""
 ___ _ __ ___   ___  _ __ ___ 
/ __| '_ ` _ \ / _ \| '__/ _ \ 
\__ \ | | | | | (_) | | |  __/
|___/_| |_| |_|\___/|_|  \___|

(simple multi-objective rule engine)
"""
import getopt,sys,re,csv,math,time
from random import random as r, choice as any, seed as seed

class o(object):
  "Javascript envy. Now 'o' is like a JS object."
  def __init__(i, **kv):    i.__dict__.update(kv)
  def __setitem__(i, k, v): i.__dict__[k] = v
  def __getitem__(i, k): return i.__dict__[k]
  def keys(i):           return i.__dict__.keys()
  def __repr__(i):       return i.__class__.__name__ + kv(i.__dict__, i._has())
  def _has(i):           return [k for k in sorted(i.__dict__.keys()) if k[0] != "_"]

THE = o(   
           cohen      = 0.2,
           DATA       = 'auto.csv',
           decimals   = 3,
           few        = 4,
           MAIN       = 'SMORE',
           power      = 0.5,
           undoutable = 1.05
       )

#------------------------------------
def demo(f=None, act=None, all=[]):
  if     f: all += [f]
  elif act:
    for one in all:
      if one.__name__ == act: one()
  else: [f() for f in all]
  return f

@demo
def SMORE(): print(banner)

def same(x): return x
def first(l): return l[0]
def second(l): return l[1]
def last(l): return l[-1]
def sym(x): return x

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
          ako     = [float if row[n][0] in "$<>" else sym for n in use]
        if n > 0:
          row     = [x if x[0]==skip else p(x) for x,p in zip(row,ako)]
          rows   += [row]
    return o(file=file, ako=ako, head=hdr, objs=objs, 
             decs=decs, weights=weights, rows=rows)

def main(calling, d, argv=None):
  "Configure command line parser from keys of dictonary 'd'"
  argv = argv or sys.argv[1:]
  opts = 'h%s' % ''.join(['%s:' % k[0] for k in d.keys()])
  oops = lambda x="": print(x) or sys.exit(2)
  try:
    com, args = getopt.getopt(argv,opts)
    for opt, arg in com:
      if opt == '-h':
        print(calling + " -h", end="")
        for k in THE.keys(): 
          print(" -%s %s:%s" % (k[0],k,d[k]),sep="",end="")
        oops()
      else:
        for k in d.keys():
          if opt[1]==k[0]:
            try: new= int(arg)
            except: 
              try: new= float(arg)
              except: new= arg
            if type(d[k]) != type(new): 
              oops('%s expected %s' % (opt,type(d[k]).__name__))
            d[k] = new
  except getopt.GetoptError as err: oops(err)

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
   main("pypy3 smore.py",THE)
   demo(act=THE.MAIN)
