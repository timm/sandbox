import random

def tunings(_ = None):
  Within(txt="loc", lo=2, hi=2000)
  prep([
  #       vlow  low   nom   high  vhigh xhigh
  # scale factors:
  'Flex', 5.07, 4.05, 3.04, 2.03, 1.01,    _],[ 
  'Pmat', 7.80, 6.24, 4.68, 3.12, 1.56,    _],[ 
  'Prec', 6.20, 4.96, 3.72, 2.48, 1.24,    _],[ 
  'Resl', 7.07, 5.65, 4.24, 2.83, 1.41,    _],[ 
  'Team', 5.48, 4.38, 3.29, 2.19, 1.01,    _],[ 
  # effort multipliers:
  'acap', 1.42, 1.19, 1.00, 0.85, 0.71,    _],[
  'aexp', 1.22, 1.10, 1.00, 0.88, 0.81,    _],[
  'cplx', 0.73, 0.87, 1.00, 1.17, 1.34, 1.74],[
  'data',    _, 0.90, 1.00, 1.14, 1.28,    _],[
  'docu', 0.81, 0.91, 1.00, 1.11, 1.23,    _],[
  'ltex', 1.20, 1.09, 1.00, 0.91, 0.84,    _],[
  'pcap', 1.34, 1.15, 1.00, 0.88, 0.76,    _],[
  'pcon', 1.29, 1.12, 1.00, 0.90, 0.81,    _],[
  'plex', 1.19, 1.09, 1.00, 0.91, 0.85,    _],[
  'pvol',    _, 0.87, 1.00, 1.15, 1.30,    _],[
  'rely', 0.82, 0.92, 1.00, 1.10, 1.26,    _],[
  'ruse',    _, 0.95, 1.00, 1.07, 1.15, 1.24],[
  'sced', 1.43, 1.14, 1.00, 1.00, 1.00,    _],[
  'site', 1.22, 1.09, 1.00, 0.93, 0.86, 0.80],[
  'stor',    _,    _, 1.00, 1.05, 1.17, 1.46],[
  'time',    _,    _, 1.00, 1.11, 1.29, 1.63],[
  'tool', 1.17, 1.09, 1.00, 0.90, 0.78,    _])

def COCOMO2(project, t, a=2.94, b=0.91, e=2.7182818285):
  em = t.acap() * t.aexp() * t.cplx() * t.data() * t.docu() * \
       t.ltex() * t.pcap() * t.pcon() * t.plex() * t.pvol() *  \
       t.rely() * t.ruse() * t.sced() * t.site() * t.stor() *   \
       t.time() * t.tool() 
  sf = t.flex() + t.pmat() + t.prec() + t.resl() + t.team()
  return a*em*loc()**(b+ 0.01*sf)
 
#####################################################
class o:
  def __init__(i, **d): i.__dict__.update(d)

def X(y): return y() if callable(y) else y

def prep(*rows):
  [ OneOf(row[0],row[1:]) for row in rows]

class Var:
  all = o()
  def __init__(i, txt) :
    Var.all.__dict__[txt] = i
    i.txt = txt
    i.local = None
    i.reset()
  def reset(i): i.cache = Cache(i.any)
  def any(i): return random.choice(i.local) if i.local else i.any1()
  def __call__(i)      : return i.cache()
  def __neg__(i)       : return -1*X(i)
  def __pos__(i)       : return +1*X(i)
  def __abs__(i)       : return abs(X(i))
  def __lt__(i,j)      : return X(i) <  X(j)
  def __gt__(i,j)      : return X(i) >  X(j)
  def __le__(i,j)      : return X(i) <= X(j)
  def __ge__(i,j)      : return X(i) >= X(j)
  def __ne__(i,j)      : return X(i) != X(j)
  def __eq__(i,j)      : return X(i) == X(j)
  def __add__(i,j)     : return X(i) +  X(j)
  def __sub__(i,j)     : return X(i) -  X(j)
  def __mul__(i,j)     : return X(i) *  X(j)
  def __mod__(i,j)     : return X(i) %  X(j)
  def __pow__(i,j)     : return X(i) ** X(j)
  def __truediv__(i,j) : return X(i) /  X(j)
  def __floordiv__(i,j): return X(i) // X(j)

class Within(Var):
  def __init__(i, txt, lo=0, hi=1):
    super().__init__(txt)
    i.lo, i.hi = lo,hi
  def xplain(i,x): return x
  def any1(i): 
    return random.uniform(i.lo, i.hi)
  def __repr__(i):
    return '<%s %s to %s>' % (i.txt, i.lo, i.hi)

class OneOf(Var):
  def __init__(i,txt,lst):
    super().__init__(txt)
    i.d    = {n:x      for n,x in enumerate(lst) if x}
    i.show = {i.d[x]:x for x   in i.d}
  def xplain(i,x):
    return i.show[x]
  def any1(i):
    return i.d[ random.choice(list(i.d.keys())) ]
  def __repr__(i):
    return '<%s %s>' % (i.txt, list(i.d.keys()))

class Cache():
  def __init__(i, fun): 
    i.kept, i.fun = None,fun
  def __call__(i):  
    i.kept = i.kept if i.kept is not None else X(i.fun)
    return i.kept

tunings()
random.seed(1)
for _ in range(0,20):
  #Var.all.acap.reset()
  print([Var.all.acap.xplain(Var.all.acap()) for _ in range(0,10)])

