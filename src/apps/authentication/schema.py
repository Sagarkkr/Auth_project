from enum import Enum
from pydantic import BaseModel, Field
from mongoengine import Document, StringField, BooleanField
from mongoengine.fields import EnumField
import bcrypt

class UserChoice(Enum):
    ADMIN = 'admin'
    USER = 'user'

class User(BaseModel):
    username:str | None = StringField(required=True, unique=True)
    password:str | None = StringField(required=True)
    is_new_user: bool | None = BooleanField(default=False)
    is_active: bool | None = BooleanField(default=True)
    role: UserChoice | None = Field(default=None)

    def set_password(self, raw_password):
        self.password = bcrypt.hashpw(raw_password.encode(), bcrypt.gensalt()).decode()
        print(self.password)

    def check_password(self, raw_password):
        return bcrypt.checkpw(raw_password.encode(), self.password.encode())
