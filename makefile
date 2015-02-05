
nosetests: 
	@echo "[testing] running nosetests"
	nosetests

pyflakes:
	@echo "[testing] running pyflakes:"	
	pyflakes libgiza

pep8:
	@echo "[testing] running pep8: "	
	pep8 --max-line-length=100 libgiza

test: nosetests pyflakes pep8
	@echo "[testing]: completed all tests"
