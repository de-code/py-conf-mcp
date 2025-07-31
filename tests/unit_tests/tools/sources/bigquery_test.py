from typing import Iterator
from unittest.mock import ANY, MagicMock, patch

import pytest

from py_conf_mcp.tools.sources import bigquery
from py_conf_mcp.tools.sources.bigquery import BigQueryTool, toquoted
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


class TestToQuoted:
    def test_should_fail_if_none(self):
        with pytest.raises(ValueError):
            toquoted(None)  # type: ignore

    def test_should_add_single_quotes(self):
        assert toquoted('test') == "'test'"

    def test_should_escape_single_quotes(self):
        assert toquoted('t\'est') == "'t\\'est'"


class TestBigQueryTool:
    def test_should_call_iter_dict_from_bq_query(
        self,
        iter_dict_from_bq_query_mock: MagicMock
    ):
        tool = BigQueryTool(
            project_name=PROJECT_NAME_1,
            sql_query=SQL_QUERY_1,
            is_sql_query_template=False
        )
        tool()
        iter_dict_from_bq_query_mock.assert_called_with(
            project_name=PROJECT_NAME_1,
            query=SQL_QUERY_1
        )

    def test_should_replace_placeholders_in_sql_query(
        self,
        iter_dict_from_bq_query_mock: MagicMock
    ):
        tool = BigQueryTool(
            project_name=PROJECT_NAME_1,
            sql_query='SELECT {{ param_1 }}',
            is_sql_query_template=True
        )
        tool(param_1='value_1')
        iter_dict_from_bq_query_mock.assert_called_with(
            project_name=ANY,
            query='SELECT value_1'
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
