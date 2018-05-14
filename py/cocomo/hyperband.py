import auto 

def bands(lst,n=3):
  "best at end"
  r,i,j = 1,len(lst),len(lst)
  while i > 0:
    yield r,lst[j-i:]
    i /= n
    r *= n

def dom(r1,r2, lows,highs):
  s1,s2,n,e,z = 0,0,len(r1.y),10,10**-32
  for a,b,w,lo,hi in zip(r1.y,r2.y,r1.w,lows,highs):
    a   = (a - lo) / (hi - lo + z)
    b   = (b - lo) / (hi - lo + z)
    s1 -= e**( w * (a-b)/n )
    s2 -= e**( w * (b-a)/n )
  return s1/n < s2/n

def doms(lst):
  def ranges(lst):
    lo = [ 10**32 for _ in lst[0].y]
    hi = [-10**32 for _ in lst[0].y]
    for r1 in lst:
      for n,obj in enumerate(r1.y):
        lo[n] = min(obj, lo[n])
        hi[n] = max(obj, hi[n])
    return lo,hi  
  lows,highs = ranges(lst)
  for x in lst:
    for y in lst:
      if dom(x,y,lows,highs):
        x.dom += 1
  return lst

class row:
  def __init__(i,x,y,w): 
    i.w,i.x,i.y,i.dom = w,x,y,0

class xy:
  def __init__(i,head,rows):
    objs = [n for n,x in enumerate(head) if x[0] in '<>']
    decs = [n for n,x in enumerate(head) if not n in objs]
    i.weights =  [-1 if head[n][0]=="<" else 1 for n in objs]
    i.rows = [ row([ x[n] for n in decs ], 
                   [ x[n] for n in objs ], 
                   i.weights) for x in rows]
    doms(i.rows)
    i.rows = sorted(i.rows, key=lambda z:z.dom)
    for x in i.rows[:10]: print("<",x.y, x.dom)
    for x in i.rows[-10:]: print(">",x.y, x.dom)
xy(auto.data[0],auto.data[1:])

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
