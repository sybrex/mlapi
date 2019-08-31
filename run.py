from starlette.applications import Starlette
from starlette.responses import JSONResponse, HTMLResponse, RedirectResponse
from starlette.config import Config as AppConfig
from io import BytesIO
import sys
import uvicorn
import aiohttp
import asyncio
from fastai.vision import *

config = AppConfig('.env')

app = Starlette()
learner = load_learner(Path(config('LEARNER_PATH')), config('MODEL'))

async def get_bytes(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.read()

def predict_image_from_bytes(bytes):
    img = open_image(BytesIO(bytes))
    pred_class, pred_idx, outputs = learner.predict(img)            
    return {
        'class': str(pred_class), 
        'rate': to_np(outputs)[try_int(pred_idx)].item()
    }

@app.route('/klitschko', methods=['GET'])
async def classify_url(request):
    bytes = await get_bytes(request.query_params['url'])
    prediction = predict_image_from_bytes(bytes)
    return JSONResponse(prediction)

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)