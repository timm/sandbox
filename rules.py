class rule:
  def __init__(i):
    i._when, i._then = [],[]
  def when(i,j) : i._when = j; return i
  def then(i,j) : i._then = j; return i
  def triggered(i):
    return i._when()

def the(i):
  return rule()

def when(*lst):
  return [lambda : x for x in lst]

def all(*lst):
  def tmp(): 
    for one in lst:
      if not one: return False
    return True
  return tmp

t=True
f=False
r=the('aa').when(all(t,t,t)).then(t)
print(r.triggered())



