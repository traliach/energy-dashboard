import asyncio
from datetime import datetime

from databases import Database
from fastapi import APIRouter, Depends, FastAPI, Request
from fastapi.responses import StreamingResponse
import httpx
from jinja2 import Environment, FileSystemLoader
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates
from .services import EnergyDataService
from .models import SessionLocal, EnergyData
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.models import ColumnDataSource

app = FastAPI()
router = APIRouter()
templates = Jinja2Templates(directory="src/energy_dashboard/templates")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        

# Dependency function to get an instance of EnergyDataService
def get_energy_service(db: Session = Depends(get_db)):
    return EnergyDataService(db, httpx.AsyncClient())

@app.get("/")
async def serve_dashboard(request: Request, service: EnergyDataService = Depends(get_energy_service)):
    # Serve the dashboard using the index.html template
    data = service.list_all()

    result = {}
    for energy_data in data:
        period_date = energy_data.period
        if period_date not in result:
            result[period_date] = []
        result[period_date].append(energy_data)

    # iterate over periods and construct a bokeh ColumnDataSource for each energy data in each period. The x axis will be respondents the y axis will be values
    period, energy_data = result.popitem()
    x = [energy.respondent for energy in energy_data]
    y = [energy.value for energy in energy_data]
    source = ColumnDataSource(data=dict(x=x, y=y))
    p = figure(title=str(period), x_axis_label="Respondent", y_axis_label="Value")
    p.vbar(x="x", top="y", width=0.9, source=source)

    print(p)
    script, div = components(p)

    context = {
        "script": script,
        "div": div,
    }

    return templates.TemplateResponse(
        "index.html", {"request": request}, context=context
    )


@app.post("/api/v1/seed-data/")
async def seed_energy_data(service: EnergyDataService = Depends(get_energy_service)):
    return await service.fetch_data(
        params={
            "frequency": "hourly",
            "data[0]": "value",
            "facets[type][]": "D",
            "sort[0][column]": "period",
            "sort[0][direction]": "desc",
            "offset": 0,
            "length": 5000,
            "start": "2019-01-29T00",
            "end": "2019-02-04T23",
        }
    )


env = Environment(loader=FileSystemLoader("src/energy_dashboard/templates"))


# async def event_generator(request: Request):
#     last_id = 0
#     template = env.get_template("row.html")
#     while True:
#         query = (
#             f"SELECT * FROM energy_data WHERE id > {last_id} ORDER BY id ASC LIMIT 1"
#         )
#         row = await Database.fetch_one(query)
#         if row:
#             last_id = row.id
#             period = (
#                 row.period.isoformat()
#                 if isinstance(row.period, datetime)
#                 else datetime.strptime(row.period, "%Y-%m-%d %H:%M:%S.%f").isoformat()
#             )
#             data = {
#                 "period": period,
#                 "respondent": row.respondent,
#                 "respondent_name": row.respondent_name,
#                 "type": row.type,
#                 "value": row.value,
#             }
#             html_row = template.render(data=data)
#             yield f"data: {html_row}\n\n"
#         await asyncio.sleep(1)


# @router.get("/api/v1/stream")
# async def stream(request: Request):
#     return StreamingResponse(event_generator(request), media_type="text/event-stream")


# @router.get("/graph")
# async def stream(request: Request):
#     return StreamingResponse(event_generator(request), media_type="text/event-stream")


# Include the router for API endpoints
app.include_router(router)
