from datetime import datetime, timedelta
import jwt
from fastapi import status, HTTPException, Response, FastAPI, Request
from models.user import RegisterModel, UserModel
from services.database_service import DatabaseService
from utils import constants
import re


from logging.config import dictConfig
import logging
from logconfig import LogConfig

dictConfig(LogConfig().dict())
logger = logging.getLogger("mycoolapp")

app = FastAPI()


@app.post('/login')
def login(payload: UserModel):
    user = DatabaseService.get_user_by_email(email=payload.email)    

    if not user:
        raise HTTPException(status_code=400,detail=f"The user does not exists.")
    
    if payload.password != user.password:
        raise HTTPException(status_code=400,detail=f"The password is wrong.")
    
    # Set the expiration time to the current time + constants.TOKEN_VALID_IN_SECONDS
    expiration_time = datetime.now() + timedelta(seconds=constants.TOKEN_VALID_IN_SECONDS)

    # Create a JWT token with the email and the expiration time (as a timestamp) as payload
    token = jwt.encode(
        payload={"email":payload.email,"exp":expiration_time},
        key=constants.SECRET_KEY, 
        algorithm='HS256',
    )
    logger.info(token)

    response = Response(
        status_code=status.HTTP_200_OK,
    )
    # Append the Set-Cookie to this response

    response.set_cookie(
        constants.COOKIE_NAME,
        value=f"Bearer {token}",
        httponly=True,
        max_age=constants.TOKEN_VALID_IN_SECONDS,
        expires=constants.TOKEN_VALID_IN_SECONDS,
        secure=False,
    )

    return response


@app.post('/logout')
def logout(request: Request):
    token = request.cookies.get(constants.COOKIE_NAME)
    response = Response(
        status_code=status.HTTP_200_OK,
    )
    logger.info(token)
    if token:
        response.delete_cookie(constants.COOKIE_NAME)    
        logger.info("removed cookie")
    return response


@app.post('/register')
def register(payload: RegisterModel):  

    email = payload.email.lower()     
 
    if not re.fullmatch(constants.EMAIL_REGEX, email):
        raise HTTPException(status_code=400, detail=f"Sorry, your email is not valid")  
    
    logger.info(email)
    user = DatabaseService.get_user_by_email(email)    
    if user:
        raise HTTPException(status_code=400,detail=f"The user with the email already exists.")

    if payload.password != payload.passwordRepeat:
        raise HTTPException(status_code=400,detail=f"The password does not matched.")

  
    if len(payload.password) < constants.MINIMUM_PASSWORD_LENGTH:
        raise HTTPException(status_code=400,detail=f"Please enter a password of at least 6 characters")
 
    DatabaseService.create_user(payload=payload)

    # Set the expiration time to the current time + constants.TOKEN_VALID_IN_SECONDS
    expiration_time = datetime.now() + timedelta(seconds=constants.TOKEN_VALID_IN_SECONDS)

    # Create a JWT token with the email and the expiration time (as a timestamp) as payload
    token = jwt.encode(
        payload={"email":payload.email,"exp":expiration_time},
        key=constants.SECRET_KEY,
        algorithm='HS256',
    )
    logger.info(token)
    response = Response(
        status_code=status.HTTP_200_OK,
    )
    # Append the Set-Cookie to this response

    response.set_cookie(
        constants.COOKIE_NAME,
        value=f"Bearer {token}",
        httponly=True,
        max_age=constants.TOKEN_VALID_IN_SECONDS,
        expires=constants.TOKEN_VALID_IN_SECONDS,
        secure=False,
    )

    return response
