from contants.enums import HTTPStatusCodes
from sanic.response import json
from contants.keys import Keys


async def send_response(data=None, status_code=HTTPStatusCodes.SUCCESS.value,
                        meta=None, body: dict = None, headers=None):
    """
        data: final response data
        status_code: success status code, default is 200
        body: Optional: Response body dict in v4 format.
        headers: Optional : Response headers to be sent to clients.
        {'is_success': True, 'data': data, 'status_code': status_code}
        meta results
    """

    if body is not None:
        return json(body=body, status=body["status_code"])

    data = {"data": data, "is_success": True, "status_code": status_code}
    if meta:
        data["meta"] = meta
    return json(body=data, status=status_code, headers=headers)


async def rectify_payload(data: dict):
    """
        This function removes unwanted parameters to return in response.
    """

    keys_to_remove = Keys.keys_to_remove.value
    new_user_dict = {key: value for key, value in data.items() if
                     key not in keys_to_remove}

    return new_user_dict
