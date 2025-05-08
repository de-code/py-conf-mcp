import logging
from typing import Mapping, Optional

import requests

from py_conf_mcp.tools.typing import ToolClass


LOGGER = logging.getLogger(__name__)


def get_requests_session() -> requests.Session:
    return requests.Session()


class WebApiTool(ToolClass):
    def __init__(
        self,
        url: str,
        query_parameters: Optional[Mapping[str, str]] = None,
        headers: Optional[Mapping[str, str]] = None,
        method: str = 'GET'
    ):
        super().__init__()
        self.url = url
        self.query_parameters = query_parameters or {}
        self.method = method
        self.headers = headers

    def __call__(self):
        session = get_requests_session()
        url = self.url
        params = self.query_parameters
        LOGGER.info('url: %r (method: %r, params: %r)', url, self.method, params)
        response = session.request(
            method=self.method,
            url=url,
            params=params,
            headers=self.headers
        )
        response.raise_for_status()
        response_json = response.json()
        LOGGER.info('response_json: %r', response_json)
        return response_json
