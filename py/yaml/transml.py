import yaml,re

class act:
  rules = []
  @staticmethod
  def when(s):
    def worker(fun):
      act.rules += [(s,fun)]
      return fun
    return worker

  @staticmethod
  def word(x):
    try: return int(x)
    except:
       try: return float(x)
       except: return x

  @staticmethod
  def asLambda( z ,context):
    if isinstance(z,str):
      for pat,fun in act.rules:
        m = re.match(pat,z)
        if m:
          return lambda: fun(context, *[act.word(x)
                                for x in m.groups()])
    else:
      return z

  @staticmethod
  def prep(d,context=None):
    context = context or []
    return o(**{k:act.prep(v,context+[k]) 
                          if   isinstance(v,dict)
                          else act.asLambda(v,context+[k])
            for k,v in d.items()})

when=act.when

class o:
  def __init__(i,**k): i.__dict__.update(**k)
  def __repr__(i): return '{' + str(i.__dict__) + '}'

@when('from the (.+) try (.+)')
def start(context,where,repeats):
  print("!!!! ",context)
  print('starting at ',where,'for',repeats)

@when('hi (.+)')
def hi(_,x):
  print("hello",x)

@when('jump (.+) to (.+)')
def jump(_,here,there):
  print("jumping from",here,"to",there)

#-------------------------------
spec = """
  start: from the street try 3
  repeat:
    n: 5
    say: hi timm
    action: jump here to there
"""

x = act.prep( yaml.load(spec) )
print(x)

#-------------------------------

class Machine:
  def __init__(i,txt):
    i.txt = txt
    i.all = {}

class State:
  last = None
  @staticmethod
  def __init__(i, machine, txt):
    last = i.machine = machine
    if not txt in i.machine.all:
      i.txt = txt
      i.machine.all[ txt ] = i
      i.out = []
  def trans(i,gaurd,j): i.out += [(gaurd,j)]

@when('if (.+)* when (.+)* go (.+)*')
def transition(here, gaurd, there):
  here  = State.exists(here)
  there = State.exists(there)

  


machine = """
states:
  start : lets get going
  end   : end of the road
changes:
  if start when happy go smile
  if start when sad   go frown
    
"""

print(act.prep( yaml.load( machine ) ))
