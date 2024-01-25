#
# EXAM QCM FASTAPI
# Florence Auréart
#
#

import data as db
from typing import Optional
import random

##retourne un booleen ok =1
def add_question(question: str, subject: str, use: str, correct: str, \
                 responseA: str, responseB: str, responseC: str, responseD: Optional[str] = None) -> bool:
    request = db.add_question(question, subject, use, correct, \
                              responseA, responseB, responseC, responseD)
    return request 