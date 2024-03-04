from pydantic import BaseModel


class JsonResponseSchema(BaseModel):
    detail: str
