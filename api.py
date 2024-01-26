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
    question: str, subject: str, correct: str, use: str,
    responseA: str, responseB: str, responseC: str, responseD: Optional[str] = None,
    username: str = Depends(auth.is_admin)
):

    # Validation des sujets et utilisations
    valid_subjects = db.get_subjects()
    valid_uses = db.get_uses()
    if subject not in valid_subjects:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Le sujet n'est pas valide.")
    if use not in valid_uses:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="L'utilisation spécifiée n'est pas valide.")

    # Tentative d'ajout de la question
    try:
        request = qcm.add_question(question, subject, correct, use, responseA, responseB, responseC, responseD)
        if not request:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erreur lors de l'ajout de la question.")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    # Réponse en cas de succès
    return {
        'results': {
            'username': username,
            'question': question, 'subject': subject, 'correct': correct,
            'use': use, 'responseA': responseA, 'responseB': responseB,
            'responseC': responseC, 'responseD': responseD
        }
    }

