from starlette.applications import Starlette
from starlette.requests import Request
from starlette.routing import Route, Mount
from starlette.endpoints import HTTPEndpoint
from starlette.responses import FileResponse, Response
from starlette.staticfiles import StaticFiles
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware


async def index(self, request: Request):
    return FileResponse("index.html")


async def post(self, request: Request):
    letter = request.path_params["letter"]
    if letter not in "ony":
        return Response(status_code=404)

    data = await request.json()
    with open("db/" + letter, "a") as file:
        file.write(''.join(map(str, data)) + '\n')
    return Response()


app = Starlette(
    routes=[
        Route('/', index),
        Route("/{letter}", post),
        Mount("/static", StaticFiles(directory="static"))
    ],
    # middleware=[
    #     Middleware(
    #         CORSMiddleware,
    #         allow_origins=['*'],
    #         allow_credentials=True,
    #         allow_methods=['*'],
    #         allow_headers=['*']
    #     )
    # ]
)
