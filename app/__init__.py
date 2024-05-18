from fastapi import FastAPI
from .routes import routes

def create_app():
    # Create a FastAPI application instance
    app = FastAPI(title="Energy Dashboard")
            
    # Include the router for handling API routes
    app.include_router(routes.router, prefix="/api/v1")
    
    return app

app = create_app()