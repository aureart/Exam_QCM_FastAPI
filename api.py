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

# -----------------------------------------------
@app.post("/add_question")
async def post_question(
         question: str, subject: str, correct: str, use: str,\
         responseA: str, responseB: str, responseC: str, responseD: Optional[str] = None, \
         username: str = Depends(auth.is_admin)) :
    #valid_subjects = db.get_subjects()
    #valid_uses = db.get_uses()
    #if subject not in valid_subjects:
    #    raise ValueError("Le sujet n'est pas valide.")
    #if use is not None and use not in valid_uses:
    #    raise ValueError("L'utilisation spécifiée n'est pas valide.")
    request = qcm.add_question(question, subject, correct, use, \
                              responseA, responseB, responseC, responseD)
    if request :        
        return {

                   'results' : {
                               'username': username,
                               'question':question, 'subject':subject, 'correct':correct,
                               'use':use, 'responseA': responseA, 'responseB': responseB,
                               'responseC': responseC, 'responseD': responseD
                   }
         }
    else : 
        return { 'message d\'erreur un peu con'}