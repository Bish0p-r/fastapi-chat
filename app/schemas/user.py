from beanie import PydanticObjectId
from pydantic import BaseModel, ConfigDict, EmailStr, Field, model_validator


class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=50)


class UserCreateSchema(UserLoginSchema):
    confirm_password: str = Field(min_length=8, max_length=50)
    first_name: str = Field(min_length=4, max_length=50)
    last_name: str = Field(min_length=4, max_length=50)

    @model_validator(mode="after")
    def check_passwords_match(self):
        pw1 = self.password
        pw2 = self.confirm_password

        if pw1 is not None and pw2 is not None and pw1 != pw2:
            raise ValueError("passwords do not match")
        return self


class UserUpdateSchema(BaseModel):
    model_config = ConfigDict(extra="forbid")

    first_name: str = Field(min_length=4, max_length=50)
    last_name: str = Field(min_length=4, max_length=50)


class UserSchema(BaseModel):
    id: PydanticObjectId
    first_name: str
    last_name: str
    email: EmailStr


class UserIdSchema(BaseModel):
    id: PydanticObjectId = Field(alias="user_id")
