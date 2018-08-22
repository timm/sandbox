V=var
D=docs
F=$(shell ls *.auk)
G=$(F:.auk=.awk)
H=$V/$(subst .awk ,.awk $V/,$G)

M=$(F:.auk=.md)
N=$D/$(subst .md ,.md $D/,$M)

Awk=AWKPATH='$V:$$AWKPATH' gawk -f

#####################

define myvar
{ print $$0 1}
endef


ok : files $H $N

files:
	@[[ ! -f .ignore ]] && echo 'var' > .gitignore
	@mkdir -p $V $D

$V/%.awk : %.auk
	@echo "# $@"  1>&2
	@gawk '{print gensub(/\.([^0-9])([a-zA-Z0-9_]*)/, "[\"\\1\\2\"]", "g", $$0)}' $< > $@

$D/%.md : %.auk
	@echo "# $@"  1>&2
	@gawk ' \
	BEGIN {In = 1; Pre=1}                                      \
	gsub(/^"""/,"") {  In =  1 - In ; if (Pre) {Pre=0} else {   \
	      if (In)  { print ""; print "```c " $$0 }  \
	      else { print "```" $$0; print "" } }        \
	    next }                    \
	Pre { next }                   \
	    { sub(/^#/,""); print }     \
	END { if (In) print "```\n" }' $< > $@

pull:
	git pull

push:
	git commit -am pushing
	git push

eg0: ok; $(Awk) lib.awk
eg1: ok; @cat data/weather.csv | $(Awk) dom.awk
eg2: ok; @cat data/weatherLong.csv | $(Awk) dom.awk
eg3: ok; @cat data/auto.csv    | $(Awk) dom.awk
Some=cut -d, -f 4,5,8,9 | sed 's/,/	/g'
Fields=head -1 data/auto.csv | $(Some)
eg4:  ok
	@$(MAKE) eg3 | $(Some)

eg4best:  ok
	@$(Fields)
	@$(MAKE) eg3 | sort -t, -n -k 9 | tail  | $(Some)

eg4worst:  ok
	@$(MAKE) eg3 | sort -t, -n -k 9 | head  | $(Some)

eg5a: ok; @$(MAKE) eg1 | $(Awk) unsup.awk
eg5: ok; @$(MAKE) eg2 | $(Awk) unsup.awk
eg6: ok; @$(MAKE) eg3 | $(Awk) unsup.awk

eg7: ok; @$(MAKE) eg2 | $(Awk) super.awk
eg8: ok; @$(MAKE) eg3 | $(Awk) super.awk


eg9: ok; @$(MAKE) eg7 | $(Awk) sdtree.awk
eg10: ok; @$(MAKE) eg8 | $(Awk) sdtree.awk

eg11: ok;
	echo 11
	$(Awk) csv.awk 
