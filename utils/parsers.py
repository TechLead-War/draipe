from datetime import date, datetime
from uuid import UUID as base_uuid

from asyncpg.pgproto.pgproto import UUID
from sanic.response import json

from contants.enums import HTTPStatusCodes
from contants.keys import Keys


async def send_response(data=None, status_code=HTTPStatusCodes.SUCCESS.value,
                   meta=None, body: dict = None, headers=None, purge_response_keys=False):
    """
    :param data: final response data
    :param status_code: success status code, default is 200
    :param body: Optional: Response body dict in v4 format.
    :param headers: Optional : Response headers to be sent to clients.
    :param purge_response_keys: Optional : Converts response into dict
    :return {'is_success': True, 'data': data, 'status_code': status_code}
    :param meta results
    """
    if body is not None:
        return json(body=body, status=body["status_code"])

    status_code = status_code
    data = {"data": data, "is_success": True, "status_code": status_code}
    if meta:
        data["meta"] = meta
    if purge_response_keys:
        return data
    return json(body=data, status=status_code, headers=headers)


async def rectify_payload(data: dict):
    """
        This function removes unwanted parameters to return in response.
    """

    keys_to_remove = Keys.keys_to_remove.value
    new_user_dict = {key: value for key, value in data.items() if
                     key not in keys_to_remove}

    return new_user_dict


def to_string(result):
    for key in result:
        if type(result[key]) == datetime:
            result[key] = str(result[key])
        if type(result[key]) == date:
            result[key] = str(result[key])
        if type(result[key]) == UUID:
            result[key] = str(result[key])
        if type(result[key]) == bool:
            result[key] = str(result[key])
        if type(result[key]) == base_uuid:
            result[key] = str(result[key])
    return result
