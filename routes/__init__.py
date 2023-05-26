from .product import product
from sanic import Blueprint

from .user import user

blueprint_group = Blueprint.group(
    product,
    user
)
