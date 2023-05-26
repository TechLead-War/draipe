from tortoise import fields
from tortoise.models import Model


class Wallet(Model):
    id = fields.BigIntField(pk=True)
    user_id = fields.BigIntField()
    wallet_balance = fields.BigIntField()
    updated_on = fields.BigIntField()
    usable_till = fields.BigIntField()
    wallet_id = fields.BigIntField()


class WalletHistory(Model):
    id = fields.BigIntField(pk=True)
    wallet_id = fields.BigIntField()
    transaction_details = fields.CharField(max_length=255)
    before_balance = fields.BigIntField()
    after_balance = fields.BigIntField()
    order_id = fields.BigIntField()
