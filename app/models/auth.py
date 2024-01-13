from datetime import datetime, timedelta

from beanie import Document


class RefreshToken(Document):
    user_id: str
    user_agent: str
    refresh_token: str
    created_at: datetime = datetime.utcnow()
    expires_at: datetime = created_at + timedelta(days=30)


    class Settings:
        name = "refreshTokens"

