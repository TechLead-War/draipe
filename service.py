from tortoise.contrib.sanic import register_tortoise
from sanic import Sanic
from sanic_cors import CORS
from sanic_limiter import Limiter, get_remote_address

from routes import blueprint_group
from utils.bots import block_bots, log_request
from utils.env import CONFIG
from urllib.request import Request


app = Sanic(name='Draipe')
app.config.update_config(CONFIG.config)
cors = CORS(app, resources={r"/*": {"origins": "*"}})  # allow all routes
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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
