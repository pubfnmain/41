from starlette.applications import Starlette
from starlette.requests import Request
from starlette.routing import Route, Mount
from starlette.endpoints import HTTPEndpoint
from starlette.responses import FileResponse, Response
from starlette.staticfiles import StaticFiles
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware


class Index(HTTPEndpoint):
    async def get(self, request: Request):
        return FileResponse("index.html")

    async def post(self, request: Request):
        data = await request.json()
        print(data)
        return Response() 


app = Starlette(
    routes=[
        Route('/', Index),
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
