# from https://github.com/zygmuntz/hyperband/blob/master/hyperband.p

from random import random
from math import log, ceil
from time import time, ctime


def get_params(): return [random()  for _ in range(10)]
def try_params(lst): return sum(lst)

class Hyperband:
  
  def __init__( i, get_params=get_params, try_params=try_params, max_iter=81,eta=3 ):
    i.get_params = get_params
    i.try_params = try_params
    i.max_iter   = max_iter    # maximum iterations per configuration
    i.eta        = eta      # defines configuration downsampling rate (default = 3)A
    i.logeta     = lambda x: log( x ) / log( i.eta )
    i.s_max      = int( i.logeta( i.max_iter ))
    i.B          = ( i.s_max + 1 ) * i.max_iter
    i.results    = []  # list of dicts
    i.counter    = 0
    i.best_loss  = 10**32
    i.best_counter = -1

  # can be called multiple times
  def run( i, skip_last = 0, dry_run = False ):
    for s in reversed( range( i.s_max + 1 )):
      n = int( ceil( i.B / i.max_iter / ( s + 1 ) * i.eta ** s ))  # init configs 
      r = i.max_iter * i.eta ** ( -s )                             # init interations/config
      T = [ i.get_params() for _ in range( n )]                    # T random configs
      print("")
      for j in range(( s + 1 ) - int( skip_last )):  # run nconfigs, keep best nconfig/eta
        n_configs = n * i.eta ** ( -j )
        n_iterations = r * i.eta ** ( j )
        print("    *** {} configurations x {:.1f} iterations each".format( n_configs, n_iterations ))
        val_losses = []
        early_stops = []
#        for t in T:
#          i.counter += 1
#          print "\n{} | {} | lowest loss so far: {:.4f} (run {})\n".format( i.counter, ctime(), i.best_loss, i.best_counter )
#          start_time = time()
#          if dry_run:
#            result = { 'loss': random(), 'log_loss': random(), 'auc': random()}
#          else:
#            result = i.try_params( n_iterations, t )    # <---
#          assert( type( result ) == dict )
#          assert( 'loss' in result )
#          
#          seconds = int( round( time() - start_time ))
#          print "\n{} seconds.".format( seconds )
#          
#          loss = result['loss']  
#          val_losses.append( loss )
#          
#          early_stop = result.get( 'early_stop', False )
#          early_stops.append( early_stop )
#          
#          # keeping track of the best result so far (for display only)
#          # could do it be checking results each time, but hey
#          if loss < i.best_loss:
#            i.best_loss = loss
#            i.best_counter = i.counter
#          
#          result['counter'] = i.counter
#          result['seconds'] = seconds
#          result['params'] = t
#          result['iterations'] = n_iterations
#          
#          i.results.append( result )
#        
#        # select a number of best configurations for the next loop
#        # filter out early stops, if any
#        indices = np.argsort( val_losses )
#        T = [ T[i] for i in indices if not early_stops[i]]
#        T = T[ 0:int( n_configs / i.eta )]
        #print("    best", n/i.eta)

#     return i.results


Hyperband().run()

