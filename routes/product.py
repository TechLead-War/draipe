from urllib.request import Request
from sanic import Blueprint

from models.orm_wrappers import ORMWrapper
from models.products import Product
from sanic_jwt import protected, inject_user
from sanic.response import json
from utils.parsers import send_response


product = Blueprint("product")


# Get a specific product
@product.route('/products/<product_id>', methods=['GET'])
@protected()
@inject_user()
async def get_product(request: Request, product_id):
    try:
        result_set = await ORMWrapper.get_by_filters(model=Product, filters={
            "id": product_id
        })

        if not result_set:
            return json({'message': 'Product not found'}, status=404)

        return send_response(result_set)

    except Exception as ex:
        return json({'message': f'Failed to retrieve product, {ex}'},
                    status=500)


# Create a new product
@product.route('/products/create', methods=['POST'])
@protected()
@inject_user()
async def create_product(request: Request, user):
    try:
        payload = request.json  # Access the JSON payload

        title = payload.get("title")
        description = payload.get("description")
        price = payload.get("price")
        # Include other attributes as needed
        # check if these attribute exists

        result_set = await Product.create(
            title=title, description=description, price=price
        )

        return send_response({"message": "Product created successfully"})

    except Exception as e:
        return send_response({"message": "Failed to create product"}, status=500)


# Update an existing product
@product.route('/products/update/<product_id>', methods=['PUT'])
@protected()
@inject_user()
async def update_product(request: Request, product_id):
    try:
        result_set = await Product.get_or_none(id=product_id)
        if not result_set:
            return json({'message': 'Product not found'}, status=404)

        payload = request.json  # Access the JSON payload
        result_set.title = payload.get('sku_name', result_set.title)
        result_set.description = payload.get('description', result_set.description)
        result_set.price = payload.get('price', result_set.price)
        # Include other attributes as needed

        await result_set.save()

        return json({'message': 'Product updated successfully'})

    except Exception as ex:
        return json({'message': f'Failed to update product, {ex}'}, status=500)


# Delete a product
@product.route('/products/delete/<product_id>', methods=['DELETE'])
@protected()
@inject_user()
async def delete_product(request: Request, product_id):
    try:
        result_set = await Product.get_or_none(id=product_id)
        if not result_set:
            return send_response({'message': 'Product not found'},
                                 status_code=404)

        await result_set.delete()

        return send_response({'message': 'Product deleted successfully'})

    except Exception as ex:
        return send_response({'message': f'Failed to delete product, {ex}'},
                             status_code=500)


# 1. Error Handling
# 2. Input Validation
# 3. Consistent Naming
# 4. Authorization
