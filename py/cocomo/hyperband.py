import auto 

def bands(lst,n=3):
  "best at end"
  r,i,j = 1,len(lst),len(lst)
  while i > 0:
    yield r,lst[j-i:]
    i /= n
    r *= n

def kv(d,keys=None, decimals=3):
   "print dictionary, in key sort order"
   keys = keys or sorted(list(d.keys()))
   pretty = lambda x: round(x,decimals) if isinstance(x,float) else x
   return '<'+', '.join(['%s: %s' % (k, pretty(d[k])) for k in keys)  + '>'

class o(object):
  "Javascript envy. Now 'o' is like a JS object."
  def __init__(i, **l)    : i.__vals().update(l)
  def __getitem__(i, k)   : return i.__dict__[k]
  def __setitem__(i, k, v): return i.__dict__[k] = v
  def __repr__(i):
    return i.__class__.__name__ + kv(i.__dict__,i.__keys())
  def __keys(j): 
    return [k for k in sorted(i.__dict__.)keys()) if not k[0] is "_"]

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

class Rules:
  def __init__(i,data):
    t = Table(data[0], data[1:])

def nodes(t):
  if t:
    yield t
    for kid in [t.left, t.right]:
      for z in nodes(kid):
        yield z

# needs to 
def splits(lst, epsilon=None, few=None, x=same, y=same):
  def val(j): return x( lst[j] )
  def worker(lo, hi, parent, lvl):
    m1 = m2 = m = lo + (hi - lo) // 2
    while m1 < hi-1 and val(m1) == val(m1+1): m1 += 1
    while m2 > 0    and val(m2) == val(m2-1): m2 -= 1
    m = m1 if (m1 - m) < (m - m2) else m2
    node = o(x= Num( lst[lo:hi], f=x ),
             y= Num( lst[lo:hi], f=y ),
             level=lvl,
             _parent=parent, cut=None, left=None, right=None) 
    if hi - lo > few:
      if val(hi-1) - val(lo) > epsilon:
        if m is not lo and m is not hi-1:
          node.cut=m
          left  = worker(lo,  m, node, lvl+1)
          right = worker(m,  hi, node, lvl+1)
          if left.cut and right.cut:
            cuts += [m]
            node.left = left
            node.right = right
    return node
  # main ------------------
  cuts    = []
  epsilon = epsilon or Num(inits=lst,f=x).sd()*THE.cohen
  few     = few     or len(lst)**THE.power
  few     = max(few,THE.few)
  lst     = sorted(lst, key=x)
  return cuts,worker( 0, len(lst), None, 0) 
 
Rules(auto.data)

# #rows have id and objs and __lt__
# def chunkify(lst):
#   a,b,c = 0, len(lst), int(len(lst))/chunks
#   while a < b:
#     yield lst[a:a+c]
#     a += c
# 
# def best(d, nth): 
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
