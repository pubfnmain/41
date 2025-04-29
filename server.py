from starlette.applications import Starlette
from starlette.requests import Request
from starlette.routing import Route, Mount
from starlette.endpoints import HTTPEndpoint
from starlette.responses import FileResponse, JSONResponse, Response
from starlette.staticfiles import StaticFiles
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
import tensorflow as tf
import numpy as np
from uvicorn import run

from model.config import model, CKPT


model.load_weights(CKPT)

predictor = tf.keras.Sequential([
    model,
    tf.keras.layers.Softmax()
])



classes = "абвгдеёжзийклмнңоөпрстуүфхцчшщъыьэюя"


async def index(request: Request):
    data = await request.json()
    predict = predictor.predict(np.array([data]))[0]
    predict = np.round(predict, 2) * 100
    return JSONResponse({
        j: int(predict[i])
        for i, j in enumerate(classes)
    })


app = Starlette(
    routes=[
        Route("/", index, methods=["POST"]),
    ],
    middleware=[
        Middleware(
            CORSMiddleware,
            allow_origins=['*'],
            allow_credentials=True,
            allow_methods=['*'],
            allow_headers=['*']
        )
    ]
)


if __name__ == "__main__":
    run(app)
