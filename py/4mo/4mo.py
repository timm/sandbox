from lib import *

def filep(x): return os.path.isfile(x)

ABOUT = dict( 
why  = "4mo: for making multi-objective rules",
who  = "Tim Menzies, MIT license (2 clause)",
when = 2018,
how  = "pypy3 smore.py",
copyright="""
Redistribution and use in source and binary forms, with or without modification,
are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this 
   list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, 
   this list of conditions and the following disclaimer in the documentation 
   and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
  """,
  what = dict(
     cohen=   dict(why  = "define small changes",
	 	   what = [0.2,0.1,0.3,0.5], 
                   want = float)
    ,DATA=    dict(why  = "input data csv file",
		   what = 'auto.csv', 
                   make = str, 
                   want = filep)
    ,decimals=dict(why  = "decimals to display for floats",
		   what = 3, 
                   want = int)
    ,few=     dict(why  = "min bin size = max(few, N ^ power)",
		   what = 10, 
                   want = int)
    ,MAIN=    dict(why  = "start up action",
		   what = "FORMO", 
                   want = same)
    ,power=   dict(why  = "min bin size = max(few, N ^ power)",
		   what = 0.5, 
                   want = float)
    ,undoubt= dict(why  = "doubt reductions must be larger than x*undoubt",
		   what = 1.05, 
                   want = float)
    ,verbose= dict(why  = "trace all calls",
		   what = False, 
                   want = bool)
))

@demo
def FORMO(): print(ABOUT["why"])

#-------------
   
@demo
def CSV(): 
  for n,r in enumerate(data(rows("auto.csv"))): 
    if n< 10: print(r)

class Row(o):
  id = 0
  def __init__(i,x,y): 
    i.x,i.y,i.dom = x,y,0
    i._id = Row.id = Row.id+1
  def __hash__(i):
    return i._id
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
 
class Table:
  def __init__(i,decs,objs):
    i.rows  = []
    i._dom  = False
    i.x     = o(head    = decs,
                nums    = [n for n,x in enumerate(decs) if x[0] == '$'] ,
                syms    = [n for n,x in enumerate(decs) if x[0] != '$'] )
    i.y     = o(head    = objs,
                weights = [1 if x[0]==">" else -1 for x in objs],
                lo      = [ 10**32 for _ in objs],
                hi      = [-10**32 for _ in objs])
  def row(i,decs,objs):
    update  = lambda new,b4,f: new if new=="?" else f(new,b4)
    i.rows += [ Row(decs,objs) ]
    i.y.lo  = [ update(now, b4, min) for now,b4 in zip(objs, i.y.lo) ]
    i.y.hi  = [ update(now, b4, max) for now,b4 in zip(objs, i.y.hi) ]
  def doms(i):
    if not i._dom: 
      i._dom = True
      for row1 in i.rows:
        for row2 in i.rows:
          if row1.dominates(row2, i.y.weights, i.y.lo, i.y.hi):
            row1.dom += 1
    return i
  def splits(i):
    i.doms()
    val={}
    for n in i.x.nums:
      tree = prune( grow( i.rows, x=lambda r:r.x[n], y=lambda r:r.dom) )
      showt( tree, val=showNode )
      for u in leaves(tree):
        if u.simpler:
          key=(n,u.x.lo)
          val[key] = u.y
          u.y.key = key
    for row in i.rows: 
      for n in i.x.syms:
        key = (n, row.x[n])
        tmp = val[key] if key in val else Num()
        tmp.key = key
        tmp.rows += [row]
        tmp + row.dom
        val[key] = tmp
    return val
 
class Range:
  def __init__(i,lo=None, hi=None):
    if hi == None: hi=lo
    i.lo, i.hi = lo, hi

#class Range:
#    def __init__(i,t,n): i.n, i.t, i.act = n, t, None
#    def __eq__(i, z): lambda row: t.rows.x[i.n] == z
#    def __ne__(i, z): lambda row: t.rows.x[i.n] != z
#    def __lt__(i, z): lambda row: t.rows.x[i.n] <  z
#    def __gt__(i, z): lambda row: t.rows.x[i.n] >  z
#    def __le__(i, z): lambda row: t.rows.x[i.n] <= z
#    def __ge__(i, z): lambda row: t.rows.x[i.n] >= z

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
  for x,y in xy(data(rows(file))):
    if t: t.row(x,y)
    else: t = Table(x,y)
  t.doms()
  return t

@demo
def DOM():
  t = table("auto.csv")
  t.rows = sorted(t.rows)
  for row in t.rows[:10]: print("<", row.y,row.dom)
  print()
  for row in t.rows[-10:]: print(">",row.y,row.dom)

@demo
def SPLITS():
  t = table("auto.csv")
  val = t.splits()
  lst = sorted(val.values(),key=lambda z:z.mu,reverse=True)
  for x in lst: print(x.key, x, len(x.rows))
  out = []
  for sub in subsets(lst[:10]):
    one = combine(sub, len(t.rows)**0.6)
    if one:
      out += [one]
  print()
  sized = sorted(out, key=lambda z:(z[2],-z[1].mu))
  seen=[]
  best=-1
  for keys, summary, cardinality in sized: 
    if not cardinality in seen:
      seen += [cardinality]
      if summary.mu > best:
        best = summary.mu
        print(int(summary.mu),summary.n,cardinality, keys)
  #print(sorted(out, key=lambda z: z[1].mu,reverse=True)[0])

def combine(ranges, few):
  print(".",end="")
  ors, keys =  {},{}
  for r in ranges:
    col,val   = r.key
    ors[col]  = set(r.rows) | ors.get(col, set())
    keys[col] = keys.get(col,[]) + [val]
  ands = None
  for one in ors.values(): 
    ands = ands & one if ands else one
  if ands and len(ands) > few:
    return keys,Num(ands, f=lambda r:r.dom),len(ranges)
  
class Thing(o):
  def __init__(i, inits=[],f=lambda z:z):
    i.locals()
    i.rows=[]
    i.n, i._f = 0, f
    [i+x for x in inits]
  def __add__(i,x):
    x = i._f(x)
    if x != '?':
      i.n += 1
      i._add( x )
  def simpler(i,j,k):
    return i.doubt() > THE.undoubt * ( 
           j.doubt() * j.n/i.n + k.doubt() * k.n/i.n ) 

class Num(Thing):
  def locals(i): 
    i.mu = i.m2 =  0
    i.hi = -10**32
    i.lo =  10**32
  def doubt(i): 
    return i.sd()
  def _add(i,x):
    i.hi = max(i.hi,x)
    i.lo = min(i.lo,x)
    delta  = x - i.mu
    i.mu  += delta/i.n
    i.m2  += delta*(x - i.mu)
  def sd(i): 
    return (i.m2/(i.n - 1))**0.5
  def __repr__(i):
    return 'Num'+kv(dict(lo=i.lo,hi=i.hi,mu=i.mu, sd=i.sd(), n=i.n))

class Sym(Thing):
  def locals(i): i.seen, i._ent = {}, None
  def doubt(i): 
    return i.ent()
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

def grow(lst, epsilon=None, few=None, x=same, y=same, klass=Num):
  "returns nil if nothing"
  def makeNode(lst, lvl=0, up=None):
    tmp= o(x= Num( lst, f=x ), y= klass( lst, f=y ),
             level= lvl,
             _up  = up, 
             simpler=False, left = None, right= None) 
    tmp.y.rows = lst
    return tmp
  def X(j):       return  notNull( x( lst[j] ))
  def notNull(x): return  -10**32 if x is '?' else x
  def mid(lo,hi):
    m = m1 = m2 = int(lo +(hi-lo)/2)
    while m1 < hi-1 and X(m1-1) == X(m1)  : m1 += 1
    while m2 > 0    and X(m2)   == X(m2-1): m2 -= 1
    m = m2 if (m-m2) < (m1-m) else m
    return m
  def recurse(lo=0, hi=len(lst), up=None, lvl=0):
    node = makeNode(lst[lo:hi], lvl=lvl, up=up) if lvl else up
    m = mid(lo,hi)
    #print("lo",X(lo),dict(lo=lo,m=m,hi=hi,few=few,left=hi-m, 
    #                      right=m-lo,epsilon=epsilon,xM=X(m),xh=X(hi -1),xRight=X(m)-X(lo),yLeft=X(hi-1)-X(m)))
    if hi - m > few:
      if m - lo > few:
        if X(m) - X(lo) > epsilon:
          if X(hi-1) - X(m) > epsilon:
             node.left = recurse(lo=lo,  hi=m,  up=node,  lvl=lvl+1)
             node.right= recurse(lo=m,   hi=hi, up=node, lvl=lvl+1)
    return node
  lst     = sorted(lst, key=lambda row: notNull(x(row)))
  #print([x(z) for z in lst])
  root    = makeNode(lst)
  epsilon = epsilon or root.x.sd()*THE.cohen
  few     = max(few or len(lst)**THE.power, THE.few)
  print(dict(epsilon=epsilon, few=few))
  return recurse(up=root)

def showt(t, tab="|.. ", pre="",lvl=0,val=lambda z: ""):
  if t:
    if lvl==0: print("")
    val(t)
    print(' ' + tab*lvl + pre)
    if t.left:
      showt(t.left,  tab, "< ", lvl+1, val)
    if t.right:
      showt(t.right, tab, "> ", lvl+1, val)

def showNode(z):
  f = plain if z.simpler else red 
  f('%s y=%6.3g sd=%6.3g  when %6.3g <= x <= %6.3g [%5s]' %(
    "\u2714" if z.simpler else "\u2717", 
    z.y.mu, z.y.sd(),  z.x.lo, z.x.hi,z.y.n))

def _grow(X=same,Y=same,N=10000):
  def flats(y):
      if 33 < y < 66: return y
      return 0
  def show(z): return [X(z), flats(z)]
  #(z)]
  seed(1)
  print("\n--------------------------")
  tree = grow( [show(int(100*r())) for _ in range(N)],
               x=first,
               y=last)
  prune( tree )
  showt( tree, val=showNode )
  print([u.x.lo for u in leaves(tree) if u.simpler])
  return tree

def prune(t):
  for u in subtree(t):
    #if not u.simpler:
      if u.left and u.right:
        if u.y.simpler(u.left.y, u.right.y):
          for v in supertree(u.left) : v.simpler = True
          for w in supertree(u.right): w.simpler = True
  return t

@demo
def GROW0(): 
  _grow(N=4096)

@demo
def GROW1(): 
  _grow(X=lambda x : 0 if x <40 else x,N=64)

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
