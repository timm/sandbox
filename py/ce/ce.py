# /* vim: set tabstop=2 softtabstop=2 shiftwidth=2 expandtab : */
import random

r=random.random
def rseed(s=1): random.seed(s)

class o(object):
  def __repr__(i):
    return i.__class__.__name__ + kv(i.__dict__)
  def __init__(i, **l): i.__dict__.update(l)

def within(min,max,inc=1):
  while min<=max:
    yield min
    min += inc

THE=o(round = 3, 
      private="_",
      r=5,
      m=3,
      n=6,
      b=0.2,
      x= dict(abe = dict(k       = within(1,6),
                         bins    = within(2,10),
                         outlier = ["none","odd"],
                         sample  = ["median","mean","tri5","tri7"]),
              tree = dict(c      = within(0,0.5,0,1),
                          

)

def kv(d):
  "Print dicts, keys sorted (ignoring 'private' keys)"
  _private = lambda key: key[0] == THE.private
  pretty   = lambda x: round(x,THE.round) if isa(x,float) else x
  return '('+', '.join(['%s: %s' % (k,pretty(d[k]))
          for k in sorted(d.keys())
          if not _private(k)]) + ')'

def candidates(n=1000):

