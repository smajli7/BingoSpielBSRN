GV = gv
LATEX = latex
PDFLATEX = pdflatex
DVIPS = dvips -Ppdf 
PSPDF = ps2pdf -dCompatibilityLevel=1.4 -dOptimize=true -dUseFlateCompression=true 
BIBTEX = bibtex
XDVI = xdvi
THUMBPDF = thumbpdf --modes=ps2pdf
PDLIN = pdlin -user passwort -perm acsp
CMD=TEXINPUTS="./llncs:"
ACROBAT = acroread
DATEINAME = BSRN_Paper_Vorlage

all:
	${CMD} $(PDFLATEX) $(DATEINAME).tex

clean:
	rm *.snm *.vrb *.nav *.log *.toc *.tpm *.dvi *.aux *.out *~


