--vim: ts=2 sw=2 sts=2 expandtab:cindent:formatoptions+=cro 
--------- --------- --------- --------- --------- --------- 

require "num"

function data()
  return {w={}, nums={}, rows={}, name={}, _use={}} 
end

function header(t,cells,     c,w)
  for c0,x in pairs(cells) do
    if not x:match("%?")  then
      c = #t._use+1
      t._use[c] = c0
      t.name[c] = x
      if x:match("[<>%$]") then
	w = x:match("<") and 1 or -1
	t.nums[c] = num(w) end end end
end

function row(t,r,cells,     x)
  t.rows[r] = {}
  for c,c0 in pairs(t._use) do
    x = cells[c0]
    t.rows[r][c] = x 
    if t.nums[c] then 
      ninc(t.nums[c], tonumber(x)) end end
end  

function rows(file,t,f0,f,      stream,txt,cells,r,line)
  t  = t  or data()
  f0 = f0 or header
  f  = f  or row
  stream = file and io.input(file) or io.input()
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
