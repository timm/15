typo: ready
	- git status
	- rm -f *.pyc
	- git commit -am "stuff"
	- git push origin master

commit: ready
	- git status
	- rm -f *.pyc
	- git commit -a
	- git push origin master

update:
	- git pull origin master

status:
	- git status

gitting:
	git config --global credential.helper cache
	git config credential.helper 'cache --timeout=3600'

timm:
	git config --global user.name "Tim Menzies"
	git config --global user.email tim.menzies@gmail.com
	
your:
	git config --global user.name "Your name"
	git config --global user.email your@email.address

install: ready
	sudo pip install matplotlib
	sudo pip install -U scikit-learn

ready: gitting files

files: .gitignore

.gitignore :
	@echo ".DS_Store" > $@
	@echo ".pyc" >> $@
	@git add $@

ok:
	@rm -rf okok.py;  
	@python unittestok.py;
	@ls *ok.py | grep -v unittest | sed 's/\.py//' |  \
	gawk '  \
	BEGIN {print "from unittest import *"} \
	      {print "import " $$1} \
	END   {print "print \"\\nTest suite results... TRIES:\",unittest.tries,\"FAILS:\",unittest.fails"}\
	' > okok.py
	@python okok.py
	@rm -rf okok.py 







