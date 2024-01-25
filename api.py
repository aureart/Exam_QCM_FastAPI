#
# EXAM QCM FASTAPI
# Florence Auréart
#
#

from  fastapi import FastAPI, Depends, Query, HTTPException, status
from typing import List, Optional
import uvicorn
from typing import Optional
from pydantic import BaseModel, validator
import data as db
import basicauth as auth
import qcm


app = FastAPI(
    title="Exam Fastapi Auréart",
    description="Exam Fastapi Auréart powered by FastAPI.",
    version="0.0.1")


@app.get("/")
async def get_index():
    return {"message": "Bienvenue sur l'API des QCM"}


@app.get('/check_fonctionnel')
async def check(qui: str = Depends(auth.is_identified)):
    available_questions = "Non disponible"
    try:
        # Tentative de connexion au fichier csv
        available_questions =  db.get_nb_questions()
        df_status = "Connecté"
        
    except Exception as e:
        df_status = f"Erreur: {e}"
    return {
        'fichier csv':df_status,
        'nb de questions disponibles': available_questions,
        'personne loggée':qui
    }

@app.get("/current_user")
async def authenticate_user(username: str = Depends(auth.get_current_username)):

    return {
                'results': username
    }