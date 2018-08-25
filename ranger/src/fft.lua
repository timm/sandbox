#!/usr/bin/env lua
-- vim: ts=2 sw=2 sts=2 expandtab:cindent:formatoptions+=cro 
--------- --------- --------- --------- --------- ---------~

require "lib"

function fft(t)
  for c,name in pairs(t.name) do
    if indep(t,c) then
      if t.nums[c]

      then print("",name) else print("y",name) end end
end

function mainFft() fft(rows()) end

return {main=mainFft}
