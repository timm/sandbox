--vim: ts=2 sw=2 sts=2 expandtab:cindent:formatoptions+=cro 
--------- --------- --------- --------- --------- --------- 

require "num"

function data()
  return {w={}, nums={}, class=nil, rows={}, name={}, _use={}} 
end

function indep(t,c) return not t.w[c] and t.class ~= c end
function dep(t,c)   return not indep(t,c) end

function header(t,cells,     c,w)
  for c0,x in pairs(cells) do
    if not x:match("%?")  then
      c = #t._use+1
      t._use[c] = c0
      t.name[c] = x
      if x:match("[<>%$]") then t.nums[c] = num() end 
      if x:match("<")      then t.w[c]  = -1 end
      if x:match(">")      then t.w[c]  =  1 end 
      if x:match("!")      then t.class =  c end end end
end

function row(t,r,cells,     x)
  t.rows[r] = {}
  for c,c0 in pairs(t._use) do
    x = cells[c0]
    if t.nums[c] then 
      if x ~= "?" then
	x = tonumber(x)
        ninc(t.nums[c], x) end end
    t.rows[r][c] = x  end
end  

function rows1(stream, t,f0,f,   r,line,cells)
  r,line = -1,io.read()
  while line do
    line:gsub("([\t\r ]*|#.*)","")
    cells = split(line)
    line = io.read()
    if #cells > 0 then
      r = r + 1
      if r==0 then f0(t,cells) else f(t,r,cells) end end
  end 
  io.close(stream)
  return t
end

function rows(file,t,f0,f,      stream,txt,cells,r,line)
  return rows1( file and io.input(file) or io.input(),
                t  or data(), f0 or header, f or row) end 

