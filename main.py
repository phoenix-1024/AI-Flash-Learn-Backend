from fastapi import FastAPI, UploadFile, HTTPException, File, Response, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse, FileResponse
import os
from typing import List
from service import read_pdf, read_docx, write_docx, zip_files, make_qa_from_all_para
import asyncio
from database import get_db, Question, Document, Session

app = FastAPI()

RUNNING = 'RUNNING'
COMPLETED = 'COMPLETED'


@app.post("/make_flash_cards")
async def make_flash_cards(
    f: UploadFile, 
    b : BackgroundTasks,
    db: Session = Depends(get_db)):
    doc = Document(doc_name = f.filename, status=RUNNING)
    db.add(doc)
    db.commit()
    doc.doc_id
    b.add_task(make_qas,doc,db,f.filename,f.file.read())
    return {"message": "success"}

async def make_qas(doc,db,file_name,file_bytes):
#    db = Session()
    if file_name.endswith('.pdf'):
        all_para = read_pdf(file_bytes)
        
    elif file_name.endswith('.docx'):
        all_para = read_docx(file_bytes)
    else:
        raise Exception(f"file: {file.filename} \nFile type not supported. Only PDF files are accepted.")
    QAs = await make_qa_from_all_para(all_para)
    
    doc_id = doc.doc_id
    
    for QA in QAs:
        que = Question(doc_id = doc_id, **QA)
        db.add(que)
        db.commit()
    doc.status = COMPLETED
    db.commit()
    db.close()
    print("should be updated now.",doc_id)

@app.get("/get_questions_by_doc_id")
async def get_questions_by_doc_id(doc_id, db: Session = Depends(get_db)):
    results = db.query(Question).filter_by(doc_id = doc_id).all()
    Qs = [r.question for r in results]
    return {"Questions": Qs}

    




