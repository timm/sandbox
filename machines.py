# vim: set filetype=python ts=2 sw=2 sts=2 expandtab: 
import re,traceback,time,random

def rseed(seed=1):
  random.seed(seed)

def shuffle(lst):
  random.shuffle(lst)
  return lst

def about(f):
  print("\n-----| %s |-----------------" % f.__name__)
  if f.__doc__:
    print("# "+ re.sub(r'\n[ \t]*',"\n# ",f.__doc__))

TRY=FAIL=0
def ok(f=None):
  global TRY,FAIL
  if f:
    try:    TRY  += 1; about(f); f(); print("# pass"); 
    except: FAIL += 1; print(traceback.format_exc());
    return f
  else:
    print("\n# %s TRY= %s ,FAIL= %s ,%%PASS= %s"  % (
      time.strftime("%d/%m/%Y, %H:%M:%S,"),
      TRY, FAIL, 
      int(round((TRY - FAIL)*100/(TRY+0.001)))))

def contains(all,some): 
  return all.find(some) != -1

def kv(d):
  """Return a string of the dictionary,
     keys in sorted order,
     hiding any key that starts with '_'"""
  return '(' + ', '.join(['%s: %s' % (k, d[k])
                          for k in sorted(d.keys())
                          if k[0] != "_"]) + ')'

def isa(k, seen = None):
  assert isinstance(k, type),"superclass must be 'object'"
  seen = seen or set()
  if k  not in seen:
    seen.add(k)
    yield k
    for sub in k.__subclasses__():
      for x in isa(sub, seen):
        yield x

class Thing(object):
  def __repr__(i) : 
    return i.__class__.__name__ + kv(i.__dict__)

class Struct(Thing):
  def __init__(i, **dic) : i.__dict__.update(dic)
  def __getitem__(i, x)  : return i.__dict__[x]

#########################################################
#<BEGIN>

class Trans(Thing):
  def __init__(i,here,gaurd,there):
    i.here  = here
    i.there = there
    i.gaurd = gaurd
  def maybe(i) : return random.random() < 0.5

class Ocean(Trans):
  def whales(i)   : return random.random() < 0.1
  def atlantis(i) : return random.random() < 0.01

class State(Thing) : 
  tag = ""
  def __init__(i, name):
    i.name   = txt
    i._trans = []
  def step(i):
    for j in shuffle(i._trans):
      if j.gaurd(i):
        i.onExit()
        j.there.onEntry()
        return j.there
    return i
  def onEntry(i):
    print("arriving at %s" % txt)
  def onExit(i):
    print("leaning  %s" % txt)

class Happy(State) : tag = ":-)"
class Sad(State)   : tag = ":-("
class Exit(State)  : tag = "."

# need a global stop

class Machine(Thing):
  """Maintains a set of named states. 
     Creates new states if its a new name.
     Returns old states if its an old name."""
  def __init__(i, name, most=1000):
    i.seen  = {}
    i.name  = name
    i.start = None
    i.most  = hi
  def isa(i,txt): 
    for k in isa(State):
      if k.tag and contains(txt,k.tag): 
        return k(txt)
    return State(txt)
  def __add__(i,x): return i.state(x)
  def state(i,x):
    i.seen[x] = y = i.seen[x] if x in i.seen else i.isa(x) 
    i.first  = i.first or y
    i.latest = y
    return y
  def trans(i,trans):
    trans.here._trans + [trans]
  def run(i,state):
    for _ in range(i.most):
      state = state.next()
    return state
  def onEntry(i): 
    print("booting %s" % i.name)
    i.start.onEntry()
    return i.run( i.start )
  def onExit(i) : 
    print("shutting down %s" % i.name)

#END>
####################################
@ok
def sym1():
  rseed()
  m = Machine("main")
  s = m.s
  s("cheery:-)")
  s("crying:-(")
  s=Ocean(s(

if __name__== "__main__":
  ok()

