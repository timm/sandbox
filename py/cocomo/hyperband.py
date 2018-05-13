
def bands(lst,n=3):
  "best at end"
  r,i,j = 1,len(lst),len(lst)
  while i > 0:
    yield r,lst[j-i:]
    i /= n
    r *= n

#rows have id and objs and __lt__
# use Dom(lst);sorted(lst) and you'll e god
class Dom:
  "a divide and conqueor dom algorithm"
  def __init__(i,lst, ws,nth=3,p=0.5)
    i.chunks = len(lst)**0.5
    i.lows,i.highs = i.ranges(lst)
    for one in lst: one.rank = 0
    i.main(0,ws,nth, 
           random.shuffle(lst))
  #------------------------------
  def ranges(i,lst):
    "find min max of all ojectives"
    lo,hi = {},{}
    for one in lst:
      for n,obj in enumerate(one.obj):
        lo[n] = min(obj, lo.get(n, 10**32))
        hi[n] = max(obj, hi.get(n,-10**32))
    return lo,hi      
  #------------------------------
  def main(i,level,ws,nth,lst):
    "dom per chunk, promote best half of each chunk"
    while len(lst) > chunks:
      tmp = []
      for chunk in i.chunkify( lst ) :
        best,rest = i.bore( i.doms(chunk), 0.5):
        tmp += best
      level += 1
      lst = tmp
      for one in lst: one.rank = level
  #--------------------------
  def chunkify(i,lst):
    a,b,c = 0, len(lst), int(len(lst))/i.chunks
    while a < b:
      yield lst[a:a+c]
      a += c
  #------------------------------
  def bore(i,d,n): # best or rest
    "return best part, rest part"
    some = -1 * int( len(d.keys()) * n )
    lst  = sorted(list(d.values))
    return lst[some:], lst[:some]
  #------------------------------
  def doms(i,lst):
    "given n individuals, how often does each dominate?"
    dom = {}
    for one in lst:
      k = id(one)
      for two in lst:
        if i.dom(one, two):
          dom[k] = dom[k] if k in dom else one
          one.dom += 1
    return dom
  #------------------------------
  def  dom(i.x,y):
    "given two individuals, which domiantes?"
    s1,s2,n = 0,0,len(x.objs)
    z = -10**32
    n = len(x.objs)
    for a,b,w,lo,hi in zip(x.objs,y.objs,ws,i.lows,i.highs):
        a   = (a - lo) / (hi - lo + z)
        b   = (b - lo) / (hi - lo + z)
        s1 -= e**( w * (a-b)/n )
        s2 -= e**( w * (b-a)/n )
    return s1/n < s2/n
  
