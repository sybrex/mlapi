import time
from fastapi import FastAPI
from starlette.requests import Request
from starlette.config import Config as AppConfig
from fastai.tabular import *
from fastai.vision import *
from io import BytesIO
import sys
import asyncio
import aiohttp


config = AppConfig('.env')
app = FastAPI()

async def predict_odds(base_markets, model_name):    
    learner = load_learner(Path(config('LEARNER_PATH')), model_name)
    data = pd.Series(base_markets)
    prediction = learner.predict(data)
    _, _, result = prediction    
    return round(result.item(), 2)

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

@app.get("/markets")
async def markets(mrft_home: float = 1, mrft_draw: float = 1, mrft_away: float = 1, ouft_over: float = 1, ouft_under: float = 1, bts_yes: float = 1, bts_no: float = 1):
    base_markets = {
        'MRFT_HOME': mrft_home,
        'MRFT_DRAW': mrft_draw,
        'MRFT_AWAY': mrft_away,
        'OUFT2.5_OVER': ouft_over,
        'OUFT2.5_UNDER': ouft_under,
        'BTS_YES': bts_yes,
        'BTS_NO': bts_no
    }  

    return {
        'DCFT': {'name': 'Double Chance Full Time', 'odds': {
            '1/2': predict_odds(base_markets, config('DTFT_HOME_AWAY_MODEL')),
            '1/X': predict_odds(base_markets, config('DTFT_HOME_DRAW_MODEL')),
            'X/2': predict_odds(base_markets, config('DTFT_DRAW_AWAY_MODEL')),
        }},
        'MRHT': {'name': 'Match Result Half Time', 'odds': {
            '1': predict_odds(base_markets, config('MRHT_HOME_MODEL')),
            'X': predict_odds(base_markets, config('MRHT_DRAW_MODEL')),
            '2': predict_odds(base_markets, config('MRHT_AWAY_MODEL'))
        }},
        'MRSH': {'name': 'Match Result Second Half', 'odds': {
            '1': predict_odds(base_markets, config('MRSH_HOME_MODEL')),
            'X': predict_odds(base_markets, config('MRSH_DRAW_MODEL')),
            '2': predict_odds(base_markets, config('MRSH_AWAY_MODEL'))
        }}
    }

async def get_bytes(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.read()

def predict_image_from_bytes(bytes):
    img = open_image(BytesIO(bytes))
    learner = load_learner(Path(config('LEARNER_PATH')), config('KLITSCHKO_MODEL'))
    pred_class, pred_idx, outputs = learner.predict(img)            
    return {
        'class': str(pred_class), 
        'rate': round(to_np(outputs)[try_int(pred_idx)].item(), 2)
    }

@app.get('/klitschko')
async def classify_url(url):
    bytes = await get_bytes(url)
    prediction = predict_image_from_bytes(bytes)
    return prediction

