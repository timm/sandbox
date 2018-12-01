# vim: filetype=awk: ts=2 sw=2 sts=2 expandtab:cindent:formatoptions+=cro 
function new(a) { split("",a,"") }

function Object(i)  { new(i); i.oid = ++_OID }

function has(x,y,f) { # awk
  x[y][SUBSEP]
  new(x[y])
  if (f) @f(x[y])
}

function have(x,y,f,a)         { has(x,y); @f(x[y],a) }
function havE(x,y,f,a,b)       { has(x,y); @f(x[y],a,b) }
function haVE(x,y,f,a,b,c)     { has(x,y); @f(x[y],a,b,c) }
function hAVE(x,y,f,a,b,c,d)   { has(x,y); @f(x[y],a,b,c,d) }
function HAVE(x,y,f,a,b,c,d,e) { has(x,y); @f(x[y],a,b,c,d,e) }
