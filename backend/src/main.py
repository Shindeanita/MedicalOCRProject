from fastapi import FastAPI, Form, UploadFile, File
from extractor import extract
import uuid
import os
import uvicorn

app = FastAPI()

@app.get('/get_movie_name')
def get_movie_name():
    return "KGF2"

@app.post("/extractor_form_data")
def extract_form_data(
        file_format:str = Form(...),
        file:UploadFile = File(...)):

    contents = file.file.read()
    #file_path = '../uploads/test.pdf'
    file_path = '../uploads/' + str(uuid.uuid4()) + '.pdf'

    with open(file_path,'wb') as f:
        f.write(contents)

    try:
        data = extract(file_path,file_format)
    except Exception as e:
        data = {
            'error' : str(e)
        }
    if os.path.exists(file_path):
        os.remove(file_path)

    return data

if __name__ == '__main__':
    uvicorn.run(app,host='127.0.0.1',port=8000)


