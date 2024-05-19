import uvicorn
from fastapi import FastAPI
from .routes import router

def create_app():
    app = FastAPI()

    app.include_router(router, prefix="/api/v1")
    return app

app = create_app()

if __name__ == "__main__":
        uvicorn.run("src.energy_dashboard.main:app", host="0.0.0.0", port=8000, reload=True)
