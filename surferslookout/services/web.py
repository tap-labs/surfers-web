import json
from urllib.request import urlopen
from flask import current_app as app


def get(url) -> json:
    app.logger.info(f"Reading API Get: {url}")

    with urlopen(url) as _response:
        _data = _response.read()

    _item = json.loads(_data)
    return _item

