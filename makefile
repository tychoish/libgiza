NOSEOPTS := --processes 4 --with-coverage --cover-inclusive --cover-package libgiza

nosetests:
	-rm -f .coverage
	@echo "[testing] running nosetests"
	nosetests $(NOSEOPTS)
ifeq ($(shell test -f /etc/arch-release && echo arch || echo Linux),arch)
	nosetests2 $(NOSEOPTS)
endif

pyflakes:
	@echo "[testing] running pyflakes:"
	pyflakes libgiza

pep8:
	@echo "[testing] running pep8: "
	pep8 --max-line-length=100 libgiza

test: nosetests pyflakes pep8
	@echo "[testing]: completed all tests"
