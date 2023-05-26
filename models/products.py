from tortoise import fields
from tortoise.models import Model


class Product(Model):
    id = fields.BigIntField(pk=True)
    sku_name = fields.CharField(max_length=255)
    description = fields.TextField()
    unit_price = fields.BigIntField()
    quantity = fields.BigIntField()
    average_rating = fields.SmallIntField()
    images = fields.JSONField()
    created_on = fields.BigIntField()
    updated_on = fields.BigIntField()
    sku_id = fields.BigIntField()
    sku_description = fields.BigIntField()
    available_size = fields.BigIntField()
    available_colors = fields.BigIntField()
    size = fields.BigIntField()
    color = fields.BigIntField()
    product_available = fields.BigIntField()
    keyword_id = fields.BigIntField()
    meta_data = fields.BigIntField()


class OrderLayer(Model):
    id = fields.BigIntField(pk=True)
    order_id = fields.BigIntField()
    product_id = fields.BigIntField()
    quantity = fields.SmallIntField()
    item_size = fields.SmallIntField()


class Transaction(Model):
    id = fields.BigIntField(pk=True)
    user_id = fields.BigIntField()
    order_id = fields.BigIntField()
    order_value = fields.BigIntField()
    status = fields.BigIntField()
    discount_applied = fields.BigIntField()


class Cart(Model):
    id = fields.BigIntField(pk=True)
    user_id = fields.BigIntField()
    cart_layer_id = fields.BigIntField()


class Order(Model):
    id = fields.BigIntField(pk=True)
    order_id = fields.CharField(max_length=255)
    user_id = fields.BigIntField()
    order_status = fields.CharField(max_length=255)
    order_subtotal = fields.BigIntField()
    tracking_url = fields.CharField(max_length=255)
    shipped_address_id = fields.BigIntField()
    payment_mode = fields.CharField(max_length=255)
    created_on = fields.DateField()
    updated_on = fields.DateField()
    actual_price = fields.JSONField()
    discount_given = fields.BigIntField()
    final_price = fields.BigIntField()


class Search(Model):
    id = fields.BigIntField(pk=True)
    keyword_id = fields.BigIntField()
    search_word = fields.BigIntField()


class CartLayer(Model):
    id = fields.BigIntField(pk=True)
    product_id = fields.BigIntField()
