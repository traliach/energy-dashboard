import asyncio
import math

import httpx
from bokeh.embed import components
from bokeh.models import ColumnDataSource
from bokeh.models import HoverTool
from bokeh.models import NumeralTickFormatter
from bokeh.plotting import figure
from fastapi import APIRouter, Depends, FastAPI, Request
from fastapi.responses import StreamingResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from .database import AsyncSessionLocal, SessionLocal
from .services import EnergyDataService
from .utils import TEMPLATES_DIR

app = FastAPI()
router = APIRouter()
templates = Jinja2Templates(directory=TEMPLATES_DIR)

# Dependency function to get an instance of the database


## Async db: https://fastapi.tiangolo.com/tutorial/dependencies/
async def get_async_db():
    async_db = AsyncSessionLocal()
    try:
        yield async_db
    finally:
        await async_db.close()


## Sync db
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Dependency function to get an instance of EnergyDataService
def get_energy_service(
    db: Session = Depends(get_db), async_db: AsyncSession = Depends(get_async_db)
):
    return EnergyDataService(async_db, db, httpx.AsyncClient())


@app.get("/stream", name="stream", response_class=StreamingResponse)
async def stream_energy_data(
    request: Request, service: EnergyDataService = Depends(get_energy_service)
):
    """
    Stream the energy data as Server-Sent Events (SSE)
    """

    async def streaming_data():
        strm = service.stream_all()
        async for data in strm:
            yield f"data: {data.model_dump_json(indent=4)}\n\n"
            await asyncio.sleep(1)

    return StreamingResponse(streaming_data(), media_type="text/event-stream")

@app.get("/stream-chart", name="stream-chart", response_class=StreamingResponse)
async def stream_energy_data(
    request: Request, service: EnergyDataService = Depends(get_energy_service)
):
    async def streaming_data():
        # stream over the data and group by period
        data = service.stream_all()

        data_by_period = {}
        async for energy_data in data:
            period_date = energy_data.period
            if period_date not in data_by_period:
                data_by_period[period_date] = []
            data_by_period[period_date].append(energy_data)

        # iterate over periods and construct a bokeh ColumnDataSource for each energy data in each period.
        for period, data in data_by_period.items():
            respondents = [energy.respondent for energy in data]
            hourly_values = [energy.value for energy in data]

            source = ColumnDataSource(
                data=dict(respondents=respondents, hourly_values=hourly_values)
            )

            # Format the date in a more readable way
            formatted_date = period.strftime("%B %d, %Y at %I:%M %p")

            # Use the formatted date in the title
            fig = figure(
                x_range=respondents,
                height=500,
                width=1250,
                title=f"Hour: {formatted_date}",
            )

            # styling
            fig.title.align = "center"
            fig.title.text_font_size = "1em"
            fig.yaxis[0].formatter = NumeralTickFormatter(format="0.0a")
            fig.yaxis.axis_label = "Megawatt Hours"
            fig.xaxis.major_label_text_font_size = "6pt"
            fig.xaxis.major_label_orientation = math.pi / 4

            fig.vbar(x="respondents", top="hourly_values", width=1.0, source=source)

            hover = HoverTool(
                tooltips=[
                    ("Respondent", "@respondents"),
                    ("Value", "@hourly_values{0.00}"),
                ]
            )

            fig.add_tools(hover)
            script, div = components(fig)

            context = {
                "script": script,
                "div": div,
            }

            yield f"data: {context}\n\n"
            await asyncio.sleep(2)

    return StreamingResponse(streaming_data(), media_type="text/event-stream")


@app.get("/", name="index")
async def serve_dashboard(
    request: Request, service: EnergyDataService = Depends(get_energy_service)
):

    # Serve the dashboard using the index.html template
    return templates.TemplateResponse("index.html", {"request": request})


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


# Include the router for API endpoints
app.include_router(router)
