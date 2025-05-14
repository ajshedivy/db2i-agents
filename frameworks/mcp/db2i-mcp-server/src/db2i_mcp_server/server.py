from datetime import datetime
import os
import argparse
from textwrap import dedent
from typing import Any, Dict, List, Literal, Optional, Union

from dotenv import load_dotenv
from mcp.server.models import InitializationOptions
import mcp.types as types
from mcp.server import NotificationOptions, Server
from pep249 import QueryParameters, ResultRow, ResultSet
from pydantic import AnyUrl
import mcp.server.stdio
from pathlib import Path

from mapepire_python.data_types import DaemonServer
from mapepire_python import connect, Connection

import logging

SERVER = "db2i-mcp-server"

QUERY_PROMPT = """
You are a Db2 for IBM i expert focused on writing efficient, accuracte SQL queries.

When a user messages you, determine if you need to query the database or respond directly. If you can respond directly, do so.

If you need to access the database to answer the user's question, you can use the following tools:
- `list-usable-tables`: List the usable tables in the schema. This tool should be called before running any other tool.
- `describe-table`: Describe a specific table including its columns and sample rows. This tool should be called after list-usable-tables.
- `run-sql-query`: Run a valid Db2 for i SQL query. This tool should be called after list-usable-tables and describe-table.

Follow these steps to answer the user's question:
1. First, indentify the tables that the user has access to. use the `list-usable-tables` tool to get the list of usable tables in the schema.
    - This should ALWAYS be the first tool call. 
2. Then, think step-by-step about the query construction process, don't rush this step
3. Follow a chain of thought approach before writing the SQL query, ask clarifying questions where needed.
4. Based on the user's question, determine if you need to describe any tables. If so, use the `describe-table` tool to get the table definition and sample rows.
    - decribe multiple tables if needed to get a better understanding of the data.
5. Then, using all the information about the tables, create a single syntactically correct Db2 for i SQL query to accomplish the task.
6. If you need to join tables, check the table definitions for foreign keys and constraints to determine the relationships between the tables.
    - ONLY join tables for which you have table definitions. If you do not have a table definition, call `describe-table` to get the table definition.
    - If the table definition has a foreign key to another table, use that to join the tables.
    - If you cannot find a relationship in the table definitions, only join on the columns that have the same name and data type.
    - If you cannot find a valid relationship, ask the user to provide the column name to join.
7. If you cannot find relevant tables, columns or relationships, stop and ask the user for more information.
8. Once you have a syntactically correct SQL query, use the `run-sql-query` tool to execute the query.
9. When running a query:
    - Do not add `;` at the end of the query.
    - Always provide a `LIMIT` clause to limit the number of rows returned, unless the user explicitly asks for all results.
    - Always reference tables with SCHMEA.TABLE_NAME format. 
10. After you run the query, analyse the results and return the answer in markdown format.
12. Always show the user the SQL you ran to get the answer.
13. Continue till you have accomplished the task.
14. Show results as a table or a chart if possible.

After finishing your task, ask the user relevant followup questions like "was the result okay, would you like me to fix any problems?"
If the user says yes, get the previous query fix the problems.
If the user wants to see the SQL, get it from the previous message. 

Finally, here are a set of rules you MUST follow:
<rules>
- All SQL queries must be syntactically correct and valid for Db2 for i.
- All SQL queries must use a valid table reference format (SCHEMA.TABLE_NAME).
- Always call `describe-table` before creating and running a query.
- Make sure your query accounts for duplicate records.
- Make sure your query accounts for null values.
- If you run a query, explain why you ran it.
- **NEVER, EVER RUN CODE TO DELETE DATA OR ABUSE THE LOCAL SYSTEM.**
- **Always use valid column references from the table definitions.**
- ** DO NOT HALLUCINATE TABLES, COLUMNS OR DATA**
</rules>
"""


# Initialize empty notes dictionary for the server
notes: Dict[str, str] = {}
class NoOpLogger:
    """A no-operation logger that silently ignores all logging calls."""
    
    def debug(self, msg, *args, **kwargs): pass
    def info(self, msg, *args, **kwargs): pass
    def warning(self, msg, *args, **kwargs): pass
    def error(self, msg, *args, **kwargs): pass
    def critical(self, msg, *args, **kwargs): pass
    def exception(self, msg, *args, **kwargs): pass

# Singleton instance of NoOpLogger
NO_OP_LOGGER = NoOpLogger()

def configure_logging():
    """
    Configure logging for the MCP server with a simplified approach.
    Redirects stdout to avoid interfering with MCP communication.
    
    Environment variables:
    - ENABLE_LOGGING: Set to "false" to disable all logging
    - LOG_LEVEL: Set to DEBUG, INFO, WARNING, ERROR, or CRITICAL (default: INFO)
    
    Returns:
        A logger instance that will properly handle log messages (either real logger or no-op)
    """
    # Check if logging is enabled
    logging_enabled = os.environ.get("ENABLE_LOGGING", "true").lower() != "false"
    
    if not logging_enabled:
        return NO_OP_LOGGER
    
    # Set up log file path
    log_directory = os.path.join(Path.home(), ".mcp", "logs")
    os.makedirs(log_directory, exist_ok=True)
    log_filename = os.path.join(
        log_directory, f'db2i_mcp_server_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'
    )
    
    # Get log level from environment
    log_level_name = os.environ.get("LOG_LEVEL", "INFO").upper()
    log_level = getattr(logging, log_level_name, logging.INFO)
    
    # Clear any existing handlers from the root logger
    root_logger = logging.getLogger()
    root_logger.handlers = []
    
    # Configure logging to file with basicConfig
    logging.basicConfig(
        filename=log_filename,
        filemode='w',
        format='%(asctime)s %(levelname)s [%(name)s:%(funcName)s:%(lineno)d] %(message)s',
        level=logging.DEBUG
    )
    
    # Get our specific logger
    logger = logging.getLogger("db2i_mcp_server")
    
    # Log startup info
    logger.info(f"Starting Db2i MCP Server (log level: {log_level_name})")
    logger.info(f"Logs location: {log_filename}")
    
    return logger


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

        self.connection: Optional[Connection] = None
        self.is_connected = False

        if include_tables and ignore_tables:
            raise ValueError("Cannot specify both include_tables and ignore_tables")

        self._schema = schema
        self._server_config = server_config
        self._include_tables = include_tables
        self._ignore_tables = ignore_tables
        self._all_tables: Optional[set[str]] = None  # Will be populated in get_usable_table_names

        self._sample_rows_in_table_info = sampler_rows_in_table_info
        self._customed_table_info = custom_table_info
        self._max_string_length = max_string_length
        
        self.logger = configure_logging()
        
    def _get_server_config(self) -> Dict[str, str]:
        server_config_dict = {}
        if isinstance(self._server_config, DaemonServer):
            # Extract attributes from DaemonServer instance
            for attr in ["host", "port", "user", "password"]:
                if hasattr(self._server_config, attr):
                    server_config_dict[attr] = getattr(self._server_config, attr)
        else:
            server_config_dict = dict(self._server_config)
        
        return server_config_dict

    def _connect(self) -> Connection:
        """Set up any connections required by the handler

        Should return connection

        """
        server_config_dict = self._get_server_config()
        
        if not all(
            key in server_config_dict for key in ["host", "port", "user", "password"]
        ):
            raise ValueError(
                "Required parameters (host, user, password, port) must be provided."
            )

        try:
            if isinstance(self._server_config, DaemonServer):
                # Use the instance directly
                connect_args = self._server_config
            else:
                # Create a new instance
                connect_args = DaemonServer(
                    host=str(server_config_dict["host"]),
                    port=int(server_config_dict["port"]) if isinstance(server_config_dict["port"], str) else server_config_dict["port"],
                    user=str(server_config_dict["user"]),
                    password=str(server_config_dict["password"]),
                    ignoreUnauthorized=True,
                )

            self.connection = connect(connect_args)
            self.is_connected = True
            self.connection.execute(f"SET CURRENT SCHEMA = '{self._schema}'")
            return self.connection
        except Exception as e:
            host = server_config_dict.get('host', 'unknown')
            self.logger.error(f"Error while connect to {host}, {e}")
            raise

    def _get_all_table_names(self, schema: str) -> List[str]:
        sql = f"""
            SELECT TABLE_NAME as name, TABLE_TYPE
            FROM QSYS2.SYSTABLES
            WHERE TABLE_SCHEMA = ? AND TABLE_TYPE = 'T'
            ORDER BY TABLE_NAME        
        """

        options = [schema]
        result = self._execute(sql, options=options, fetch="all")
        
        # Handle the possible types of result
        if not result:
            return []
            
        names = []
        for row in result:
            if isinstance(row, dict) and "NAME" in row:
                names.append(row["NAME"])
        
        return names

    def _execute(
        self,
        sql: str,
        options: Optional[QueryParameters] = None,
        fetch: Union[Literal["all", "one"], int] = "all",
    ) -> ResultRow | ResultSet | list:
        """Execute SQL query and return data

        Args:
            sql (str): SQL query to execute
            options (Optional[QueryParameters], optional): Query parameters. Defaults to None.
            fetch (Union[Literal["all", "one"], int], optional): Fetch mode. Defaults to "all".

        Raises:
            ValueError: When SQL is invalid or not a SELECT statement

        Returns:
            ResultRow | ResultSet | list: Query results
        """
        # Log query details (truncate long queries)
        self.logger.debug(f"SQL: {sql[:200]}{'...' if len(sql) > 200 else ''} | Params: {options} | Fetch: {fetch}")

        # Remove trailing semicolon
        if sql.endswith(";"):
            sql = sql[:-1]

        # Only allow SELECT statements
        if sql.strip().upper().startswith(("INSERT", "UPDATE", "DELETE", "CREATE", "ALTER", "DROP")):
            self.logger.warning(f"Rejected non-SELECT query: {sql[:50]}...")
            raise ValueError("Only SELECT statements are allowed")

        conn = None
        safe_config = {}
        try:
            # Get server config
            server_config_dict = self._get_server_config()
            
            # mask password in logs    
            safe_config = {k: (v if k != "password" else "***REDACTED***") for k, v in server_config_dict.items()}
            conn = self._connect()
            # Connect and execute
            host = safe_config.get('host', 'unknown') if isinstance(safe_config, dict) else 'unknown'
            self.logger.info(f"Connected to DB ({host})")
            with conn.execute(sql, options) as cursor:
                if not cursor.has_results:
                    self.logger.debug("Query returned no results")
                    return []
                
                # Handle different fetch modes
                if fetch == "all":
                    result = cursor.fetchall()
                    # Properly handle result structure
                    if isinstance(result, dict) and 'data' in result:
                        data = result.get('data', [])
                        row_count = len(data)
                        self.logger.debug(f"Fetched all rows: {row_count}")
                        return data
                    elif isinstance(result, list):
                        self.logger.debug(f"Fetched all rows: {len(result)}")
                        return result
                    return []
                    
                elif fetch == "one":
                    result = cursor.fetchone()
                    self.logger.debug(f"Fetched one row: {'Found' if result else 'None'}")
                    return result if result is not None else []
                    
                elif isinstance(fetch, int):
                    result = []
                    for i in range(fetch):
                        row = cursor.fetchone()
                        if not row:
                            break
                        result.append(row)
                    self.logger.debug(f"Fetched {len(result)}/{fetch} rows")
                    return result
                    
                else:
                    raise ValueError(f"Invalid fetch value: {fetch}")

                
        except Exception as e:
            error_type = type(e).__name__
            self.logger.error(f"{error_type}: {str(e)}")
            if "connection" in error_type.lower() and safe_config:
                self.logger.debug(f"Connection details: {safe_config}")
            raise
        
        finally:
            if conn:
                conn.close()
            
        # This line should never be reached
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

        res = []
        for r in result:
            if isinstance(r, dict):
                res.append({
                    column: truncate_word(value, length=self._max_string_length)
                    for column, value in r.items()
                })
            else:
                # Handle non-dictionary results
                if self.logger:
                    self.logger.warning(f"Unexpected result type in run: {type(r)}")
                res.append(r)

        if not include_columns:
            # Handle different row types
            transformed_res = []
            for row in res:
                if isinstance(row, dict):
                    transformed_res.append(tuple(row.values()))
                else:
                    # Handle non-dict rows
                    transformed_res.append(row)
            res = transformed_res

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
            # Use our connection method which already handles both types correctly
            conn = self._connect()
            with conn:
                with conn.execute(sql) as cursor:
                    if cursor.has_results:
                        res = cursor.fetchall()
                        # Handle different result structures
                        if isinstance(res, dict) and 'data' in res:
                            result = res.get('data', [])
                        elif isinstance(res, list):
                            result = res

            rows = []
            if result and isinstance(result, list) and len(result) > 0:
                # Process rows if they're dictionaries
                first_row = result[0]
                if isinstance(first_row, dict):
                    # Get column names as a tab-separated string
                    columns_str = "\t".join(first_row.keys())

                    # Convert each row to a tab-separated string of values
                    for row in result:
                        if isinstance(row, dict):
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

            # Join all rows with newlines (even if empty)
            sample_rows_str = "\n".join(rows)

        except Exception as e:
            self.logger.error(f"Error getting sample rows: {str(e)}")
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
        if not result:
            return ""
            
        # Handle the result which could be a list of dictionaries
        if isinstance(result, list):
            # Build the result string safely
            result_strings = []
            for res in result:
                if isinstance(res, dict):
                    # Use dictionary get() method for dictionaries
                    src_data = res.get("SRCDTA", "")
                    result_strings.append(str(src_data))
            return "\n".join(result_strings)
        return ""

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

    def get_usable_table_names(self):
        """Get the list of usable table names based on include_tables and ignore_tables"""

        
        try:
            # Return cached tables if already loaded
            if self._all_tables is not None:
                return sorted(self._all_tables)
            else:
                self.logger.info(f"Loading tables from schema: {self._schema}")
                self._all_tables = set(self._get_all_table_names(self._schema))
                self.logger.debug(f"Found {len(self._all_tables)} tables in schema")

                # Apply table filters
                result_tables = self._all_tables
                
                # Check for conflicting options
                if self._include_tables and self._ignore_tables:
                    self.logger.warning("Both include_tables and ignore_tables specified; using include_tables")
                    
                # Filter by included tables
                if self._include_tables:
                    include_set = set(self._include_tables)
                    missing_tables = include_set - self._all_tables
                    if missing_tables:
                        self.logger.warning(f"Tables not found in schema: {missing_tables}")
                    result_tables = self._all_tables.intersection(include_set)
                    self.logger.debug(f"Filtered to {len(result_tables)} included tables")
                    
                # Filter by ignored tables
                elif self._ignore_tables:
                    ignore_set = set(self._ignore_tables)
                    result_tables = self._all_tables - ignore_set
                    self.logger.debug(f"Filtered to {len(result_tables)} tables (after ignoring {len(ignore_set)})")
                
                return sorted(result_tables)
            
        except Exception as e:
            self.logger.error(f"Error getting tables: {type(e).__name__}: {str(e)}")
            return []

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
            # Convert parameters to the right QueryParameters type if needed
            query_params: Optional[QueryParameters] = None
            if parameters:
                if isinstance(parameters, list):
                    query_params = parameters
                elif isinstance(parameters, dict):
                    # Convert dict to list (simple approach)
                    query_params = list(parameters.values())
                
            return self.run(
                sql, options=query_params, fetch=fetch, include_columns=include_columns
            )
        except Exception as e:
            """Format the error message"""
            return f"Error: {e}"


async def main():
    # Load environment variables
    load_dotenv()
    parser = argparse.ArgumentParser(description="Db2i MCP Server")
    parser.add_argument("--use-env", action="store_true", help="Use environment variables for configuration")
    parser.add_argument("--host", type=str, help="Host of the Db2i server (ignored if --use-env is set)")
    parser.add_argument("--user", type=str, help="User for the Db2i server (ignored if --use-env is set)")
    parser.add_argument("--password", type=str, help="Password for the Db2i server (ignored if --use-env is set)")
    parser.add_argument("--port", type=int, default=8075, help="Port of the Db2i server (ignored if --use-env is set)")
    parser.add_argument("--schema", type=str, help="Schema name (ignored if --use-env is set)")
    parser.add_argument("--ignore-unauthorized", action="store_true", help="Ignore unauthorized access (optional)")
    parser.add_argument("--ignore-tables", type=str, nargs="+", help="Tables to ignore (optional)")
    parser.add_argument("--include-tables", type=str, nargs="+", help="Tables to include (optional)")
    parser.add_argument("--custom-table-info", type=str, help="Custom table info (optional)")
    parser.add_argument("--sample-rows-in-table-info", type=int, default=3, help="Number of sample rows in table info (optional, default: 3)")
    parser.add_argument("--max-string-length", type=int, default=300, help="Max string length for truncation (optional, default: 300)")
    args = parser.parse_args()

    # Get database connection details based on use_env flag
    if args.use_env:
        # Use environment variables
        connection_details = {
            "host": os.getenv("HOST"),
            "user": os.getenv("DB_USER"),
            "port": int(os.getenv("DB_PORT", "8075")),
            "password": os.getenv("PASSWORD"),
            "ignoreUnauthorized": os.getenv("IGNORE_UNAUTHORIZED", "true").lower() == "true",
        }
        schema = os.getenv("SCHEMA")
    else:
        # Use command line arguments
        if not all([args.host, args.user, args.password, args.schema]):
            raise ValueError("When not using environment variables, you must provide --host, --user, --password, and --schema")

        connection_details = {
            "host": args.host,
            "user": args.user,
            "port": args.port,
            "password": args.password,
            "ignoreUnauthorized": args.ignore_unauthorized,
        }
        schema = args.schema

    # Initialize server
    server = Server(SERVER)

    # Initialize database connection
    db = Db2iDatabase(
        schema=schema or "",  # Ensure schema is always a string
        server_config=connection_details,
        ignore_tables=args.ignore_tables,
        include_tables=args.include_tables,
        custom_table_info=args.custom_table_info,
        sampler_rows_in_table_info=args.sample_rows_in_table_info,
        max_string_length=args.max_string_length,
    )

    @server.list_resources()
    async def handle_list_resources() -> list[types.Resource]:
        """
        List available note resources.
        Each note is exposed as a resource with a custom note:// URI scheme.
        """
        return [
            types.Resource(
                uri=AnyUrl(f"note://internal/{name}"),
                name=f"Note: {name}",
                description=f"A simple note named {name}",
                mimeType="text/plain",
            )
            for name in notes
        ]

    @server.read_resource()
    async def handle_read_resource(uri: AnyUrl) -> str:
        """
        Read a specific note's content by its URI.
        The note name is extracted from the URI host component.
        """
        if uri.scheme != "note":
            raise ValueError(f"Unsupported URI scheme: {uri.scheme}")

        name = uri.path
        if name is not None:
            name = name.lstrip("/")
            return notes[name]
        raise ValueError(f"Note not found: {name}")

    @server.list_prompts()
    async def handle_list_prompts() -> list[types.Prompt]:
        """
        List available prompts.
        Each prompt can have optional arguments to customize its behavior.
        """
        return [
            types.Prompt(
                name="summarize-notes",
                description="Creates a summary of all notes",
                arguments=[
                    types.PromptArgument(
                        name="style",
                        description="Style of the summary (brief/detailed)",
                        required=False,
                    )
                ],
            ),
            types.Prompt(
                name="query",
                description="Create an SQL query to answer the user's question",
            )
        ]

    @server.get_prompt()
    async def handle_get_prompt(
        name: str, arguments: dict[str, str] | None
    ) -> types.GetPromptResult:
        """
        Generate a prompt by combining arguments with server state.
        The prompt includes all current notes and can be customized via arguments.
        """
        if name == "summarize-notes":

            style = "brief"
            if arguments is not None and isinstance(arguments, dict):
                style = arguments.get("style", "brief")
            detail_prompt = " Give extensive details." if style == "detailed" else ""

            return types.GetPromptResult(
                description="Summarize the current notes",
                messages=[
                    types.PromptMessage(
                        role="user",
                        content=types.TextContent(
                            type="text",
                            text=f"Here are the current notes to summarize:{detail_prompt}\n\n"
                            + "\n".join(
                                f"- {name}: {content}" for name, content in notes.items()
                            ),
                        ),
                    )
                ],
            )
        elif name == "query":
            return types.GetPromptResult(
                description="Create an SQL query to answer the user's question",
                messages=[
                    types.PromptMessage(
                        role="user",
                        content=types.TextContent(
                            type="text", text=QUERY_PROMPT
                        )
                    )
                ]
            )
        else:
            raise ValueError(f"Unknown prompt: {name}")

    @server.list_tools()
    async def handle_list_tools() -> list[types.Tool]:
        """
        List available tools.
        Each tool specifies its arguments using JSON Schema validation.
        """
        return [
            types.Tool(
                name="list-usable-tables",
                description="List the usable tables in the schema. This tool should be called before running any other tool.",
                inputSchema={
                    "type": "object",
                    "properties": {},
                },
            ),
            types.Tool(
                name="describe-table",
                description="Describe a specific table including ites columns and sample rows. This tool should be called after list-usable-tables.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "table_name": {
                            "type": "string",
                            "description": "The name of the table to describe",
                        },
                    },
                    "required": ["table_name"],
                },
            ),
            types.Tool(
                name="run-sql-query",
                description="run a valid Db2 for i SQL query. This tool should be called after list-usable-tables and describe-table.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "sql": {
                            "type": "string",
                            "description": "SELECT SQL query to execute",
                        },
                    },
                    "required": ["sql"],
                },
            ),
            types.Tool(
                name="add-note",
                description="Add a new note",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "content": {"type": "string"},
                    },
                    "required": ["name", "content"],
                },
            ),
        ]

    @server.call_tool()
    async def handle_call_tool(
        name: str, arguments: dict | None
    ) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
        """
        Handle tool execution requests.
        Tools can modify server state and notify clients of changes.
        """

        try:
            if name == "list-usable-tables":
                usable_tables = db.get_usable_table_names()
                return [
                    types.TextContent(
                        type="text", text=f"Usable tables: {usable_tables}"
                    )
                ]

            elif name == "describe-table":
                if not arguments or not isinstance(arguments, dict) or "table_name" not in arguments:
                    raise ValueError("Missing table_name argument")

                table_name = str(arguments["table_name"]).upper()
                table_info = db.get_table_info_no_throw([table_name])
                return [types.TextContent(type="text", text=table_info)]

            elif name == "run-sql-query":
                if not arguments or not isinstance(arguments, dict) or "sql" not in arguments:
                    raise ValueError("Missing sql argument")

                sql = str(arguments["sql"])
                result = db.run_no_throw(sql)
                return [types.TextContent(type="text", text=f"Query result: {result}")]

            elif name == "add-note":
                if not arguments:
                    raise ValueError("Missing arguments")

                note_name = None
                content = None
                if isinstance(arguments, dict):
                    note_name = arguments.get("name")
                    content = arguments.get("content")

                if not note_name or not content:
                    raise ValueError("Missing name or content")

                # Update server state
                notes[note_name] = content

                # Notify clients that resources have changed
                await server.request_context.session.send_resource_list_changed()

                return [
                    types.TextContent(
                        type="text",
                        text=f"Added note '{note_name}' with content: {content}",
                    )
                ]

            else:
                # Handle unknown tool name
                raise ValueError(f"Unknown tool: {name}")

        except Exception as e:
            return [types.TextContent(type="text", text=f"Error: {str(e)}")]

    # Run the server using stdin/stdout streams
    try:
        async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
            # logger.debug("stdio streams initialized")
            await server.run(
                read_stream,
                write_stream,
                InitializationOptions(
                    server_name="db2i-mcp-server",
                    server_version="0.1.0",
                    capabilities=server.get_capabilities(
                        notification_options=NotificationOptions(),
                        experimental_capabilities={},
                    ),
                ),
            )
    except Exception as e:
        # logger.critical(f"Server terminated with error: {type(e).__name__}: {str(e)}")
        raise
