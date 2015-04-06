
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

ready: gitting files

files: .gitignore

.gitignore :
	@echo ".DS_Store" > $@
	@echo ".pyc" >> $@
	@git add $@

view: $X.md
	pandoc -s -f markdown -t man $X.md > /tmp/$X.man
	man   /tmp/$X.man







