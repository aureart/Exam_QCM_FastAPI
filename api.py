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

# --------use et subject identique a la liste actuelle------------------------------------------
# --------je peux faire un aure methode pour creer une question sur un nouveau sujet ou use-----
@app.post("/ajout_question")
async def post_question(
    # Query parameters
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
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Le use  n'est pas valide.")

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

# ----------------------------------------
# Conna^tre les use disponibles
# --------------------------------------------
@app.get("/uses")
async def get_uses(username: str = Depends(auth.is_identified)):
    available_uses = db.get_uses()
    return {
        
        'results': available_uses
    }
# ---------------------


# --------------------------------------------
# Conna^tre les sujets disponibles
# --------------------------------------------
@app.get("/subjects")
async def get_subjects(username: str = Depends(auth.is_identified)):
    available_subjects = db.get_subjects()
    return {
        
        'results': available_subjects
    }


#-----------------------------------------------
@app.get("/qcm/")
async def get_qcm(
    # Query parameters
        number: int = Query(
                  5,
                  title = "Number (Nombre de questions)",
                  description = "Choisir entre les nombres suivants :  [5, 10, 20]",

              ), 
        use:  str = Query(
                 #db.get_uses(),
                 "Test de positionnement",
                 title = "Use (type de questions)",
                 description = f"Use, <br> \
                                 {db.get_uses()}",
  
             ), 
        subjects: 
              Optional[List[str]] = Query(
                  db.get_subjects(),
                  title = "Subject ",
                  description = "Optionnel : choisir un sujet.",

              ), 
        username: str = Depends(auth.is_identified)
    ):
    valid_numbers = [5, 10, 20]
    valid_qcm_subjects = db.get_subjects()
    valid_uses = db.get_uses()
    if number not in valid_numbers:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Choisir un chiffre entre 5,10 ou 20 svp")
    #if subjects not in valid_qcm_subjects:
    #    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Le sujet n'est pas valide.")
    if use not in valid_uses:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Le use  n'est pas valide.")

    results = qcm.get_qcm(use, subjects, int(number))
    return {
        'results':{
                      "use": use,
                      "subject": subjects,
                      "number": int(number),
                      "results": results
        }
            
    }