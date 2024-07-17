import PyPDF2
import sys

def pdf_to_text(pdf_path, txt_path):
    with open(pdf_path, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        with open(txt_path, 'w', encoding='utf-8') as txt_file:
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text = page.extract_text()
                if text:
                    txt_file.write(text)
                    txt_file.write("\n")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: convert_pdf_to_txt.exe <pdf_path> <txt_path>")
    else:
        pdf_path = sys.argv[1]
        txt_path = sys.argv[2]
        pdf_to_text(pdf_path, txt_path)
