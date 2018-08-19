F=$(shell ls *.auk)

all : $(F:.auk=.awk)

%.awk : %.auk
	gawk '{print gensub(/\.([^0-9])([a-zA-Z0-9_]*)/, "[\"\\1\\2\"]", "g", $$0)}' $< > $@
