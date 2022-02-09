from enum import Enum
from typing import Any, Optional

from flask import jsonify


class ResponseType(Enum):
    SUCCESS = "success"
    ERROR = "error"


def json_response(responseType: ResponseType, data: Any, msg: str = ""):
    return jsonify({
        "status": responseType.value,
        "data": data,
        "msg": msg
    })
