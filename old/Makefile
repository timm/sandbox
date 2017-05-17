Files=where.md

all:: $(Files) commit

commit:
	svn commit -m sff

%.md : %.py
	@echo $<
	 @gawk 'gsub(/^"""/,"") { Out = 1 - Out; next }  \
               {print  (Out ? "" : "     ") $$0} ' $< > $@
