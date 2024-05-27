import asyncio
import math
from datetime import datetime

import httpx
import pandas as pd
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


def render_sse_html_chunk(event, chunk, attrs=None):
    if attrs is None:
        attrs = {}
    tmpl = templates.get_template("partials/streaming_chunk.jinja2")
    html_chunk = tmpl.render(event=event, chunk=chunk, attrs=attrs)
    return html_chunk


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


@app.get("/stream-chart", response_class=StreamingResponse)
async def energy_stream(service: EnergyDataService = Depends(get_energy_service)):
    async def streaming_data():
        ## TODO REPLACE HARD CODED DATE RANGE
        start_date = pd.Timestamp("2019-01-29")
        end_date = pd.Timestamp("2019-02-04 23:00:00")
        
        chart_state = {
            "x_state": [],
            "y_state": [],
        }
        
        async for energy_data in service.stream_all():
            for data in energy_data:
                
                chart_state["y_state"].extend([data.value])
                chart_state["x_state"].extend([data.period])

    
                values = [value for value in chart_state["y_state"]]
                hours = [period for period in chart_state["x_state"]]
                
                source = ColumnDataSource(data=dict(hours=hours, values=values))

                fig = figure(
                    x_axis_type="datetime",
                    height=500,
                    tools="xpan",
                    width=1250,
                    title=f"Demand: MISO",
                    x_range=(start_date, end_date),
                )
                fig.title.align = "center"
                fig.title.text_font_size = "1em"
                fig.yaxis[0].formatter = NumeralTickFormatter(format="0.0a")
                fig.yaxis.axis_label = "Megawatt Hours"
                fig.y_range.start = 0
                fig.y_range.end = 150000
                fig.xaxis.major_label_text_font_size = "6pt"
                fig.xaxis.major_label_orientation = math.pi / 4

                fig.line(
                    x="hours",
                    y="values",
                    source=source,
                    line_width=2,
                )

                # hover = HoverTool(
                #     tooltips=[
                #         ("Value", "@values{0.00}"),
                #         ("Hours", "@hours{%F %T}"),
                #     ],
                #     formatters={
                #         "@hours": "datetime",
                #     },
                #     mode="vline",
                #     show_arrow=False,
                # )
                # fig.add_tools(hover)

                script, div = components(fig)
                # print(f"script: {script} \n div: {div}")
                context = {
                    "script": script.replace("\n", " "),
                    "div": div.replace("\n", " "),
                }
                chunk = render_sse_html_chunk(
                    "linechart", context, attrs={"id": "linechart", "hx-swap-oob": "true"}
                )
                # print(f"Chunk: {chunk}")
                yield f"{chunk}\n\n".encode("utf-8")
                await asyncio.sleep(.5)

    return StreamingResponse(streaming_data(), media_type="text/event-stream")


@app.get("/", name="index")
async def index(request: Request):
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
