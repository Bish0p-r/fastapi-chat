from pydantic import BaseModel, Field, model_validator, EmailStr
from beanie import Document


class User(Document):
    first_name: str
    last_name: str
    email: str
    hashed_password: str
    is_active: bool = False
    is_superuser: bool = False

    class Settings:
        name = "users"


class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=50)


class UserCreateSchema(UserLoginSchema):
    confirm_password: str = Field(min_length=8, max_length=50)
    first_name: str = Field(min_length=8, max_length=50)
    last_name: str = Field(min_length=8, max_length=50)

    @model_validator(mode="after")
    def check_passwords_match(self):
        pw1 = self.password
        pw2 = self.confirm_password

        if pw1 is not None and pw2 is not None and pw1 != pw2:
            raise ValueError("passwords do not match")
        return self
