import random

class ShowError(Exception): pass

def c():
  print("in c")
  raise ShowError('A very specific bad thing happened.')

def b(): 
  if random.random() < 0.5:
    c()
  else:
    1/0

def a():
  try: 
    b()
  except ShowError as e : 
    print("elegant nested termination ", e)
  print("after")
  
a()
