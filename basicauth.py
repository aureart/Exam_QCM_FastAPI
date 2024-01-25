from fastapi import Depends, FastAPI, HTTPException, status
import secrets
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from passlib.context import CryptContext

'''Nous utilisons les fonctions Depends, FastAPI, HTTPException et status du module fastapi. Depends sera utile pour appliquer des 
dépendances pour exiger une authentification avant d'accéder à une route. 

HTTPException et status seront utiles pour lever des exceptions avec des erreurs. 

Nous importons également HTTPBasicet HTTPBasicCredentialsdu module fastapi.securitypour employer la méthode HTTP Basic Auth 
et pour utiliser le formulaire d'authentification à l'aide deHTTPBasicCredentials. 
Enfin, nous avons importé les modules passlib.context pour crypter les mots de passes qui seront donnés dans le formulaire d'authentification.'''

security = HTTPBasic()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

users = {
                "alice": "wonderland",
                "bob": "builder",
                "clementine": "mandarine",
                "admin": "4dm1N"
}

#Je completerais avec une versions des users en BaseModel plus tard

def is_identified(credentials: HTTPBasicCredentials = Depends(security)):
    for user, passwd in users.items():
       if secrets.compare_digest(credentials.username, user):
           if secrets.compare_digest(credentials.password, passwd):
               return True
    return False


def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    if not (is_identified(credentials)):
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Incorrect email or password",
            headers = {"WWW-Authenticate" : "Basic"},
        )
    return credentials.username

def get_current_user(credentials: HTTPBasicCredentials = Depends(security)):
    username = credentials.username
    if not(users.get(username)) or not(pwd_context.verify(credentials.password, users[username]['hashed_password'])):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username
'''Dans le code ci-dessus, on récupère dans la variable credentials les identifiants entrés par l'utilisateur à l'aide de la dépendance Depends(security). Ce qui veut dire que l'on exige par cette dépendance, l'authentification de l'utilisateur à l'aide de la méthode HTTP.

On récupère l'identifiant et le mot de passe de l'utilisateur grâce aux attributs username et password de la variable credentials. 
On vérifie si l'identifiant est présent dans la base de données. 
Ensuite, on compare si le mot de passe crypté correspond bien à celui de la base de données en utilisant la méthode verify de la variable pwd_context. 
On lève une erreur 401 si ils ne correspondent pas. Sinon, on renvoie l'identifiant de l'utilisateur.'''
