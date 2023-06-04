from urllib.request import Request

from sanic import Sanic
from sanic_cors import CORS
from sanic_limiter import Limiter, get_remote_address
from tortoise.contrib.sanic import register_tortoise

from context import user_tokens
from routes import blueprint_group
from utils.bots import block_bots, log_request
from utils.env import CONFIG, cors_origins

app = Sanic(name='Draipe')
app.config.update_config(CONFIG.config)
CORS(app, origins=cors_origins)

limiter = Limiter(app, key_func=get_remote_address)

app.blueprint(blueprint_group)


for route in app.router.routes:
    print(f"/{route.path} ")


register_tortoise(
    app, db_url=CONFIG.config["DB_URL"],
    modules={"users": ["models"]}, generate_schemas=True
)


@app.middleware('request')
async def call_logger(request: Request):

    """
        This function logs all incoming requests and checks if there is a bot
        attack.
    """
    await log_request(request)
    await block_bots(request)


# Dictionary to store user tokens
app.ctx.user_tokens = user_tokens
app.ctx.app = app


def set_user_token(user_id, token):
    # Function to set user token in the application context.
    app.ctx.user_tokens[user_id] = token


# uncomment it out, to set a context, each time, server restarts context gets
# deleted.

set_user_token(user_id="03e14af2-6050-4fa8-b487-3d5d1bc3c543", token="abc")


def get_user_token(user_id):
    # Function to get user token in the application context.
    return app.ctx.user_tokens[user_id]


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
