#
# EXAM QCM FASTAPI
# Florence Auréart
#
#
import os
import pandas as pd
import numpy as np
from  fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional


def export_df(df, file_name):
    try:
        if os.path.isfile(file_name):
            os.remove(file_name)
            df.to_csv(file_name)
            return True 
    except Exception as e:
            print(f"Erreur lors de l'exportation du DataFrame : {e}")

def prepare_dataset(file_name: str):
    try:
        df = pd.read_csv(file_name)
        if 'Unnamed: 0.1' in df.columns:
            df.rename(columns={'Unnamed: 0':'index'}, inplace=True)
            df.drop('Unnamed: 0.1', axis=1, inplace=True)
        export_state = export_df(df, file_name)
        return export_state
    except pd.errors.EmptyDataError:
        print("Erreur : Le fichier CSV est vide.")
        return False
    except FileNotFoundError:
        print("Erreur : Fichier non trouvé.")
        return False
    except Exception as e:
        print(f"Erreur inattendue : {e}")
        return False

def initialise_df() -> bool:
    df = pd.read_csv('questions.csv')
    return df

def get_df():
    if not os.path.isfile('questions.csv'):
        prepare_dataset('questions.csv')
    return pd.read_csv('questions.csv')


def get_nb_questions():
    #df = pd.read_csv('questions.csv')# ou df = get_df()
    df = get_df()
    return df.shape[0] 

def get_uses():
    df = get_df()
    return np.unique(df.use.values).tolist()

def get_subjects():
    df = pd.read_csv('questions.csv')
    return np.unique(df.subject.values).tolist()

def get_questions(use: str, subjects: list) -> list:
    df = pd.read_csv('questions.csv')
    if subjects:  # Si la liste des sujets n'est pas vide
        filtered_questions = df[(df.use == use) & (df.subject.isin(subjects))].question.tolist()
    else:  # Si la liste des sujets est vide
        filtered_questions = df[df.use == use].question.tolist()
    #if not filtered_questions:
    #    raise HTTPException(status_code=404, detail="Aucune question trouvée pour les critères donnés.")
    return filtered_questions

def add_question(question: str, subject: str, use: str, correct: str,\
                 responseA: str, responseB: str, responseC: str, responseD: Optional[str] = None) -> bool:
    df = get_df()
    new_row = {'question':question, 'subject':subject, 'use':use, 'correct':correct,\
               'responseA': responseA, 'responseB': responseB, \
               'responseC': responseC, 'responseD': responseD, 'remark':''}
    df = df.append(new_row, ignore_index=True)
    export_state = export_df(df, 'questions.csv')
    return True
 