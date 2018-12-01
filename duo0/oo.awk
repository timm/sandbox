# vim: filetype=awk: ts=2 sw=2 sts=2 expandtab:cindent:formatoptions+=cro 
function new(i) { split("",i,"") } # empty array

function Object(i)  { new(i); i._id = ++_ID } # empty array with unique id

function has(i,x,f) {  # has-a creation with 0/1 arguments
  i[x][SUBSEP]         # create one-level deeper that what we want
  new(i[x])            # zap extra level, leaving an  empty array
  if (f) @f(i[x])      # maybe fill that empty array
}
# has-a creation with 1 to 5 arguments
function have(i,x,f,a)         { has(i,x); @f(i[x],a) }
function havE(i,x,f,a,b)       { has(i,x); @f(i[x],a,b) }
function haVE(i,x,f,a,b,c)     { has(i,x); @f(i[x],a,b,c) }
function hAVE(i,x,f,a,b,c,d)   { has(i,x); @f(i[x],a,b,c,d) }
function HAVE(i,x,f,a,b,c,d,e) { has(i,x); @f(i[x],a,b,c,d,e) }
