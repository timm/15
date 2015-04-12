out  = ..#
pys  = $(subst .py,.md,$(shell ls *.py;))#
mds  = $(out)/$(subst .md ,.md $(out)/,$(pys))#
Make = $(MAKE) --no-print-directory #

typo  : ;cd ..; $(Make) typo
commit: ;cd ..; $(Make) commit
update: ;cd ..; $(Make) update
status: ;cd ..; $(Make) statsus

define p2md
  BEGIN           {  
         print ""
         print "# " name
         First = 1      
         In = 1
  }         
  /^"""</,/^>"""/ {  next } 
  /^"""/          {  In = 1 - In       
                     if (In)            
                       print "````python"
                     else          
                       if (First)   
                         First = 0   
                       else     
                         print "````"  
                     next }       
  ! First { print $$0 }       
  END     { if (In) print "````"  }
endef

export p2md

publish: dirs $(mds)  typo

dirs:
	@ - mkdir -p $(out) etc

etc/p2md.awk  : Makefile
	 @- echo "$$p2md" > $@

$(out)/%.md: %.py etc/header.txt etc/footer.txt etc/p2md.awk
	@echo "making... $<"
	@cat etc/header.txt > $@
	@awk -f etc/p2md.awk -v name="$<" $< >> $@;
	@cat etc/footer.txt >> $@
	@git add $@
