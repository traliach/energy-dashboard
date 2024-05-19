import uvicorn
from fastapi import FastAPI
from app.routes import router
from app.config import database

def create_app():
    app = FastAPI()

    @app.on_event("startup")
    async def startup():
        await database.connect()

    @app.on_event("shutdown")
    async def shutdown():
        await database.disconnect()

    app.include_router(router, prefix="/api/v1")
    return app

app = create_app()

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
