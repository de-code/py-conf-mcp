from abc import ABC, abstractmethod
from dataclasses import dataclass
import importlib
import inspect
import logging
from typing import Any, Callable, Mapping, Optional, Sequence

from py_conf_mcp.config import (
    FromPythonFunctionConfig,
    ToolDefinitionsConfig
)


LOGGER = logging.getLogger(__name__)


@dataclass(frozen=True)
class Tool:
    tool_fn: Callable
    name: str
    description: Optional[str] = None


class ToolResolver(ABC):
    @abstractmethod
    def get_tool_by_name(self, tool_name: str) -> Tool:
        pass

    def get_tools_by_name(
        self,
        tool_names: Sequence[str]
    ) -> Sequence[Tool]:
        return [
            self.get_tool_by_name(tool_name)
            for tool_name in tool_names
        ]


class InvalidToolNameError(KeyError):
    pass


def get_tool_from_tool_class(
    tool_class: type[Tool],
    init_parameters: Mapping[str, Any],
    available_kwargs: Mapping[str, Any]
) -> Tool:
    parameters = inspect.signature(tool_class).parameters
    LOGGER.info('tool_class: %r, parameters: %r', tool_class, parameters)
    extra_kwargs = {
        key: value
        for key, value in available_kwargs.items()
        if key in parameters and key not in init_parameters
    }
    return tool_class(**init_parameters, **extra_kwargs)


def get_tool_from_python_tool_instance(
    config: FromPythonFunctionConfig
) -> Tool:
    tool_module = importlib.import_module(config.module)
    tool = getattr(tool_module, config.key)
    assert callable(tool)
    return Tool(
        tool_fn=tool,
        name=config.name,
        description=config.description
    )


@dataclass(frozen=True)
class ConfigToolResolver(ToolResolver):
    tool_definitions_config: ToolDefinitionsConfig

    def get_tool_by_name(self, tool_name: str) -> Tool:
        for from_python_tool_instance_config in (
            self.tool_definitions_config.from_python_function
        ):
            if from_python_tool_instance_config.name == tool_name:
                return get_tool_from_python_tool_instance(from_python_tool_instance_config)
        raise InvalidToolNameError(f'Unrecognised tool: {repr(tool_name)}')
