V=var
F=$(shell ls *.auk)
G=$(F:.auk=.awk)
H=$V/$(subst .awk ,.awk $V/,$G)
Awk=AWKPATH='$V:$$AWKPATH' gawk -f

ok : files $H

files:
	@[[ ! -f .ignore ]] && echo 'var' > .gitignore
	@mkdir -p $V

$V/%.awk : %.auk
	@echo "# $@"  1>&2
	@gawk '{print gensub(/\.([^0-9])([a-zA-Z0-9_]*)/, "[\"\\1\\2\"]", "g", $$0)}' $< > $@

pull:
	git pull

push:
	git commit -am pushing
	git push

eg0: ok; $(Awk) lib.awk
eg1: ok; @cat data/weather.csv | $(Awk) dom.awk
eg2: ok; @cat data/weatherLong.csv | $(Awk) dom.awk
eg3: ok; @cat data/auto.csv    | $(Awk) dom.awk

Some=cut -d, -f 4,5,8
Fields=head -1 data/auto.csv | $(Some)
eg4: 
	@$(MAKE) eg3 | $(Some)

eg4best:  
	@$(Fields)
	@$(MAKE) eg3 | sort -t, -n -k 3 | tail 

eg4worst:  
	@$(MAKE) eg3 | sort -t, -n -k 3 | head 

eg5: ok 
	@$(MAKE) eg3 | $(Awk) ranges.awk
