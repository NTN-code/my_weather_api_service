import os
from fastapi import FastAPI, Request, Depends
from dto import Point, TimeInterval
from utils import get_temp

app = FastAPI(
    title="Weather API"
)


@app.get("/ping")
async def ping(request: Request) -> str:
    return "OK"


@app.get("/getForecast")
async def get_forecast_weather(request: Request, time_interval: TimeInterval = Depends(), point: Point = Depends()) -> dict:
    filenames = [
        filename for filename in os.listdir("./data")
        if int(filename.split(".")[0]) in range(time_interval.from_ts, time_interval.to_ts)
    ]

    result = {}
    for filename in filenames:
        name, ext = filename.split('.')
        data = await get_temp(filename, point)
        if data:
            result[name] = data
    return result
