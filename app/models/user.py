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
