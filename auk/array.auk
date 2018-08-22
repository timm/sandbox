# vim: ft=awk:ts=2 sw=2 sts=2 expandtab:cindent:formatoptions+=cro 

function array(i) { split("",i,"") }

function has0(a,k) { a[k][SUBSEP]; split("",a[k],"") }

function has(a,k,fun)     { has0(a,k); if (fun) @fun(a[k])     }
function haS(a,k,fun,x)   { has0(a,k); if (fun) @fun(a[k],x)   }
function hAS(a,k,fun,x,y) { has0(a,k); if (fun) @fun(a[k],x,y) }

function slots(i,s,   k,a) { 
  array(i)
  split(s,a," ");
  for(k in a) has0(i,a[k])
}
