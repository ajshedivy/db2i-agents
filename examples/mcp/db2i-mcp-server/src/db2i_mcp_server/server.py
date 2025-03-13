from datetime import datetime
import os
import sys
from textwrap import dedent
from typing import Any, Dict, List, Literal, Optional, Union

from dotenv import load_dotenv
from mcp.server.models import InitializationOptions
import mcp.types as types
from mcp.server import NotificationOptions, Server
from pep249 import QueryParameters, ResultRow, ResultSet
from pydantic import AnyUrl
import mcp.server.stdio

from mapepire_python import Connection, DaemonServer, connect

import logging



# # Initialize empty notes dictionary for the server
notes = {}
def configure_logging():
    """
    Configure logging for the MCP server with a simplified approach.
    Redirects stdout to avoid interfering with MCP communication.
    
    Environment variables:
    - ENABLE_LOGGING: Set to "false" to disable all logging
    - LOG_LEVEL: Set to DEBUG, INFO, WARNING, ERROR, or CRITICAL (default: INFO)
    """
    # Check if logging is enabled
    logging_enabled = os.environ.get("ENABLE_LOGGING", "true").lower() != "false"
    
    # Set up log file path
    log_directory = os.path.join(os.getcwd(), "logs")
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
    
    if logging_enabled:
        # Configure logging to file with basicConfig
        logging.basicConfig(
            filename=log_filename,
            filemode='w',
            format='%(asctime)s %(levelname)s [%(name)s:%(funcName)s:%(lineno)d] %(message)s',
            level=logging.DEBUG
        )
        
        # Get our specific logger
        logger = logging.getLogger("db2i_mcp_server")
        
        # Log startup info if enabled
        if logging_enabled:
            logger.info(f"Starting Db2i MCP Server (log level: {log_level_name})")
            logger.info(f"Logs location: {log_filename}")
        
        return logger

    return None


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

        self.connection = None
        self.is_connected = False

        if include_tables and ignore_tables:
            raise ValueError("Cannot specify both include_tables and ignore_tables")

        self._schema = schema
        self._server_config = server_config
        self._include_tables = include_tables
        self._ignore_tables = ignore_tables
        self._all_tables = None  # Will be populated in get_usable_table_names

        self._sample_rows_in_table_info = sampler_rows_in_table_info
        self._customed_table_info = custom_table_info
        self._max_string_length = max_string_length
        
        self.logger = configure_logging()

    def _connect(self) -> Connection:
        """Set up any connections required by the handler

        Should return connection

        """

        if not all(
            key in self._server_config for key in ["host", "port", "user", "password"]
        ):
            raise ValueError(
                "Required parameters (host, user, password, port) must be provided."
            )

        try:
            connect_args = DaemonServer(
                host=self._server_config["host"],
                port=self._server_config["port"],
                user=self._server_config["user"],
                password=self._server_config["password"],
                ignoreUnauthorized=True,
            )
            # schema = self._server_config["schema"]

            self.connection = connect(connect_args)
            self.is_connected = True
            self.connection.execute(f"SET CURRENT SCHEMA = '{self._schema}'")
            return self.connection
        except Exception as e:
            self.logger.error(
                f"Error while connect to {self._server_config.get('host')}, {e}"
            )
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

        try:
            # Sanitize connection details for logging
            safe_config = {k: (v if k != "password" else "***REDACTED***") for k, v in dict(self._server_config).items()}
            conn = self._connect()
            # Connect and execute
            self.logger.info(f"Connected to DB ({safe_config.get('host', 'unknown')})")
            with conn.execute(sql, options) as cursor:
                if not cursor.has_results:
                    self.logger.debug("Query returned no results")
                    return []
                
                # Handle different fetch modes
                if fetch == "all":
                    result = cursor.fetchall()
                    row_count = len(result.get('data', [])) if isinstance(result, dict) else 0
                    self.logger.debug(f"Fetched all rows: {row_count}")
                    return result["data"]
                    
                elif fetch == "one":
                    result = cursor.fetchone()
                    self.logger.debug(f"Fetched one row: {'Found' if result else 'None'}")
                    return result
                    
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
            if "connection" in error_type.lower():
                self.logger.debug(f"Connection details: {safe_config}")
            raise
        
        finally:
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
            return self.run(
                sql, options=parameters, fetch=fetch, include_columns=include_columns
            )
        except Exception as e:
            """Format the error message"""
            return f"Error: {e}"


async def main():
    # Load environment variables
    load_dotenv()
    # logger.debug("Loaded environment variables")

    # Get database connection details
    connection_details = {
        "host": os.getenv("HOST"),
        "user": os.getenv("DB_USER"),
        "port": os.getenv("DB_PORT", 8075),
        "password": os.getenv("PASSWORD"),
        "ignoreUnauthorized": os.getenv("IGNORE_UNAUTHORIZED", True),
    }
    
    # Log connection details (with password redacted)
    safe_details = {k: (v if k != "password" else "***REDACTED***") for k, v in connection_details.items()}
    # logger.info(f"DB connection config: {safe_details}")

    # Get schema name
    SCHEMA = os.getenv("SCHEMA")
    # logger.info(f"Using schema: {SCHEMA}")

    # Initialize server
    # logger.info("Initializing MCP Db2i server")
    server = Server("db2i-mcp-server")
    
    # Initialize database connection
    db = Db2iDatabase(SCHEMA, connection_details)

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
        if name != "summarize-notes":
            raise ValueError(f"Unknown prompt: {name}")

        style = (arguments or {}).get("style", "brief")
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
                if not arguments or "table_name" not in arguments:
                    raise ValueError("Missing table_name argument")

                table_name = arguments["table_name"].upper()
                table_info = db.get_table_info_no_throw([table_name])
                return [types.TextContent(type="text", text=table_info)]

            elif name == "run-sql-query":
                if not arguments or "sql" not in arguments:
                    raise ValueError("Missing sql argument")

                sql = arguments["sql"]
                result = db.run_no_throw(sql)
                return [types.TextContent(type="text", text=f"Query result: {result}")]

            elif name == "add-note":
                if not arguments:
                    raise ValueError("Missing arguments")

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