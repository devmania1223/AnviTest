import jwt
import json
from datetime import datetime
from fastapi import HTTPException,Request, Response, status, FastAPI
from services.database_service import DatabaseService
from utils import constants

app = FastAPI()

from logging.config import dictConfig
import logging
from logconfig import LogConfig

dictConfig(LogConfig().dict())
logger = logging.getLogger("mycoolapp")

@app.middleware('http')
async def check_authentication(request: Request, call_next):
    token = request.cookies.get(constants.COOKIE_NAME)

    logger.info(token)

    if not token:
        return Response(
            content=json.dumps({
                'detail': 'No token found',
            }),
            media_type='application/json',
            status_code=status.HTTP_401_UNAUTHORIZED,
        )
    token = str.replace(str(token), 'Bearer ', '')

  
    # Decode the incoming token
    payload: dict = jwt.decode(
        jwt=token,
        key=constants.SECRET_KEY,
        algorithms=['HS256'],
    )
    
    # Extract the email and expiration from the payload
    email = payload.get("email")
    expiration = payload.get("exp")    

    if expiration < (datetime.now() - datetime(1970, 1, 1)).total_seconds():
        raise HTTPException(status_code=401,detail=f"The session is expired.") 

    # Get the user by email
    
    logger.info("dashboard")
    user = DatabaseService.get_user_by_email(email=email) 
    if not user:
        raise HTTPException(status_code=401,detail=f"The user does not exists.")

    response = await call_next(request)
    return response


@app.get('/verify-authentication')
def verify_authentication():
    # This empty method is used to verify authentication when user changes route manually.
    return


@app.get('/getData')
def getData():
    return DatabaseService.getData()
