-- vim: ts=2 sw=2 sts=2 expandtab:cindent:formatoptions+=cro 
--------- --------- --------- --------- --------- --------- 

package.path = '../src/?.lua;' .. package.path 
require "lib"
require "ok"
require "rows"

o(names2data({'outlook', '$temp', '<humid', 'wind', '!play'}))

o(rows("../data/weatherLong.csv"))
rogues()

