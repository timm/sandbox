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
      i.walk(payload, i.start) 
    except Drama as event: #can check for super class? https://goo.gl/H3jz7x
      # handle event
    finally: # always runs, exception of no
      return payload
  # -----------------------
  def walk(i, payload, state):
    while state:
       state = state.step(payload)

"""
Belifs desires intentions https://goo.gl/PJygJy
Welcome to high church AI
"""
class State:
  def __init__(i,name,machine):
    i.name, i.machine = name,machine
    beliefs=[] # if simple symbols, insert here. if complex structure,
               # make it a state
    intentions=[] # short term stuff. queries and operations on this state
    desires=[]    # longer terms stuff. when  

# make intentions a list of gaurds which, if satisfied, return a list 
# of actions (messages to this state) 
# make desires a a list of messages to send to the next state, so
# some meory can pass from here to there
