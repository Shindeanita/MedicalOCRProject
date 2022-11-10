from pdf2image import convert_from_path
import pytesseract
import util
from backend.src.parser_prescription import PrescriptionParser
from backend.src.parser_patientdetails import PatientDetailsParser

#poppler is used for image to pdf conversion
#pytesseract is used for image to string conversion

POPPLER_PATH = r'C:\poppler-22.04.0\Library\bin'
pytesseract.pytesseract.tesseract_cmd=r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extract(file_path,file_format):
    # extraction text from pdf file
    pages = convert_from_path(file_path, poppler_path=POPPLER_PATH)
    document_text = ''
    #for page in pages:
    if len(pages)>0:
        page = pages[0]
        processed_image = util.preprocess_image(page)
        text = pytesseract.image_to_string(processed_image, lang="eng")
        document_text = '\n' + text
    #step 2 : check file format
    if file_format == 'prescription':
        extracted_data = PrescriptionParser(document_text).parse()
    elif file_format =='patient_details':
        extracted_data = PatientDetailsParser(document_text).parse()
    else:
        raise Exception(f"Invalid File format: {file_format}")
    #step 3 : Return the data
    return extracted_data
if __name__ == '__main__':
    data = extract('../resources/patient_details/pd_1.pdf','patient_details')
    print(data)
