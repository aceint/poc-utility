from fastapi import FastAPI, UploadFile, File
import fitz  # PyMuPDF

app = FastAPI()

@app.post("/upload-pdf/")
async def upload_pdf(file: UploadFile = File(...)):
    contents = await file.read()
    try:
        # Open the PDF from bytes
        doc = fitz.open(stream=contents, filetype="pdf")
        full_text = ""

        for page in doc:
            full_text += page.get_text() + "\n"

        return {"filename": file.filename, "extracted_text": full_text.strip()}

    except Exception as e:
        return {"error": str(e)}
