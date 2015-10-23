NOSEOPTS := --quiet --with-randomly --with-coverage --cover-inclusive --cover-package libgiza

nosetests:
	-rm -f .coverage
	@echo "[testing] running nosetests"
ifeq ($(shell test -f /etc/arch-release && echo arch || echo Linux),arch)
	nosetests2 $(NOSEOPTS)
endif
	nosetests $(NOSEOPTS)

pyflakes:
	@echo "[testing] running pyflakes:"
	pyflakes libgiza

pep8:
	@echo "[testing] running pep8: "
	pep8 --max-line-length=100 libgiza

test: nosetests pyflakes pep8
	@echo "[testing]: completed all tests"
