out    = ../doc#
prefix = https://github.com/timm/15/blob/master#


pys  = $(subst .py,.md,$(shell ls *.py;))#
mds  = $(out)/$(subst .md ,.md $(out)/,$(pys))#
Make = $(MAKE) --no-print-directory #

publish: dirs $(mds)  typo

typo  : ;cd ..; $(Make) typo
commit: ;cd ..; $(Make) commit
update: ;cd ..; $(Make) update
status: ;cd ..; $(Make) status

define p2md
  BEGIN           {  
         q="\""
         print "" 
         print "# " name 
         print ""
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



dirs:
	@ - mkdir -p $(out) etc

etc/p2md.awk  : Makefile
	 @- echo "$$p2md" > $@

$(out)/%.md: %.py etc/header.txt etc/footer.txt etc/p2md.awk
	@echo "making... $<"
	@(cat etc/header.txt; awk -f etc/p2md.awk -v name="$<" $< ; cat etc/footer.txt) | sed 's?_PREFIX?$(prefix)?g' > $@;
	@git add $@
