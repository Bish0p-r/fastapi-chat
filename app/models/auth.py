from datetime import datetime, timedelta

from beanie import Document


class RefreshToken(Document):
    user_id: str
    refresh_token: str
    expires_at: datetime = datetime.utcnow() + timedelta(days=30)
    created_at: datetime = datetime.utcnow()

    class Settings:
        name = "refreshTokens"

