from app.repositories.user import UserRepository


class AuthServices:
    def __init__(self, repository: type[UserRepository]):
        self.repository = repository

    async def create_access_token(self):
        pass

    async def get_id_from_token(self):
        pass

    async def get_email_from_token(self):
        pass

    async def verify_token(self):
        pass

    async def login(self):
        pass
