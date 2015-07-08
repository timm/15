e=.
f=../src
t=..
files=$(shell cd $f; ls *.html | sed 's?^?$t/?')

all: ${files}

# $(etc)/head.sh $(etc)/tail.sh

../%.html : $f/%.html
	@ echo $@
	@ - bash $e/make.sh "$e" "$<" > $@

install:
	brew install tidy-html5
