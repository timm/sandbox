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

def subsets(lst):
  if lst is None: return None
  subsets = [[]]
  lst1 = []
  for n in lst:
    for s in subsets:
      lst1.append(s + [n])
    subsets += lst1
    lst1 = []
  return subsets

print(len(subsets([1,2,3,4,5,6,7])))
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

def data(src, rules={"$": float,"<":float,">":float}): 
  "Coerce strings to things using rules seen on line 1"
  changes = None
  def change1(x,f): return x if x[0]=="?" else f(x) 
  for row in src:
    if changes: 
      row = [ change1(x,f) for x,f in zip(row, changes)  ]
    else:       
      changes= [ rules.get(x[0],lambda z:z) for x in row ] 
    yield row

def xy(src, rules=['<','>']):
  decs, objs = None, None
  for row in src:
    decs = decs or [n for n,x in enumerate(row) if not x[0] in rules]
    objs = objs or [n for n,x in enumerate(row) if     x[0] in rules]
    yield [row[n] for n in decs] , [row[n] for n in objs]

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
  opts = 'hC%s' % ''.join(['%s%s' % (k[0],mark(k)) for k in keys])
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
  def oneLine():
    print(about["why"],"\n",'(c) ',about["when"],", ",about["who"],sep="")
  def usage():
    oneLine()
    print('\nUSAGE: ' , 
          about["how"]," -",''.join([s for s in opts if s != ':']),
          sep="", end="\n\n")
    for k in keys: 
      print("  -%s\t%-10s\t%s    (default=%s)" % (
             k[0],k,about["what"][k]["why"],d[k]))
    oops("  -hC\t%-10s\tshow help" % '' , 0)
  def copyrite():
     oneLine()
     oops(about["copyright"],0)
  #-------------------------------------------------------
  try:
    com, args = getopt.getopt(argv,opts)
    for opt, arg in com:
      if opt == '-h': usage()
      elif opt == '-C': copyrite()
      else:
        for k in keys:
          if opt[1]==k[0]:
            try: d[k] = one(d,about["what"][k], opt,arg)
            except Exception as err: oops(err)
  except getopt.GetoptError as err: oops(err)
  return d


from colorama import Fore, Style
from contextlib import contextmanager

class Highlight:
  def __init__(self, clazz, color):
    self.color = color
    self.clazz = clazz
  def __enter__(self):
    print(self.color, end="")
  def __exit__(self, type, value, traceback):
    if self.clazz == Fore:
      print(Fore.RESET, end="")
    else:
      assert self.clazz == Style
      print(Style.RESET_ALL, end="")
    sys.stdout.flush()

def plain(s):
  print(s,end="")
def red(s):
  with Highlight(Fore, Fore.RED): print(s,end="")

