from typing import NotRequired, Sequence, TypedDict


class FromPythonFunctionConfigDict(TypedDict):
    name: str
    module: str
    key: str
    description: NotRequired[str]


class ToolDefinitionsConfigDict(TypedDict):
    fromPythonFunction: NotRequired[Sequence[FromPythonFunctionConfigDict]]


class ServerConfigDict(TypedDict):
    name: str
    tools: Sequence[str]


class AppConfigDict(TypedDict):
    toolDefinitions: NotRequired[ToolDefinitionsConfigDict]
    server: ServerConfigDict
