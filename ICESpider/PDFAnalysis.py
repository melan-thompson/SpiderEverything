from PyPDF2 import PdfFileReader, PdfFileWriter

class pdfAnalysis:
    def __init__(self,filename):
        self.pdf= PdfFileReader(open(filename, 'rb'))
        print("this pdf has {} pages".format(self.pdf.getNumPages()))
        print(self.pdf.documentInfo)


if __name__=="__main__":
    pdf=pdfAnalysis("Characterising the Digital Twin  A systematic literature review.pdf")