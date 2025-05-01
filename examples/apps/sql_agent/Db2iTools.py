import json
from textwrap import dedent
from typing import Any, Dict, List, Literal, Optional, Sequence, Union

from agno.tools.toolkit import Toolkit
from agno.utils.log import log_debug, logger
from mapepire_python import DaemonServer, connect
from pep249 import QueryParameters, ResultRow, ResultSet


def truncate_word(content: Any, *, length: int, suffix: str = "...") -> str:
    """
    Truncate a string to a certain number of words, based on the max string
    length.
    """

    if not isinstance(content, str) or length <= 0:
        return content

    if len(content) <= length:
        return content

    return content[: length - len(suffix)].rsplit(" ", 1)[0] + suffix


class Db2iDatabase:

    def __init__(
        self,
        schema: str,
        server_config: Union[DaemonServer, Dict[str, str]],
        ignore_tables: Optional[List[str]] = None,
        include_tables: Optional[List[str]] = None,
        custom_table_info: Optional[Dict[Any, Any]] = None,
        sampler_rows_in_table_info: int = 3,
        max_string_length: int = 300,
    ):
        self._schema = schema
        self._server_config = server_config
        if include_tables and ignore_tables:
            raise ValueError("Cannot specify both include_tables and ignore_tables")

        self._all_tables = set(list(self._get_all_table_names(schema)))
        self._include_tables = set(include_tables) if include_tables else set()
        if self._include_tables:
            missing_tables = self._include_tables - self._all_tables
            if missing_tables:
                raise ValueError(
                    f"Tables {missing_tables} are not present in the schema {schema}"
                )

        self._ignore_tables = set(ignore_tables) if ignore_tables else set()
        if self._ignore_tables:
            missing_tables = self._ignore_tables - self._all_tables
            if missing_tables:
                raise ValueError(
                    f"Tables {missing_tables} are not present in the schema {schema}"
                )

        self.usable_tables = self.get_usable_table_names()

        self._sample_rows_in_table_info = sampler_rows_in_table_info
        self._customed_table_info = custom_table_info
        self._max_string_length = max_string_length

    @property
    def dialect(self) -> str:
        """Return string representation of dialect to use."""
        return "Db2i"

    def _get_all_table_names(self, schema: str) -> List[str]:
        sql = f"""
            SELECT TABLE_NAME as name, TABLE_TYPE
            FROM QSYS2.SYSTABLES
            WHERE TABLE_SCHEMA = ? AND TABLE_TYPE = 'T'
            ORDER BY TABLE_NAME        
        """

        options = [schema]
        result = self._execute(sql, options=options, fetch="all")
        names = [row["NAME"] for row in result]

        return names

    def _execute(
        self,
        sql: str,
        options: Optional[QueryParameters] = None,
        fetch: Union[Literal["all", "one"], int] = "all",
    ) -> ResultRow | ResultSet | list:
        """Execute SQL query and return data

        Args:
            sql (str): _description_
            options (Optional[QueryParameters], optional): _description_. Defaults to None.
            fetch (Union[Literal[&quot;all&quot;, &quot;one&quot;], int], optional): _description_. Defaults to "all".

        Raises:
            ValueError: _description_

        Returns:
            ResultRow | ResultSet | list: _description_
        """

        with connect(self._server_config) as conn:
            with conn.execute(sql, options) as cursor:
                if cursor.has_results:
                    if fetch == "all":
                        result = cursor.fetchall()
                    elif fetch == "one":
                        result = cursor.fetchone()
                    elif isinstance(fetch, int):
                        result = []
                        for _ in range(fetch):
                            row = cursor.fetchone()
                            if row is None:
                                break
                            result.append(row)
                    else:
                        raise ValueError(f"Invalid fetch value: {fetch}")

                    return result["data"]

        return []

    def run(
        self,
        sql: str,
        options: Optional[QueryParameters] = None,
        include_columns: bool = False,
        fetch: Union[Literal["all", "one"], int] = "all",
    ) -> str | ResultRow | ResultSet | list:
        """Execute a SQL command and return a string representing the results.

        If the statement returns rows, a string of the results is returned.
        If the statement returns no rows, an empty string is returned.
        """
        result = self._execute(sql, options=options, fetch=fetch)

        if fetch == "cursor":
            return result

        res = [
            {
                column: truncate_word(value, length=self._max_string_length)
                for column, value in r.items()
            }
            for r in result
        ]

        if not include_columns:
            res = [tuple(row.values()) for row in res]  # type: ignore[misc]

        if not res:
            return ""
        else:
            return str(res)

    def get_table_info(self, table_names: Optional[List[str]] = None):

        all_table_names = self.get_usable_table_names()
        if table_names is not None:
            missing_tables = set(table_names).difference(all_table_names)
            if missing_tables:
                raise ValueError(
                    f"Tables {missing_tables} are not present in the schema"
                )

            all_table_names = table_names

        tables = []
        for table in all_table_names:
            if self._customed_table_info and table in self._customed_table_info:
                tables.append(self._customed_table_info[table])

            table_definition = self._get_table_definition(table)
            table_info = f"{table_definition.rstrip()}"

            if self._sample_rows_in_table_info:
                table_info += f"\n{self._get_sample_rows(table)}"
            tables.append(table_info)

        final_str = "\n\n".join(tables)
        return final_str

    def _get_sample_rows(self, table: str):

        sql = f"SELECT * FROM {self._schema}.{table} FETCH FIRST {self._sample_rows_in_table_info} ROWS ONLY"

        columns_str = ""
        sample_rows_str = ""
        try:
            result = []
            with connect(self._server_config) as conn:
                with conn.execute(sql) as cursor:
                    if cursor.has_results:
                        res = cursor.fetchall()
                        result = res["data"]

            if result:
                # Get column names as a tab-separated string
                columns_str = "\t".join(result[0].keys())

                # Convert each row to a tab-separated string of values
                rows = []
                for row in result:
                    # Convert all values to strings and join with tabs
                    row_values = []
                    for val in row.values():
                        if val is None:
                            row_values.append("NULL")
                        else:
                            str_val = str(val)
                            if len(str_val) > 100:
                                str_val = str_val[:97] + "..."
                            row_values.append(str_val)

                    rows.append("\t".join(row_values))

                # Join all rows with newlines
                sample_rows_str = "\n".join(rows)

        except Exception as e:
            print(e)
            columns_str = ""
            sample_rows_str = ""

        return (
            f"{self._sample_rows_in_table_info} sample rows from {table}:\n"
            f"{columns_str}\n"
            f"{sample_rows_str}"
        )

    def _get_table_definition(self, table: str) -> str:
        sql = dedent(
            f"""
            CALL QSYS2.GENERATE_SQL(
                DATABASE_OBJECT_NAME => ?,
                DATABASE_OBJECT_LIBRARY_NAME => ?,
                DATABASE_OBJECT_TYPE => 'TABLE',
                CREATE_OR_REPLACE_OPTION => '1',
                PRIVILEGES_OPTION => '0',
                STATEMENT_FORMATTING_OPTION => '0',
                SOURCE_STREAM_FILE_END_OF_LINE => 'LF',
                SOURCE_STREAM_FILE_CCSID => 1208
            )
        """
        )
        result = self._execute(sql, options=[table, self._schema])
        return "\n".join(res["SRCDTA"] for res in result)

    def get_table_info_no_throw(self, table_names: Optional[List[str]] = None) -> str:
        """Get information about specified tables.

        Follows best practices as specified in: Rajkumar et al, 2022
        (https://arxiv.org/abs/2204.00498)

        If `sample_rows_in_table_info`, the specified number of sample rows will be
        appended to each table description. This can increase performance as
        demonstrated in the paper.
        """
        try:
            return self.get_table_info(table_names)
        except ValueError as e:
            """Format the error message"""
            return f"Error: {e}"

    def get_table_names(self):
        return self.get_usable_table_names()

    def get_usable_table_names(self):
        if self._include_tables:
            return sorted(self._include_tables)
        return sorted(self._all_tables - self._ignore_tables)

    def run_no_throw(
        self,
        sql: str,
        include_columns: bool = False,
        fetch: Literal["all", "one"] = "all",
        parameters: Optional[Dict[str, Any]] = None,
    ) -> ResultRow | str | ResultSet | list:
        """Execute a SQL command and return a string representing the results.

        If the statement returns rows, a string of the results is returned.
        If the statement returns no rows, an empty string is returned.

        If the statement throws an error, the error message is returned.
        """
        try:
            return self.run(
                sql, options=parameters, fetch=fetch, include_columns=include_columns
            )
        except Exception as e:
            """Format the error message"""
            return f"Error: {e}"

    def get_context(self) -> Dict[str, Any]:
        """Return db context that you may want in agent prompt."""
        table_names = list(self.get_usable_table_names())
        table_info = self.get_table_info_no_throw()
        return {"table_info": table_info, "table_names": ", ".join(table_names)}


class Db2iTools(Toolkit):
    """
    Db2iTools is a Toolkit for DB2 for i databases.
    This class provides SQL-related functionality specifically designed for DB2i systems.
    """

    def __init__(
        self,
        schema: str,
        server_config: Union[DaemonServer, Dict[str, str]],
        ignore_tables: Optional[List[str]] = None,
        include_tables: Optional[List[str]] = None,
        custom_table_info: Optional[Dict[Any, Any]] = None,
        sampler_rows_in_table_info: int = 3,
        max_string_length: int = 300,
        list_tables: bool = True,
        describe_table: bool = True,
        run_sql_query: bool = True,
        name: str = "db2i_tools",
        instructions: Optional[str] = None,
        add_instructions: bool = True,
        cache_results: bool = False,
        cache_ttl: int = 3600,
        cache_dir: Optional[str] = None,
    ):
        """
        Initialize Db2iTools with the Db2iDatabase instance.

        Args:
            schema: The DB2 schema name
            server_config: Configuration for the DB2 server connection
            ignore_tables: Optional list of tables to ignore
            include_tables: Optional list of tables to include (if specified, only these tables will be used)
            custom_table_info: Optional custom table information
            sampler_rows_in_table_info: Number of sample rows to include in table info
            max_string_length: Maximum length of strings in results
            list_tables: Whether to register the list_tables function
            describe_table: Whether to register the describe_table function
            run_sql_query: Whether to register the run_sql_query function
            name: A descriptive name for the toolkit
            instructions: Instructions for the toolkit
            add_instructions: Whether to add instructions to the toolkit
            cache_results: Enable in-memory caching of function results
            cache_ttl: Time-to-live for cached results in seconds
            cache_dir: Directory to store cache files
        """
        # Default DB2i instructions if none provided
        if not instructions:
            instructions = dedent(
                """\
                Use these tools to interact with DB2 for IBM i database systems.
                - Use list_tables() to get a list of available tables
                - Use describe_table(table_name) to get schema and sample data for a table
                - Use run_sql_query(query, limit) to execute SQL queries
                
                DB2 for i specific notes:
                - Use FETCH FIRST n ROWS ONLY instead of LIMIT for pagination
                - Use proper DB2i functions for date handling and string operations
                - Always use schema-qualified table names (SCHEMA.TABLE)
            """
            )

        # Initialize the Toolkit parent class
        super().__init__(
            name=name,
            instructions=instructions,
            add_instructions=add_instructions,
            cache_results=cache_results,
            cache_ttl=cache_ttl,
            cache_dir=cache_dir,
        )

        # Create the Db2iDatabase instance
        self.db2i_database = Db2iDatabase(
            schema=schema,
            server_config=server_config,
            ignore_tables=ignore_tables,
            include_tables=include_tables,
            custom_table_info=custom_table_info,
            sampler_rows_in_table_info=sampler_rows_in_table_info,
            max_string_length=max_string_length,
        )

        # Register the functions based on flags
        if list_tables:
            self.register(self.list_tables)
        if describe_table:
            self.register(self.describe_table)
        if run_sql_query:
            self.register(self.run_sql_query)

    def list_tables(self) -> str:
        """Use this function to get a list of table names in the database.

        Returns:
            str: list of tables in the database.
        """
        try:
            log_debug("listing tables in the Db2i database")
            table_names = self.db2i_database.get_usable_table_names()
            log_debug(f"table_names: {table_names}")
            return json.dumps(table_names)
        except Exception as e:
            logger.error(f"Error getting tables: {e}")
            return f"Error getting tables: {e}"

    def describe_table(self, table_name: str) -> str:
        """Use this function to describe a table.

        Args:
            table_name (str): The name of the table to get the schema for.

        Returns:
            str: schema of a table
        """
        try:
            log_debug(f"Describing table: {table_name}")
            table_info = self.db2i_database.get_table_info_no_throw([table_name])
            return table_info
        except Exception as e:
            logger.error(f"Error getting table schema: {e}")
            return f"Error getting table schema: {e}"

    def run_sql_query(self, query: str, limit: Optional[int] = 10) -> str:
        """Use this function to run a SQL query and return the result.

        Args:
            query (str): The query to run.
            limit (int, optional): The number of rows to return. Defaults to 10. Use `None` to show all results.
        Returns:
            str: Result of the SQL query.
        Notes:
            - The result may be empty if the query does not return any data.
        """
        try:
            log_debug(f"Running SQL query on Db2i: {query}")
            if limit is not None:
                # Add FETCH FIRST n ROWS ONLY if limit is provided and query doesn't already have it
                if "FETCH FIRST" not in query.upper() and "LIMIT" not in query.upper():
                    query = f"{query.rstrip(';')} FETCH FIRST {limit} ROWS ONLY"

            result = self.db2i_database.run_no_throw(query, include_columns=True)
            return str(result)
        except Exception as e:
            logger.error(f"Error running query: {e}")
            return f"Error running query: {e}"
