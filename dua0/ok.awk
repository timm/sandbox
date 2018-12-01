function tests(what, all,   one,a,i,n) {
  n = split(all,a,",")
  print("n " n)
  print " "
  print "#--- " what " -----------------------"
  for(i=1;i<=n;i++) {
    one = a[i]
    @one(one) }
  rogues()
}

function is(f,got,want,    pre) {
  if (want == "") want=1
  if (want == got)
   pre="#TEST:\tPASSED"
  else
   pre="#TEST:\tFAILED"
  print( pre "\t" f "\t" want "\t" got )
}

function rogues(    s) {
  for(s in SYMTAB)
   if (s ~ /^[A-Z][a-z]/) print "Global " s
  for(s in SYMTAB)
   if (s ~ /^[_a-z]/) print "Rogue: " s
}
