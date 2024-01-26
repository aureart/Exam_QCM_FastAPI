#
# EXAM QCM FASTAPI
# Florence Auréart
#
#

import data as db
from typing import Optional
from  fastapi import FastAPI, Depends, Query, HTTPException, status
import random

##retourne un booleen ok =1
def add_question(question: str, subject: str, use: str, correct: str, \
                 responseA: str, responseB: str, responseC: str, responseD: Optional[str] = None) -> bool:
    request = db.add_question(question, subject, use, correct, \
                              responseA, responseB, responseC, responseD)
    return request 


def get_qcm (use: str, subjects: list, nbr: int) -> list:
    print (' QCM Aléatoire ', use, subjects, nbr)
    mylist = db.get_questions(use, subjects)
    if not mylist:
        raise HTTPException(status_code=404, detail="Aucune question trouvée pour les critères donnés.")
    random.shuffle(mylist)  # Mélanger la liste pour une distribution aléatoire
    return mylist[:nbr]  # Retourner les premières 'nbr' questions