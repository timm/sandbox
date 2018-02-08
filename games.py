"""
Warning: code written not run
"""

"""
HighDram classes
"""
class Drama(Exception): pass
class FireAlarm(Drama): pass
class Win(Drama): pass

# -----------------------------------------------------
"""
Not you again
"""
def kv(d):
  return '(' + ', '.join(['%s: %s' % (k, d[k])  
                          for k in sorted(d.keys()) if k[0] != "_"]) + ')'

class Thing(object):
  def __repr__(i) : return i.__class__.__name__ + kv(i.__dict__)

class o(Thing):
  def __init__(i, **dic) : i.__dict__.update(dic)
  def __getitem__(i, x)  : return i.__dict__[x]

# -----------------------------------------------------
class Machine(Thing): pass
class Guess(Machine): pass
class MyGame(Machine):
  def __init__(i, nplayers):
    """
    Your knowledge of other players is a set of "guess" machines
    """
    i.machines = [Guess(j) for j in range(nplayers - 1)]  # not you
    i.start = something
  # ------------------------
  """
  No central controller
  """
  def run(i):
    payload = o(whatever)
    try:
      state = i.start
      while state:
        state = state.step(payload)
    except Drama as event : #can check for super class? https://goo.gl/H3jz7x
      1 # handle event
    finally: # always runs, exception of no
      return payload

"""
Belifs desires intentions https://goo.gl/PJygJy
Welcome to high church AI
"""
class State:
  def __init__(i,name,machine):
    i.name, i.machine = name,machine
    i.beliefs=[] # working memory of things you ahve worked out
                 # if simple symbols, insert here. if complex structure, 
                 # make it a state and go to that state
    i.intentions=[] # short term stuff. queries and operations on this state
    i.desires=[]    # longer terms stuff. when  
  """
  Make intentions a list of gaurds which, if satisfied, return a list
  of actions (messages to this state)
  Make desires a a list of messages to send to the next state, so
  some meory can pass from here to there
  """
  def step(i,payload):
    "match, select, act"
    todo = i.match(payload)
    if todo:
      command = i.select(todo)
      return i.act([payload, command)
    return i

  def match(i,payload):
    out=[]
    for j in i.intentions: #?? replace shuffle with priority?
      todo,there =  j.gaurd(i,payload):
      if todo:
        out += [(j.__name__,todo,there)]
    return out

  def select(i, candidates):
    return random.choice(matched)

  def act(i, payload, (what,actions, there)):
    print("now",what)
    [action(payload) for action in actions]
    i.onExit()
    there.onEntry()
    for desire in i.desires:
      desire(there,payload)  # infect next state with my desires
    return there

  def exampleGaurd(i,payload):
    "dance in place"
    if payload.happy:
      return [i.machine.grin, i.machine.dance], i

  def exampleDesire(i,there,payload):
    there.beliefs += [payload.optimism]
