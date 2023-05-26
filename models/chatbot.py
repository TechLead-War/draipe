from tortoise import fields
from tortoise.models import Model


class Review(Model):
    id = fields.BigIntField(pk=True)
    user_id = fields.BigIntField()
    product_id = fields.BigIntField()
    order_id = fields.BigIntField()
    rating = fields.SmallIntField()
    comment = fields.TextField()
    product_images = fields.JSONField()
    created_on = fields.DateField()


class Chatbot(Model):
    id = fields.BigIntField(pk=True)


class Analysis(Model):
    id = fields.BigIntField(pk=True)
    page_id = fields.BigIntField()
    visited_count = fields.BigIntField()
    buyed_counter = fields.BigIntField()
    age_group = fields.BigIntField()
    famous_from = fields.BigIntField()
    published_in = fields.BigIntField()
