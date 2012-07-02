develop:
	@if [ ! -f lib/buildout/bootstrap.py ]; then \
	    mkdir -p lib/buildout; \
	    wget http://svn.zope.org/*checkout*/zc.buildout/tags/1.5.2/bootstrap/bootstrap.py?content-type=text%2Fplain -O lib/buildout/bootstrap.py; \
	    python lib/buildout/bootstrap.py --distribute; \
	fi
	bin/buildout -N

update: develop

uninstall:
	rm -rf bin/ lib/ *.egg-info

tests:
	bin/nosetests -v --rednose --with-doctest --with-coverage --cover-erase --cover-package=debisogen debisogen/

readme:
	mkdir -p docs/_build/html
	bin/rst2 html README.rst > docs/_build/html/README.html
