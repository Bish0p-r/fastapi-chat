from fastapi import FastAPI

from app.db.mongodb import init_db

from app.routes.user import router as user_router


app = FastAPI()

app.include_router(user_router)


@app.on_event("startup")
async def start_db():
    await init_db()

