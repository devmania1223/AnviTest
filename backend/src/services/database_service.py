import sqlite3
import json
from sqlite3 import Cursor, Row
from typing import List
from fastapi import status
from fastapi.exceptions import HTTPException
from models.user import RegisterModel, UserModel
from utils import constants
import random

from logging.config import dictConfig
import logging
from logconfig import LogConfig

dictConfig(LogConfig().dict())
logger = logging.getLogger("mycoolapp")


class DatabaseService:
    @staticmethod
    def getData() -> List[int]:
        try:
            data = []
            for i in range(0 , 8):
                n = random.randint(1,100)
                data.append(n)
            return data
        except Exception as e:
            raise HTTPException(
                detail=str(e),
                status_code=status.HTTP_400_BAD_REQUEST,
            )

    @staticmethod
    def create_user(payload: RegisterModel):
        try:
            conn = sqlite3.connect(constants.DB_FILE)
            conn.row_factory = DatabaseService._dict_factory

            cursor = conn.cursor()
            cursor.execute("insert into accounts(email, password) values(:email, :password)" ,{"email":payload.email,"password":payload.password})
            conn.commit()
        except Exception as e:
            raise HTTPException(
                detail=str(e),
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        finally:
            if conn:
                conn.close()

    @staticmethod
    def get_user_by_email(email: str) -> UserModel:
        try:
            conn = sqlite3.connect(constants.DB_FILE)
            conn.row_factory = DatabaseService._dict_factory

            cursor = conn.cursor()
            cursor.execute("select * from accounts where email = :email" , {"email":email})
            user =  cursor.fetchone()
            if user:
                return UserModel.parse_obj(user)
            return user
        except Exception:
            raise HTTPException(
                detail='User not found',
                status_code=status.HTTP_404_NOT_FOUND,
            )
        finally:
            if conn:
                conn.close()

    # Private Methods
    @staticmethod
    def _dict_factory(cursor: Cursor, row: Row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d
