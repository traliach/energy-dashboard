from fastapi import FastAPI
from .routes import router
from .models import get_engine, get_session_factory, get_base
import uvicorn

def create_app():
    app = FastAPI(title="Energy Dashboard")
    app.include_router(router)
    return app

if __name__ == "__main__":
    engine = get_engine("postgresql+asyncpg://user:password@localhost/energydb")
    session_factory = get_session_factory(engine)
    Base = get_base()
    Base.metadata.create_all(bind=engine)
    app = create_app()
    uvicorn.run(app, host="0.0.0.0", port=8000)
