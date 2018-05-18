#---------------------------------------------
import getopt,sys,re,math,time,os
from random import random as r, choice as any, seed as seed

DECIMALS=3

#------------------------------------
def demo(f=None, act=None, all=[]):
  if     f: all += [f]
  elif act:
    for one in all:
      if one.__name__ == act: return one()
    print("unknown %s"% act)
  else: [f() for f in all]
  return f

def sym(x): return x
def same(x): return x
def first(l): return l[0]
def second(l): return l[1]
def last(l): return l[-1]

def kv(d,keys=None):
   "print dictionary, in key sort order"
   keys = keys or sorted(list(d.keys()))
   pretty = lambda x: round(x,DECIMALS) if isinstance(x,float) else x
   return '{'+', '.join(['%s: %s' % (k, pretty(d[k]))for k in keys])+'}'

def timeit(f):
  t1=time.perf_counter()
  f()
  return time.perf_counter() - t1

#----------------------------------------------
def rows(file, doomed=r'([\n\r\t]|#.*)', sep=",", skip="?"):
  "World's smallest csv reader?"
  use=None
  with open(file) as fs:
    for n,line in enumerate(fs):
      line = re.sub(doomed, "", line)
      cells = [z.strip() for z in line.split(sep)]
      if len(cells) > 0:
        use = use or [n for n,x in enumerate(cells) if x[0] != skip]
        assert len(cells) == len(use),'row %s has not %s cells' % (n,len(use))
        yield [cells[n] for n in use]

def data(rows, rules={"$": float,"<":float,">":float}): 
  "Coerce strings to things using rules seen on line 1"
  changes = None
  def change1(x,f): return x if x[0]=="?" else f(x) 
  for row in rows:
    if changes:
      row  = [ change1(x,f) for x,f in zip(row, changes)  ]
    else:
      changes = [ rules.get(x[0],lambda z:z) for x in row ] 
    yield row
 
#----------------------------------------------
class o(object):
  "Javascript envy. Now 'o' is like a JS object."
  def __init__(i, **kv):    i.__dict__.update(kv)
  def __setitem__(i, k, v): i.__dict__[k] = v
  def __getitem__(i, k):    return i.__dict__[k]
  def keys(i):              return i.__dict__.keys()
  def __repr__(i):          return i.__class__.__name__ + kv(i.__dict__, i._has())
  def __len__(i):           return len(i.__dict__)
  def _has(i):              return [k for k in sorted(i.__dict__.keys()) if k[0] != "_"]

#----------------------------------------------
def the(b4):
  now = o()
  options = lambda x: x if isinstance(x, list) else [x]
  for k in b4["what"].keys(): 
    now[k]= options( b4["what"][k]["what"] )[0]
  return now

#----------------------------------------------
def main(about, argv=None):
  "Configure command line parser from keys of dictonary 'd'"
  d = the(about)
  argv = argv or sys.argv[1:]
  keys = sorted([k for k in about["what"].keys()])
  mark = lambda k: "" if isinstance(d[k],bool) else ":"
  opts = 'h%s' % ''.join(['%s%s' % (k[0],mark(k)) for k in keys])
  oops = lambda x,y=2: print(x) or sys.exit(y)
  #-------------------------------------------------------
  def one(d,slot,opt,arg):
    what = slot["what"]
    if isinstance(what,bool):
      return not what
    want = slot["want"]
    arg  = (slot.get("make",want))(arg)
    if not want(arg):
       oops("%s: %s is not %s" % (opt,arg,want.__name__))
    if isinstance(what,list):
      if arg not in what:
        oops("%s: %s is not one of %s" % (opt, arg, what))
    return arg
  #-------------------------------------------------------
  def usage():
    print(about["why"],"\n",'(c) ',about["when"],", ",about["who"],sep="")
    print('\nUSAGE: ' , 
          about["how"]," -",''.join([s for s in opts if s != ':']),
          sep="", end="\n\n")
    for k in keys: 
      print("  -%s\t%-10s\t%s    (default=%s)" % (
             k[0],k,about["what"][k]["why"],d[k]))
    oops("  -h\t%-10s\tshow help" % '' , 0)
  #-------------------------------------------------------
  try:
    com, args = getopt.getopt(argv,opts)
    for opt, arg in com:
      if opt == '-h': usage()
      else:
        for k in keys:
          if opt[1]==k[0]:
            try: d[k] = one(d,about["what"][k], opt,arg)
            except Exception as err: oops(err)
  except getopt.GetoptError as err: oops(err)
  return d
