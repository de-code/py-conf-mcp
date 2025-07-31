from typing import Iterator
from unittest.mock import MagicMock, patch

import pytest

from py_conf_mcp.tools.sources import bigquery
from py_conf_mcp.tools.sources.bigquery import BigQueryTool
from py_conf_mcp.utils.json import get_json_as_csv_lines


PROJECT_NAME_1 = 'project_name_1'

SQL_QUERY_1 = 'sql_query_1'

ROW_1 = {'column_1': 'value_1'}


@pytest.fixture(name='bigquery_mock', autouse=True)
def _bigquery_mock() -> Iterator[MagicMock]:
    with patch.object(bigquery, 'bigquery') as mock:
        yield mock


@pytest.fixture(name='iter_dict_from_bq_query_mock')
def _iter_dict_from_bq_query_mock() -> Iterator[MagicMock]:
    with patch.object(bigquery, 'iter_dict_from_bq_query') as mock:
        yield mock


@pytest.fixture(name='get_json_as_csv_lines_mock')
def _get_json_as_csv_lines_mock() -> Iterator[MagicMock]:
    with patch.object(bigquery, 'get_json_as_csv_lines') as mock:
        yield mock


class TestBigQueryTool:
    def test_should_call_iter_dict_from_bq_query(
        self,
        iter_dict_from_bq_query_mock: MagicMock
    ):
        tool = BigQueryTool(
            project_name=PROJECT_NAME_1,
            sql_query=SQL_QUERY_1
        )
        tool()
        iter_dict_from_bq_query_mock.assert_called_with(
            project_name=PROJECT_NAME_1,
            query=SQL_QUERY_1
        )

    def test_should_return_query_results_as_json(
        self,
        iter_dict_from_bq_query_mock: MagicMock
    ):
        tool = BigQueryTool(
            project_name=PROJECT_NAME_1,
            sql_query=SQL_QUERY_1
        )
        iter_dict_from_bq_query_mock.return_value = iter([ROW_1])
        assert tool() == [ROW_1]

    def test_should_return_query_results_as_csv(
        self,
        iter_dict_from_bq_query_mock: MagicMock
    ):
        tool = BigQueryTool(
            project_name=PROJECT_NAME_1,
            sql_query=SQL_QUERY_1,
            output_format='csv'
        )
        iter_dict_from_bq_query_mock.return_value = iter([ROW_1])
        assert tool() == '\n'.join(list(get_json_as_csv_lines([ROW_1])))
