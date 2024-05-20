import uvicorn
from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from .routes import router

def create_app():
    app = FastAPI()

    # Include the router for API endpoints
    app.include_router(router, prefix="/api/v1")

    # Set up the templates directory for Jinja2
    templates = Jinja2Templates(directory="src/energy_dashboard/templates")
    
    @app.get("/")
    async def serve_dashboard(request: Request):
        # Serve the dashboard using the index.html template
        return templates.TemplateResponse("index.html", {"request": request})
    
    return app

# Create the FastAPI app
app = create_app()

if __name__ == "__main__":
    # Run the app using uvicorn
    uvicorn.run("src/energy_dashboard.main:app", host="0.0.0.0", port=8000, reload=True)
