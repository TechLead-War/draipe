from contants.enums import UserStatus, DeactivationReasons
from tortoise import Model, fields


class Users(Model):
    serializable_keys = {
        "id",
        "first_name",
        "last_name",
        "created_on",
        "updated_on",
        "email",
        "dob",
        "number",
        "number_code",
        "gender",
        "metadata",
        "status",
        "username",
        "premium_user",
        "premium_buy_on",
        "reference_id",
        "password",
        "deactivation_reason"
        "profile_picture",
        "address_id",
        "is_email_verified",
        "is_number_verified",
        "is_loyal_customer",
        "cart_id",
        "referral_id"
    }

    id = fields.UUIDField(pk=True, dump_only=True)
    first_name = fields.CharField(max_length=50)
    last_name = fields.CharField(max_length=50)
    created_on = fields.DatetimeField(auto_now_add=True)
    updated_on = fields.DatetimeField(null=True)
    email = fields.CharField(max_length=50, collation='NOCASE', unique=True)
    dob = fields.DateField(null=False)
    number = fields.CharField(index=True, max_length=10, null=False)
    number_code = fields.CharField(max_length=3)
    gender = fields.CharField(max_length=1, null=False, collation='NOCASE')
    # metadata = fields.JSONField(null=True)
    status = fields.CharField(max_length=10, default=UserStatus.ACTIVE.value)
    username = fields.CharField(max_length=50, null=True)
    # we'll generate - "some_keyword" + firstname + secondname + some_id
    premium_user = fields.BooleanField(default=False)
    premium_buy_on = fields.DatetimeField(null=True)
    reference_id = fields.TextField(default=True)
    password = fields.CharField(max_length=500, null=False)
    deactivation_reason = fields.CharField(
        max_length=50, default=DeactivationReasons.NOT_DEACTIVATED.value
    )
    profile_picture = fields.CharField(max_length=255)
    address_id = fields.TextField()
    is_email_verified = fields.BigIntField()
    is_number_verified = fields.BigIntField()
    is_loyal_customer = fields.BigIntField()
    cart_id = fields.BigIntField()
    referral_id = fields.CharField(max_length=255)


class UserAddress(Model):
    id = fields.BigIntField(pk=True)
    user_id = fields.BigIntField()
    full_name = fields.CharField(max_length=255)
    mobile_number = fields.BigIntField()
    pin_code = fields.BigIntField()
    house_number = fields.CharField(max_length=255)
    area = fields.CharField(max_length=255)
    landmark = fields.CharField(max_length=255)
    city = fields.CharField(max_length=255)
    state = fields.CharField(max_length=255)
    country = fields.CharField(max_length=255)

