MAIN = daimo-paper-es

# pdflatex is run twice so \ref / \cite references resolve.
all: $(MAIN).pdf

$(MAIN).pdf: $(MAIN).tex
	pdflatex -interaction=nonstopmode $(MAIN).tex
	pdflatex -interaction=nonstopmode $(MAIN).tex

clean:
	rm -f $(MAIN).aux $(MAIN).log $(MAIN).out $(MAIN).toc $(MAIN).bbl $(MAIN).blg

distclean: clean
	rm -f $(MAIN).pdf

.PHONY: all clean distclean
