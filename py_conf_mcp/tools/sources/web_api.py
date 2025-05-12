import logging
from typing import Any, Mapping, Optional

import jinja2
import requests

from py_conf_mcp.tools.typing import ToolClass


LOGGER = logging.getLogger(__name__)


def get_requests_session() -> requests.Session:
    return requests.Session()


def get_evaluated_template(template: str, variables: Mapping[str, Any]) -> Any:
    compiled_template = jinja2.Template(template)
    return compiled_template.render(variables)


def get_evaluated_query_parameters(
    query_parameters: Mapping[str, Any],
    variables: Mapping[str, Any]
) -> Mapping[str, Any]:
    return {
        key: get_evaluated_template(value, variables)
        for key, value in query_parameters.items()
    }


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

    def __call__(self, **kwargs):
        session = get_requests_session()
        url = get_evaluated_template(self.url, kwargs)
        params = get_evaluated_query_parameters(
            self.query_parameters,
            kwargs
        )
        LOGGER.info(
            'url: %r (method: %r, params: %r, kwargs: %r)',
            url, self.method, params, kwargs
        )
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
