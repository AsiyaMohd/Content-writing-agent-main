
import pdfplumber
import io
import docx
 
def pdfdata(file)->str:
    file_text=""
    filename=file.filename.lower()
    print(filename)
    file_bytes=file.read()
    file.stream.seek(0)
    if filename.endswith(".pdf"):
        with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
            for page in pdf.pages:
               file_text+=page.extract_text() +"\n"
        return file_text
    elif filename.endswith(".txt"):
        file_text=file.read().decode('utf-8')
        return file_text
    else:
        doc = docx.Document(io.BytesIO(file_bytes))
        file_text = "\n".join(p.text for p in doc.paragraphs)
        return file_text