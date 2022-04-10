from typing import Optional
from pydantic import BaseModel
from pydantic.types import StrictStr, StrictInt


class UserModel(BaseModel):
    id: Optional[StrictInt]
    email: StrictStr
    password: StrictStr


class RegisterModel(BaseModel):
    email: StrictStr
    password: StrictStr
    passwordRepeat: StrictStr
