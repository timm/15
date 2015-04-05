
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

ready: gitting files

files: .gitignore

.gitignore :
	@echo ".DS_Store" > $@
	@echo ".pyc" >> $@
	@git add $@
