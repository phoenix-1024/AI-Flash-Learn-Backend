from fastapi import FastAPI, UploadFile, HTTPException, File, Response, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse, FileResponse
import os
from typing import List
from service import read_pdf, read_docx, write_docx, zip_files, simplify_para, simplify_all_para
import asyncio
from database import get_db, Question, Document, Session

app = FastAPI()


@app.get("/")
async def read_root():
    # Serve your index.html file
    return FileResponse("frontend/index.html")


@app.post("/make_flash_cards")
async def make_flash_cards(
    files: UploadFile, 
    b : BackgroundTasks,
    db: Session = Depends(get_db)):
    doc = Document(doc_name = file.filename,status=)
    db.add(doc)
    db.commit()
    b.add_task(make_qas,doc,file.file.read())
    return {"message": "success"}

async def make_qas(doc,file_bytes)

    if file.filename.endswith('.pdf'):
        all_para = read_pdf(file_bytes)
        
    elif file.filename.endswith('.docx'):
        all_para = read_docx(file_bytes)
    else:
        raise Exception(f"file: {file.filename} \nFile type not supported. Only PDF files are accepted.")
    QAs = await make_qa_from_all_para(all_para)
    
    doc_id = doc.doc_id
    
    for QA in QAs:
        que = Question(doc_id = doc_id, **QA)
        db.add(que)
        db.commit()

    return {"message":"success"}



