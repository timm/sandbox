-- vim: ts=2 sw=2 sts=2 expandtab:cindent:formatoptions+=cro 
--------- --------- --------- --------- --------- --------- 

require "lib"
require "ok"

ok {fails = function() assert(1==2) end }
ok {passes = function() assert(1==1) end }

ok { random = function(    a,b)
                rseed(1)
                a= rand()
                rseed(1)
                b=rand()
                assert(a==b) end }

ok { ordered = function(    t)
        t={zz=1,cc=2,aa=1}
        for k,v in ordered(t) do print(k,v) end
        for k,_ in ordered(t) do
          return assert(k=="aa") end end }

ok { splits = function(   t)
          t= split("abcdab","a")
          assert("bcd" == t[1])
          assert("b" == t[2])
          end }

o{a=1,b={k={ll=234,m={}},d=44},c=3}

ok {csv = function (    d) 
    d=rows("data/weather.csv") 
    assert(#d._use == 4)
    assert(d.nums[2].lo == 64)  end }

for i=1,30 do
  io.write(another(4,{"a","b","c","d"}))
end
