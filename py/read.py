import re,traceback

class O:
  y=n=0
  @staticmethod
  def report():
    print("\n# pass= %s fail= %s %%pass = %s%%"  % (
          O.y,O.n, int(round(O.y*100/(O.y+O.n+0.001)))))
  @staticmethod
  def k(f):
    try:
      print("\n-----| %s |-----------------------" % f.__name__)
      if f.__doc__:
        print("# "+ re.sub(r'\n[ \t]*',"\n# ",f.__doc__))
      f()
      print("# pass")
      O.y += 1
    except:
      O.n += 1
      print(traceback.format_exc()) 
    return f

@O.k
def testingFailure():
  """this one must fail.. just to
  test if the  unit test system is working"""
  assert 1==2

@O.k
def testingSuccess():
  """if this one fails, we have a problem!"""
  assert 1==1

DATA1 = """
outlook,$temp,?humidity,windy,play
sunny,85,85,FALSE,no
sunny,80,90,TRUE,no
overcast,83,86,FALSE,yes
rainy,70,96,FALSE,yes
rainy,68,80,FALSE,yes
rainy,65,70,TRUE,no
overcast,64,65,TRUE,yes
sunny,72,95,FALSE,no
sunny,69,70,FALSE,yes
rainy,75,80,FALSE,yes
sunny,75,70,TRUE,yes
overcast,100,25,90,TRUE,yes
overcast,81,75,FALSE,yes
rainy,71,91,TRUE,no"""


DATA2 = """
    outlook,   # weather forecast.
    $temp,     # degrees farenheit
    ?humidity, # relative humidity
    windy,     # wind is high
    play       # yes,no
    sunny,85,85,FALSE,no
    sunny,80,90,TRUE,no
    overcast,83,86,FALSE,yes
    rainy,70,96,FALSE,yes
    rainy,68,80,FALSE,yes
    rainy,65,70,TRUE,no
    overcast,64,
       
                  65,TRUE,yes
    sunny,72,95,FALSE,no
    sunny,69,70,FALSE,yes
    rainy,75,80,FALSE,yes
          sunny,
                75,70,TRUE,yes
    overcast,100,25,90,TRUE,yes
    overcast,81,75,FALSE,yes # unique day
    rainy,71,91,TRUE,no"""



def lines(s):
   "Return contents, one line at a time."
   if s[-3:] in ["csv","dat"]:
     with open(s) as fs:
       for line in fs: 
         yield line
   else:
     for line in s.splitlines():
       yield line

def rows(src):
   """Kill bad characters. If line ends in ',' 
    then join to next. Skip blank lines."""
   cache = []
   for line in src:
     line = re.sub(r'([ \n\r\t]|#.*)', "", line)
     cache += [line]
     if len(line)> 0:
       if line[-1] != ",":
         line = ''.join(cache)
         cache=[]
         yield line


def cols(src,   uses=None):
   """ If a column name on row1 contains '?', 
   then skip over that column."""
   for row in src:
     cells = row.split(",")
     uses  = uses or [False if "?" in s[0] else True for s in cells]
     out   = [cells[pos] for pos,use  in enumerate(uses) if use]
     yield out


def prep(src,   nums=None):
   """ If a column name on row1 contains '$', 
   coerce strings in that column to a float."""
   for xs in src:
     if nums:
       xs= [(float(x) if num else x) for x,num in zip(xs,nums)]
     else:
       nums = ["$" in x[0] for x in xs]
     yield xs


def ok0(s):
  for row in prep(cols(rows(lines(s)))):
    print(row)

@O.k
def ok1(): ok0(DATA1)

@O.k
def ok2(): ok0(DATA2)

if __name__== "__main__":
  O.report()
