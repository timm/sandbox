#!/usr/bin/env python3
import sys,random

########################################
seed = random.seed
r    = random.random
any  = random.choice
nump = lambda z: isinstance(z,(float,int))

def kv(d):
  out = lambda x: round(x,THE.decimals) if nump(x) else x
  return '('+', '.join(['%s: %s' % (k,out(d[k]))
          for k in sorted(d.keys())
          if not k[0] is "_"]) + ')'

########################################
class o:
  def __repr__(i): return i.__class__.__name__ + kv(i.__dict__)
  def __init__(i, **l): i.__dict__.update(l)

THE = o(decimals=3, skip='?')

class Num(o):
  def __init__(i, lo= 10**32, hi= -10**32): 
    i.n,i.mu,i.m2,i.sd,i.lo,i.hi = 0,0,0,0,lo,hi
  def __add__(i,x):
    i.n   += 1
    i.lo   = min(x, i.lo)  
    i.hi   = max(x, i.hi)  
    delta  = x - i.mu
    i.mu  += delta/i.n
    i.m2  += delta*(x - i.mu)
  def sd(i): 
    return (i.m2/(i.n - 1))**0.5
  def norm(i, x, z=10**-32):
    return  (x - i.lo) / (i.hi - i.lo + z)

class Sym(o):
  def __init__(i):  
    i.n, i.seen, _cdf = 0, {}, None
  def __add__(i,x): 
    i.n += 1
    i.seen[x] = i.seen.get(x,0) + 1
    i._cdf = None
  def cdf(i):
    i._cdf = i._cdf or sorted(
                         [(k[d]/i.n, k) for k in i.seen], 
                         reverse=True)
    return i._cdf
  def any(i):
    z = r()
    for p,k in i.cdf():
      z -= p
      if z <= 0: return k
    return k

class Col(o):
  def __init__(i,pos, txt): 
    i.pos, i.txt, i.has, i.w = pos, txt, None, -1
  def __add__(i,x):
    if x is not THE.skip:
      i.has = i.has or (Num() if nump(x) else Sym())
      i.has + x

class Row(o):
  id = 0
  def __init__(i,cells,t): 
    i.dom,i.cells= 0,cells
    i.id = Row.id = Row.id + 1 
    for col in t.cols: col + cells[ col.pos ]
  def dominates(i,j,t, e=2.71828):
    s1,s2,n = 0,0,len(t.outs)
    for col in t.outs :
      a   = col.has.norm( i.cells[ col.pos ] )
      b   = col.has.norm( j.cells[ col.pos ] )
      s1 -= e**( col.w * (a-b)/n )
      s2 -= e**( col.w * (b-a)/n )
    return s1/n < s2/n

class Table(o):
  def __init__(i, rows=[], cols=[]):
    i.cols = i.words2cols(cols)
    i.rows = [ Row(row,i) for row in rows ]
    i.dominates()
  def words2cols(i, words ):
    cols   = [ Col(j,x) for j,x in enumerate( words )     ]
    i.less = [ c for c in cols if c.txt[0] == "<"      ]
    i.more = [ c for c in cols if c.txt[0] == ">"      ]
    i.ins  = [ c for c in cols if c.txt[0] not in "<>" ]
    i.outs = [ c for c in cols if c.txt[0]     in "<>" ]
    for col in i.more: col.w =  1
    for col in i.less: col.w = -1
    return cols
  def dominates(i):
    for row1 in i.rows:
      for row2 in i.rows:
        if row1.dominates(row2,i):
          row1.dom += 1
    i.rows = sorted(i.rows, 
                    reverse= True,
                    key= lambda z: z.dom) 
    print([row.dom for row in i.rows])

########################################
def choice(lst,items):
    tmp = r(items)
    return choice(lst) if lst[tmp] == None else tmp

### need to keep the indexes around
def one(all, less):
    out = {f1:choice(lst1,len(lst1)) for f1,lst1 in all.items()}
    for constraints in less:
        for f2,lst2 in constraints.items():
            out[f2] = choice(all[f2],lst2)
    return out

vl, l, n, h, vh, xh = 'vl', 'l', 'n', 'h', 'vh', 'xh'

Table(cols=['id', 
            'center',
            'year',
            'Prec', #{h}
            'Flex', #{h}
            'Resl', #{h}
            'Team', #{vh}
            'Pmat', #{l,n,h}
            'rely', #{l,n,h,vh}
            'data', #{l,n,h,vh}
            'cplx', #{l,n,h,vh,xh}
            'ruse', #{n}
            'docu', #{n}
            'time', #{n,h,vh,xh}
            'stor', #{n,h,vh,xh}
            'pvol', #{l,n,h}
            'acap', #{n,h,vh}
            'pcap', #{n,h,vh}
            'pcon', #{n} 
            'apex', #{l,n,h,vh}
            'plex', #{vl,l,n,h}
            'ltex', #{vl,l,n,h}
            'tool', #{n,h}
            'site', #{n}
            'sced', #{n,l,h}
            'kloc',
            '<effort',   # development effort in months (one month =152 hours. 
                         #  includes development+ management)
            '<defects',  # observed defects
            '<months'    # calendar months to develop (so staff = effort/months)
            ],
        rows=[
            [1,2,1979,h,h,h,vh,h,h,l,h,n,n,n,n,l,n,n,n,n,n,h,n,n,l,25.9,117.6,808,15.3],
            [2,2,1979,h,h,h,vh,h,h,l,h,n,n,n,n,l,n,n,n,n,n,h,n,n,l,24.6,117.6,767,15],
            [3,2,1979,h,h,h,vh,h,h,l,h,n,n,n,n,l,n,n,n,n,n,h,n,n,l,7.7,31.2,240,10.1],
            [4,2,1979,h,h,h,vh,h,h,l,h,n,n,n,n,l,n,n,n,n,n,h,n,n,l,8.2,36,256,10.4],
            [5,2,1979,h,h,h,vh,h,h,l,h,n,n,n,n,l,n,n,n,n,n,h,n,n,l,9.7,25.2,302,11],
            [6,2,1979,h,h,h,vh,h,h,l,h,n,n,n,n,l,n,n,n,n,n,h,n,n,l,2.2,8.4,69,6.6],
            [7,2,1979,h,h,h,vh,h,h,l,h,n,n,n,n,l,n,n,n,n,n,h,n,n,l,3.5,10.8,109,7.8],
            [8,2,1982,h,h,h,vh,h,h,l,h,n,n,n,n,l,n,n,n,n,n,h,n,n,l,66.6,352.8,2077,21],
            [9,1,1980,h,h,h,vh,h,h,l,h,n,n,xh,xh,l,h,h,n,h,n,h,h,n,n,7.5,72,226,13.6],
            [10,1,1980,h,h,h,vh,n,n,l,h,n,n,n,n,l,h,vh,n,vh,n,h,n,n,n,20,72,566,14.4],
            [11,1,1984,h,h,h,vh,n,n,l,h,n,n,n,n,l,h,h,n,vh,n,h,n,n,n,6,24,188,9.9],
            [12,1,1980,h,h,h,vh,n,n,l,h,n,n,n,n,l,h,vh,n,vh,n,h,n,n,n,100,360,2832,25.2],
            [13,1,1985,h,h,h,vh,n,n,l,h,n,n,n,n,l,h,n,n,vh,n,l,n,n,n,11.3,36,456,12.8],
            [14,1,1980,h,h,h,vh,n,n,l,h,n,n,n,n,h,h,h,n,h,l,vl,n,n,n,100,215,5434,30.1],
            [15,1,1983,h,h,h,vh,n,n,l,h,n,n,n,n,l,h,h,n,vh,n,h,n,n,n,20,48,626,15.1],
            [16,1,1982,h,h,h,vh,n,n,l,h,n,n,n,n,l,h,n,n,n,n,vl,n,n,n,100,360,4342,28],
            [17,1,1980,h,h,h,vh,n,n,l,h,n,n,n,xh,l,h,vh,n,vh,n,h,n,n,n,150,324,4868,32.5],
            [18,1,1984,h,h,h,vh,n,n,l,h,n,n,n,n,l,h,h,n,h,n,h,n,n,n,31.5,60,986,17.6],
            [19,1,1983,h,h,h,vh,n,n,l,h,n,n,n,n,l,h,h,n,vh,n,h,n,n,n,15,48,470,13.6],
            [20,1,1984,h,h,h,vh,n,n,l,h,n,n,n,xh,l,h,n,n,h,n,h,n,n,n,32.5,60,1276,20.8],
            [21,2,1985,h,h,h,vh,h,h,l,h,n,n,n,n,l,n,n,n,n,n,h,n,n,l,19.7,60,614,13.9],
            [22,2,1985,h,h,h,vh,h,h,l,h,n,n,n,n,l,n,n,n,n,n,h,n,n,l,66.6,300,2077,21],
            [23,2,1985,h,h,h,vh,h,h,l,h,n,n,n,n,l,n,n,n,n,n,h,n,n,l,29.5,120,920,16],
            [24,2,1986,h,h,h,vh,n,h,n,n,n,n,h,n,n,n,h,n,h,n,n,n,n,n,15,90,575,15.2],
            [25,2,1986,h,h,h,vh,n,h,n,h,n,n,n,n,n,n,h,n,h,n,n,n,n,n,38,210,1553,21.3],
            [26,2,1986,h,h,h,vh,n,n,n,n,n,n,n,n,n,n,h,n,h,n,n,n,n,n,10,48,427,12.4],
            [27,2,1982,h,h,h,vh,h,n,vh,h,n,n,vh,vh,l,vh,n,n,h,l,h,n,n,l,15.4,70,765,14.5],
            [28,2,1982,h,h,h,vh,h,n,vh,h,n,n,vh,vh,l,vh,n,n,h,l,h,n,n,l,48.5,239,2409,21.4],
            [29,2,1982,h,h,h,vh,h,n,vh,h,n,n,vh,vh,l,vh,n,n,h,l,h,n,n,l,16.3,82,810,14.8],
            [29,2,1982,h,h,h,vh,h,n,vh,h,n,n,vh,vh,l,vh,n,n,h,l,h,n,n,l,12.8,62,636,13.6],
            [31,2,1982,h,h,h,vh,h,n,vh,h,n,n,vh,vh,l,vh,n,n,h,l,h,n,n,l,32.6,170,1619,18.7],
            [32,2,1982,h,h,h,vh,h,n,vh,h,n,n,vh,vh,l,vh,n,n,h,l,h,n,n,l,35.5,192,1763,19.3],
            [33,2,1985,h,h,h,vh,h,h,l,h,n,n,n,n,l,n,n,n,n,n,h,n,n,l,5.5,18,172,9.1],
            [34,2,1987,h,h,h,vh,h,h,l,h,n,n,n,n,l,n,n,n,n,n,h,n,n,l,10.4,50,324,11.2],
            [35,2,1987,h,h,h,vh,h,h,l,h,n,n,n,n,l,n,n,n,n,n,h,n,n,l,14,60,437,12.4],
            [36,2,1986,h,h,h,vh,n,h,n,h,n,n,n,n,n,n,n,n,n,n,n,n,n,n,6.5,42,290,12],
            [37,2,1986,h,h,h,vh,n,n,n,h,n,n,n,n,n,n,n,n,n,n,n,n,n,n,13,60,683,14.8],
            [38,2,1986,h,h,h,vh,h,n,n,h,n,n,n,n,n,n,h,n,n,n,h,h,n,n,90,444,3343,26.7],
            [39,2,1986,h,h,h,vh,n,n,n,h,n,n,n,n,n,n,n,n,n,n,n,n,n,n,8,42,420,12.5],
            [40,2,1986,h,h,h,vh,n,n,n,h,n,n,h,n,n,n,n,n,n,n,n,n,n,n,16,114,887,16.4],
            [41,2,1980,h,h,h,vh,h,n,h,h,n,n,vh,h,l,h,h,n,n,l,h,n,n,l,177.9,1248,7998,31.5],
            [42,6,1975,h,h,h,vh,h,h,l,h,n,n,n,n,l,n,h,n,n,n,n,n,n,n,302,2400,8543,38.4],
            [43,5,1982,h,h,h,vh,h,n,h,l,n,n,n,n,h,h,n,n,h,n,n,h,n,n,282.1,1368,9820,37.3],
            [44,5,1982,h,h,h,vh,h,h,h,l,n,n,n,n,n,h,n,n,h,n,n,n,n,n,284.7,973,8518,38.1],
            [45,5,1982,h,h,h,vh,n,h,h,n,n,n,n,n,l,n,h,n,h,n,h,n,n,n,79,400,2327,26.9],
            [46,5,1977,h,h,h,vh,l,l,n,n,n,n,n,n,l,h,vh,n,h,n,h,n,n,n,423,2400,18447,41.9],
            [47,5,1977,h,h,h,vh,h,n,n,n,n,n,n,n,l,h,vh,n,vh,l,h,n,n,n,190,420,5092,30.3],
            [48,5,1984,h,h,h,vh,h,n,n,h,n,n,n,h,n,h,n,n,h,n,h,n,n,n,47.5,252,2007,22.3],
            [49,5,1980,h,h,h,vh,l,vh,n,xh,n,n,h,h,l,n,n,n,h,n,n,h,n,n,21,107,1058,21.3],
            [50,5,1983,h,h,h,vh,l,n,h,h,n,n,vh,n,n,h,h,n,h,n,h,n,n,n,78,571.4,4815,30.5],
            [51,5,1984,h,h,h,vh,l,n,h,h,n,n,vh,n,n,h,h,n,h,n,h,n,n,n,11.4,98.8,704,15.5],
            [52,5,1985,h,h,h,vh,l,n,h,h,n,n,vh,n,n,h,h,n,h,n,h,n,n,n,19.3,155,1191,18.6],
            [53,5,1979,h,h,h,vh,l,h,n,vh,n,n,h,h,l,h,n,n,n,h,h,n,n,n,101,750,4840,32.4],
            [54,5,1979,h,h,h,vh,l,h,n,h,n,n,h,h,l,n,n,n,h,n,n,n,n,n,219,2120,11761,42.8],
            [55,5,1979,h,h,h,vh,l,h,n,h,n,n,h,h,l,n,n,n,h,n,n,n,n,n,50,370,2685,25.4],
            [56,2,1979,h,h,h,vh,h,vh,h,h,n,n,vh,vh,n,vh,vh,n,vh,n,h,h,n,l,227,1181,6293,33.8],
            [57,2,1977,h,h,h,vh,h,n,h,vh,n,n,n,n,l,h,vh,n,n,l,n,n,n,l,70,278,2950,20.2],
            [58,2,1979,h,h,h,vh,h,h,l,h,n,n,n,n,l,n,n,n,n,n,h,n,n,l,0.9,8.4,28,4.9],
            [59,6,1974,h,h,h,vh,l,vh,l,xh,n,n,xh,vh,l,h,h,n,vh,vl,h,n,n,n,980,4560,50961,96.4],
            [60,6,1975,h,h,h,vh,n,n,l,h,n,n,n,n,l,vh,vh,n,n,h,h,n,n,n,350,720,8547,35.7],
            [61,5,1976,h,h,h,vh,h,h,n,xh,n,n,h,h,l,h,n,n,n,h,h,h,n,n,70,458,2404,27.5],
            [62,5,1979,h,h,h,vh,h,h,n,xh,n,n,h,h,l,h,n,n,n,h,h,h,n,n,271,2460,9308,43.4],
            [63,5,1971,h,h,h,vh,n,n,n,n,n,n,n,n,l,h,h,n,h,n,h,n,n,n,90,162,2743,25],
            [64,5,1980,h,h,h,vh,n,n,n,n,n,n,n,n,l,h,h,n,h,n,h,n,n,n,40,150,1219,18.9],
            [65,5,1979,h,h,h,vh,n,h,n,h,n,n,h,n,l,h,h,n,h,n,h,n,n,n,137,636,4210,32.2],
            [66,5,1977,h,h,h,vh,n,h,n,h,n,n,h,n,h,h,h,n,h,n,h,n,n,n,150,882,5848,36.2],
            [67,5,1976,h,h,h,vh,n,vh,n,h,n,n,h,n,l,h,h,n,h,n,h,n,n,n,339,444,8477,45.9],
            [68,5,1983,h,h,h,vh,n,l,h,l,n,n,n,n,h,h,h,n,h,n,h,n,n,n,240,192,10313,37.1],
            [69,5,1978,h,h,h,vh,l,h,n,h,n,n,n,vh,l,h,h,n,h,h,h,n,n,l,144,576,6129,28.8],
            [70,5,1979,h,h,h,vh,l,n,l,n,n,n,n,vh,l,h,h,n,h,h,h,n,n,l,151,432,6136,26.2],
            [71,5,1979,h,h,h,vh,l,n,l,h,n,n,n,vh,l,h,h,n,h,h,h,n,n,l,34,72,1555,16.2],
            [72,5,1979,h,h,h,vh,l,n,n,h,n,n,n,vh,l,h,h,n,h,h,h,n,n,l,98,300,4907,24.4],
            [73,5,1979,h,h,h,vh,l,n,n,h,n,n,n,vh,l,h,h,n,h,h,h,n,n,l,85,300,4256,23.2],
            [74,5,1982,h,h,h,vh,l,n,l,n,n,n,n,vh,l,h,h,n,h,h,h,n,n,l,20,240,813,12.8],
            [75,5,1978,h,h,h,vh,l,n,l,n,n,n,n,vh,l,h,h,n,h,h,h,n,n,l,111,600,4511,23.5],
            [76,5,1978,h,h,h,vh,l,h,vh,h,n,n,n,vh,l,h,h,n,h,h,h,n,n,l,162,756,7553,32.4],
            [77,5,1978,h,h,h,vh,l,h,h,vh,n,n,n,vh,l,h,h,n,h,h,h,n,n,l,352,1200,17597,42.9],
            [78,5,1979,h,h,h,vh,l,h,n,vh,n,n,n,vh,l,h,h,n,h,h,h,n,n,l,165,97,7867,31.5],
            [79,5,1984,h,h,h,vh,h,h,n,vh,n,n,h,h,l,h,n,n,n,h,h,n,n,n,60,409,2004,24.9],
            [80,5,1984,h,h,h,vh,h,h,n,vh,n,n,h,h,l,h,n,n,n,h,h,n,n,n,100,703,3340,29.6],
            [81,2,1980,h,h,h,vh,n,h,vh,vh,n,n,xh,xh,h,n,n,n,n,l,l,n,n,n,32,1350,2984,33.6],
            [82,2,1980,h,h,h,vh,h,h,h,h,n,n,vh,xh,h,h,h,n,h,h,h,n,n,n,53,480,2227,28.8],
            [83,3,1977,h,h,h,vh,h,h,l,vh,n,n,vh,xh,l,vh,vh,n,vh,vl,vl,h,n,n,41,599,1594,23],
            [84,3,1977,h,h,h,vh,h,h,l,vh,n,n,vh,xh,l,vh,vh,n,vh,vl,vl,h,n,n,24,430,933,19.2],
            [85,5,1977,h,h,h,vh,h,vh,h,vh,n,n,xh,xh,n,h,h,n,h,h,h,n,n,n,165,4178.2,6266,47.3],
            [86,5,1977,h,h,h,vh,h,vh,h,vh,n,n,xh,xh,n,h,h,n,h,h,h,n,n,n,65,1772.5,2468,34.5],
            [87,5,1977,h,h,h,vh,h,vh,h,vh,n,n,xh,xh,n,h,h,n,h,h,h,n,n,n,70,1645.9,2658,35.4],
            [88,5,1977,h,h,h,vh,h,vh,h,xh,n,n,xh,xh,n,h,h,n,h,h,h,n,n,n,50,1924.5,2102,34.2],
            [89,5,1982,h,h,h,vh,l,vh,l,vh,n,n,vh,xh,l,h,n,n,l,vl,l,h,n,n,7.25,648,406,15.6],
            [90,5,1980,h,h,h,vh,h,vh,h,vh,n,n,xh,xh,n,h,h,n,h,h,h,n,n,n,233,8211,8848,53.1],
            [91,2,1983,h,h,h,vh,n,h,n,vh,n,n,vh,vh,h,n,n,n,n,l,l,n,n,n,16.3,480,1253,21.5],
            [92,2,1983,h,h,h,vh,n,h,n,vh,n,n,vh,vh,h,n,n,n,n,l,l,n,n,n,6.2,12,477,15.4],
            [93,2,1983,h,h,h,vh,n,h,n,vh,n,n,vh,vh,h,n,n,n,n,l,l,n,n,n,3,38,231,12]])
            
def ground():
  "JPL ground systems"
  return dict(
    kloc=range(11,392),
    Pmat = [2,3],         acap = [3,4,5],
    aexp = [2,3,4,5],     cplx = [1,2,3,4],
    data = [2,3],         rely = [1,2,3,4],
    ltex = [1,2,3,4],     pcap = [3,4,5],
    pexp = [1,2,3,4],     time = [3,4],
    stor = [3,4],
    tool = [2],
    sced = [3])

def osp():
  "Orbital space plane. Flight guidance system."
  return dict(
    kloc= range(75,125),
    Flex = [2,3,4,5],     Pmat = [1,2,3,4],
    Prec = [1,2],         Resl = [1,2,3],
    Team = [2,3],         acap = [2,3],
    aexp = [2,3],         cplx = [5,6],
    docu = [2,3,4],       ltex = [2,3,4],
    pcon = [2,3],         tool = [2,3],
    ruse = [2,3,4],       sced = [1,2, 3],
    stor = [3,4,5],
    data = [3],
    pcap = [3],
    pexp = [3],
    pvol = [2],
    rely = [5],
    site = [3])

def osp2():
  """Osp, version 2. Note there are more restrictions
  here than in osp version1 (since as a project
  develops, more things are set in stone)."""
  return dict(
    kloc= range(75,125),
    docu = [3,4],         ltex = [2,5],
    sced = [2,3,4],       Pmat = [4,5],
    Prec = [3,4, 5],
    Resl = [4],           Team = [3],
    acap = [4],           aexp = [4],
    cplx = [4],           data = [4],
    Flex = [3],           pcap = [3],
    pcon = [3],           pexp = [4],
    pvol = [3],           rely = [5],
    ruse = [4],           site = [6],
    stor = [3],           time = [3],
    tool = [5])

"""

### Defining "Ranges(Treatment)"

Lastly, we need to define what we are going to do to a project.

First, we define a little booking code that remembers all the
treatments and, at load time, checks that the ranges are good.


Ok, now that is done, here are the treatments. Note that they all start
with _@rx_.

"""

def doNothing(): return {}

def improvePersonnel(): return dict(
  acap=[5],pcap=[5],pcon=[5], aexp=[5], pexp=[5], ltex=[5])

def improveToolsTechniquesPlatform(): return dict(
  time=[3],stor=[3],pvol=[2],tool=[5], site=[6])

def improvePrecendentnessDevelopmentFlexibility(): return dict(
  Prec=[5],Flex=[5])

def increaseArchitecturalAnalysisRiskResolution(): return dict(
  Resl=[5])

def relaxSchedule(): return dict(
  sced = [5])

def improveProcessMaturity(): return dict(
  Pmat = [5])

def reduceFunctionality(): return dict(
  data = [2], nkloc=[0.5]) # nloc is a special symbol. Used to change kloc.

def improveTeam(): return dict(
  Team = [5])

def reduceQuality():  return dict(
  rely = [1], docu=[1], time = [3], cplx = [1])

rx = [ doNothing, improvePersonnel, improveToolsTechniquesPlatform,
       improvePrecendentnessDevelopmentFlexibility,
       increaseArchitecturalAnalysisRiskResolution, relaxSchedule,
       improveProcessMaturity, reduceFunctionality, improveTeam,
       reduceQuality]

"""

### Under the Hood: Complete-ing the Ranges.

Now that we have defined _Ranges(Base), Ranges(Project), and
Ranges(Treatment)_, we need some tool to generate the ranges
of the currnet project, given some treatment.
In the  following code:

+ `ranges()` looks up the ranges for `all` COCOMO values; i.e. the _Ranges(Base)_
+ `project()` accesses _Ranges(Project)_. For each of those ranges, we
  override _Ranges(Base)_.
+ Then we impose _Ranges(Treatment)_ to generate a list of valid ranges
  consistent with _Ranges(*)_
+ The guesses from the project are then added to  `ask` which
  pulls on value for each attribute.

```python
def ask(x):
  return random.choice(list(x))
```

And here's the code:


For example, here some code to generate projects that are consistent
with what we know about `flight` projects. Note that we call it three
times and get three different project:

```python

==>
 {'sced': 3, 'cplx': 5, 'site': 2, 'Prec': 3, 'Pmat': 3,
  'acap': 3, 'Flex': 3, 'rely': 5, 'data': 2, 'tool': 2,
  'pexp': 3, 'pcon': 1, 'aexp': 4, 'stor': 4, 'docu': 5,
  'Team': 5, 'pcap': 5, 'kloc': 41, 'ltex': 1, 'ruse': 6,
  'Resl': 2, 'time': 4, 'pvol': 3}

 {'sced': 3, 'cplx': 6, 'site': 5, 'Prec': 4, 'Pmat': 2,
  'acap': 3, 'Flex': 2, 'rely': 5, 'data': 3, 'tool': 2,
  'pexp': 1, 'pcon': 2, 'aexp': 4, 'stor': 3, 'docu': 1,
  'Team': 3, 'pcap': 5, 'kloc': 63, 'ltex': 2, 'ruse': 3,
  'Resl': 4, 'time': 3, 'pvol': 3}

 {'sced': 3, 'cplx': 5, 'site': 5, 'Prec': 4, 'Pmat': 2,
  'acap': 5, 'Flex': 5, 'rely': 3, 'data': 3, 'tool': 2,
   'pexp': 3, 'pcon': 5, 'aexp': 4, 'stor': 4, 'docu': 1,
   'Team': 3, 'pcap': 4, 'kloc': 394, 'ltex': 2, 'ruse': 2,
   'Resl': 1, 'time': 3, 'pvol': 5}
```

## Using  This Code

Finally, we can geterate a range of estiamtes out of this code.
"""
