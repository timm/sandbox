-- vim: tabstop=2:softtabstop=2:shiftwidth=2:expandtab
--------- --------- --------- --------- --------- --------- 

function rogues(    ignore,match)
  ignore = {
           jit=true, math=true, package=true, table=true, 
	   coroutine=true, bit=true, os=true, io=true, 
	   bit32=true, string=true,
           arg=true, debug=true, _VERSION=true, _G=true }
  for k,v in pairs( _G ) do
    if type(v) ~= "function" and not ignore[k] then
       assert(match(k,"^[A-Z]"),"rogue local ["..k.."]") end end
end

function ok(t,  n)
  rogues()
  for x,f in pairs(t) do
    print("-- Checking ".. x .."... ")
    the.ok.tries = the.ok.tries + 1
    local passed,err = pcall(f)
    if not passed then
      the.ok.fails = the.ok.fails + 1
      print("-- E> Failure: " .. err)
      n = 1-((the.ok.tries-the.ok.fails)/the.ok.fails)
      print("-- Failures: ".. 100*n  .. "%") end end
end

h
