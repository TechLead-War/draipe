from sanic import Blueprint

from .product import product
from .user import user

blueprint_group = Blueprint.group(
    product,
    user
)
