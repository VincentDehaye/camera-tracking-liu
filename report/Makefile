name :=report
all: $(name).pdf
$(name).pdf: $(name).tex $(name).bib
	mkdir -p build
	pdflatex -output-directory build/ $(name)
	biber build/$(name)
	pdflatex -output-directory build/ $(name)
	pdflatex -output-directory build/ $(name)
	mv build/$(name).pdf .
clean:
	rm -rf build
distclean: clean
	rm -f $(name).pdf
.PHONY: all clean
