
function data()
  return {w={}, lo={}, hi={}, rows={}, name={}, _use={}} 
end

function header(t,cells)
  for c0,x in pairs(cells) do
    if not x:match("%?")  then
      c = #t._use+1
      t._use[c] = c0
      t.name[c] = x
      if x:match("[<>%$]") then
        t.lo[c] = 10^32
        t.hi[c] = -10^32
        if x:match("<") then t.w[c] =  1 end
        if x:match(">") then t.w[c] = -1 end  end end end
end

function row(t,r,cells)
  t.rows[ r ] = {}
  for c,c0 in pairs(t._use) do
    x = cells[c0]
    if x ~= "?" and t.hi[c] then 
      x = tonumber(x)
      if x > t.hi[c] then t.hi[c] = x end
      if x < t.lo[c] then t.lo[c] = x end 
    end  
    t.rows[r][c] = x 
  end 
end  

function rows(file, t,f0,f,      stream,txt,cells,r)
  t  = t  or data()
  f0 = f0 or header
  f  = f  or row
  stream = file and io.input(file) or io.input()
  r,line = -1,io.read()
  while line do
    line = line:gsub("[\t\r ]*","") -- no spaces
                :gsub("#.*","") -- no comments
    if #line > 0 then
      r = r + 1
      cells = split(line)
      if r==0 then f0(t,cells) else f(t,r,cells) end 
    end
    line = io.read() 
  end
  io.close(stream)
  return t
end 


