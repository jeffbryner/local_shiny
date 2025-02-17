# shiny base
from shiny import App, run_app
from starlette.applications import Starlette
from starlette.routing import Mount
from starlette.middleware import Middleware
from starlette.middleware.sessions import SessionMiddleware
import random, string

# setup shiny pages
from echo_chat import app_page_chat_ui, echo_chat_server

page_chat = App(ui=app_page_chat_ui, server=echo_chat_server)

# connect the pages to the routes
routes = [Mount("/", app=page_chat)]

# Declare a starlette app with session support
# make up a secret key
secret_key = "".join(
    random.choice(string.ascii_uppercase + string.digits) for _ in range(50)
)
middleware = [
    Middleware(SessionMiddleware, secret_key=secret_key, https_only=False),
]
app = Starlette(routes=routes, middleware=middleware)

if __name__ == "__main__":
    run_app("local_shiny:app", launch_browser=True, log_level="debug", reload=True)
