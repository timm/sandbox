import random

r = random.random

def seed(n=1)   : random.seed(n)
def none(x)     : return None
def zero(x)     : return 0
def identity(x) : return x
def inc(x)      : return x+1

def dbscan(values2d ,n=1):
  grid, nums, size = {}, {}, len( values2d[0] )
  for i in range(size):
    nums[i] = Num( values2d, f=lambda z: z[i] )
  for vals in values2d:
    pos = [ n.dot(x) for x,n in zip(vals, nums) ]
    cell, grid = cell(pos, 
                      d     = grid,
                      init  = lambda  : Cell(nums) 
                      update= lambda z: z.place(pos,vals))
    
def cell(lst, d=None, init=zero, update=identity):
  if d == None: d={}
  last = lst[-1]
  e = d
  for x in lst[:-1]:
    print('x',x)
    f = e.get(x,None)
    if f == None:
      e[x] = {}
    e = e[x]
  val = e[last] = update( e.get( last,init() ) )
  return val,d

def empty(grid, pos):
  for x in pos:
    x = grid.get(x,None)
    if x == None:
      return False
  return True


class Cell:
  def __init__(i,nums): 
    i.vals,i.pos,i.nums = [],None,nums
  def place(i,pos,vals):
    i.pos = pos
    i.vals += [ vals ]
  def __repr__(i):
    return str(dict(pos=i.pos, vals=len(i.vals)))
  def neighbors(i,grid):
    for pos in nearby(i.pos):
      if pos != i.pos:
        if not empty(grid,pos):
          bad=False
          for x,num in zip(pos, i.nums):
            if x < 0 or x >= num.max():
              bad = True
          if not bad:
            yield pos

def nearby(lst):
    out = []
    # 1-dimension
    if len(lst) == 1:
        out += [[lst[0] - 1]]  # left
        out += [[lst[0]    ]]  # current
        out += [[lst[0] + 1]]  # right
        return out
    # n-dimensional
    for sub in nearby(lst[1:]):
        out += [[lst[0] - 1] + sub]  # left
        out += [[lst[0]    ] + sub]  # center
        out += [[lst[0] + 1] + sub]  # right
    return out

class Num:
  def __init__(i, inits=[], f=identity, cohen=0.3):
    i.n = i.mu = i.m2 = i.sd = 0
    i.epsilon = 1
    i.lo, i.hi = 10**8, -10**8
    i.f, i.cohen = f, cohen
    i.adds(inits)
  def dot(i,x) :
    return int((x - i.lo) / i.epsilon)
  def max(i) :
    return int((i.hi - i.lo) / i.epsilon)
  def __repr__(i):
    return '(%5.3f %5.3f %5.3f)' % (
            i.mu, i.sd, i.epsilon)
  def adds(i,lst): [ i.add(x) for x in lst ]
  def add(i,x):
    x = i.f(x)
    i.n += 1
    if x < i.lo : i.lo = x 
    if x > i.hi : i.hi = x
    delta = x - i.mu
    i.mu += delta / i.n
    i.m2 += delta * (x - i.mu)
    if i.n > 1 :
       i.sd = (i.m2 / (i.n - 1))**0.5
       i.epsilon = i.cohen * i.sd
    return x

def show(points,m=10,n=20):
  zs = 0
  a = [ [ 0 for _ in range(m) ] for _ in range(n) ]
  for (x,y) in points:
    x,y = int(n*x), int(n*y)
    a[x][y] += 1
  for y in range(n):
    for x in range(m):
      z= 100*a[x][y]/len(points) 
      z= int(z + 0.5)
      zs += z
      z = " " if z < 1 else z
      print("%2s" % z, end="")
    print("")
  print(zs)

if __name__ == '__main__':
  data = []
  seed()
  for i in range(1000):
    z = 3
    a = r()**(1/z)
    b = a + (1 - a)*r()
    c = r()**z
    d = c*r()
    data += [ (a,b), (c,d) ]
  d=None
  for _ in range(10):
    n,d = cell( [1,2,3], d, update=inc)
  print((n,d), cell([1,2,3],d))
  #show(data)
  #dbscan(data)
