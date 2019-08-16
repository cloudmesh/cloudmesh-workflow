UNAME := $(shell uname)

BROWSER=firefox
ifeq ($(UNAME), Darwin)
BROWSER=open
endif
ifeq ($(UNAME), Windows)
BROWSER=/cygdrive/c/Program\ Files\ \(x86\)/Google/Chrome/Application/chrome.exe
endif
ifeq ($(UNAME), CYGWIN_NT-6.3)
BROWSER=/cygdrive/c/Program\ Files\ \(x86\)/Google/Chrome/Application/chrome.exe
endif

doc: 
	cd docs; make html

publish:
	ghp-import -n -p docs/build/html

view:
	$(BROWSER) docs/build/html/index.html

######################################################################
# CLEANING
######################################################################

clean:
	rm -rf *.egg-info *.eggs
	rm -rf docs/build
	rm -rf build
	rm -rf dist
