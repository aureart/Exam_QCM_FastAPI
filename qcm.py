#
# EXAM QCM FASTAPI
# Florence Auréart
#
#

import data as db
import random

def add_question(question: str, subject: str, use: str, correct: str, \
                 responseA: str, responseB: str, responseC: str, responseD: str) -> bool:
    request = db.add_question(question, subject, use, correct, \
                              responseA, responseB, responseC, responseD)
    return request 