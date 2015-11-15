NOSEOPTS := --quiet --processes 2 --process-timeout 30 --with-randomly libgiza

nosetests:
	-rm -f .coverage
	@echo "[testing] running nosetests"
ifeq ($(shell test -f /etc/arch-release && echo arch || echo Linux),arch)
	nosetests3  $(NOSEOPTS)
	nosetests2  $(NOSEOPTS)
else
	nosetests $(NOSEOPTS)
endif

pyflakes:
	@echo "[testing] running pyflakes:"
	pyflakes libgiza

pep8:
	@echo "[testing] running pep8: "
	pep8 --max-line-length=100 libgiza

test: nosetests pyflakes pep8
	@echo "[testing]: completed all tests"
