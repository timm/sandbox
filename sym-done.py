# vim: set filetype=python ts=2 sw=2 sts=2 expandtab: 
import re,traceback,time,random

def rseed(seed=1):
  random.seed(seed)

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

#########################################################
#<BEGIN>

def kv(d):
  """Return a string of the dictionary,
     keys in sorted order,
     hiding any key that starts with '_'"""
  return '(' + ', '.join(['%s: %s' % (k, d[k])
                          for k in sorted(d.keys())
                          if k[0] != "_"]) + ')'

class Thing(object):
  def __repr__(i): return kv(i.__dict__)

class Sym(Thing):
  def __init__(i, inits=None):
    i.counts= {}   # track total of things seen so far
    i.most  = 0    # track number of most common thing
    i.mode  = None # track value of most common thing
    i.total = 0    # count of totl things seen so far
    i.adds(inits or []) # if any inits, add them in
  def __imul__(i,x): i.adds(x); return i
  def __iadd(i,x):   i.add(x) ; return i
  def adds(i,lst):  
    "call add for each item in lst"
    [i.add(x) for x in lst]
  def add(i,x):
    """increment total by one
        increat counts of x by one
       if new cost common symbol, update mode,mode"""
    i.total += 1
    new = i.counts[x] = i.counts.get(x,0) + 1
    if new > i.most:
      i.most, i.mode = new,x
  def prob(i,x):
    "return probability of x being in sample"
    return i.counts.get(x,0) / i.total
  def sample(i, enough=500):
    """Iterator.  Yields often seen things most often
     while yielding rarer this more rarely.
      Given a dictionary d{k1=n1, k2=n2, ...},
      return enough keys ki at probability
      pi = ni/total where total = n1+n2+..
      e.g. if we've seen 30 boxes and 20 circles
      and 10 lines, then this code should
      yield
      around twice as many boxes as anything else,
      circles 1/3rd of the time and lines 1/6th of the time.
    """
    n, lst = 0, []
    for x in i.counts:
       n   += i.counts[x]
       lst += [(i.counts[x],x)]
    lst.sort(reverse=True)
    while enough > 0:
      r = random.random()
      for freq,thing in lst:
        r -= freq*1.0/n
        if r <= 0:
          yield thing
          enough -= 1
          break

#<END>
####################################
@ok
def sym1():
  rseed()
  s1 = Sym('programming is fun')
  assert s1.total == 18
  assert s1.mode in 'rgm ' # rgm<space> is the most common symbol
  assert s1.most == 2      # each of rgm<spance> appear twive
  assert s1.prob('g') == 2/18
  # and if we sample from s1...
  s2 = Sym( [x for x in s1.sample(1000)] )
  # ... then we should see more 'm' than 'f'
  assert s2.counts['m'] > s2.counts['f']*1.5

if __name__== "__main__":
  ok()

