from typing import List
from langchain_core.tools.base import BaseToolkit
from langchain_core.language_models import BaseLanguageModel
from pydantic import ConfigDict, Field
from react_agent.database import Db2iDatabase
from react_agent.db2i_tools import (
    QuerySQLDatabaseTool,
    ListSQLDatabaseTool,
    InfoSQLDatabaseTool,
    QuerySQLCheckerTool
)

from langchain_core.tools import BaseTool

class Db2iDatabaseToolkit(BaseToolkit):
    """Toolkit for interacting with Db2i databases."""
    
    db: Db2iDatabase = Field(exclude=True)
    llm: BaseLanguageModel = Field(exclude=True)
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
    )
        
    @property
    def dialect(self) -> str:
        """Return string representation of SQL dialect to use."""
        return self.db.dialect
    

    

    def get_tools(self) -> List[BaseTool]:
        """Return list of tools in this toolkit."""

        list_sql_database_tool = ListSQLDatabaseTool(db=self.db)
        
        info_sql_database_tool_description = (
            "Input to this tool is a comma-separated list of tables, output is the "
            "schema and sample rows for those tables. "
            "Be sure that the tables actually exist by calling "
            f"{list_sql_database_tool.name} first! "
            "Example Input: table1, table2, table3"
        )
        info_sql_database_tool = InfoSQLDatabaseTool(db=self.db, description=info_sql_database_tool_description)
        
        query_sql_database_tool_description = (
            "Input to this tool is a detailed and correct SQL query, output is a "
            "result from the database. If the query is not correct, an error message "
            "will be returned. If an error is returned, rewrite the query, check the "
            "query, and try again. If you encounter an issue with Unknown column "
            f"'xxxx' in 'field list', use {info_sql_database_tool.name} "
            "to query the correct table fields."
        )
        query_sql_database_tool = QuerySQLDatabaseTool(
            db=self.db, description=query_sql_database_tool_description
        )
        query_sql_checker_tool_description = (
            "Use this tool to double check if your query is correct before executing "
            "it. Always use this tool before executing a query with "
            f"{query_sql_database_tool.name}!"
        )
        query_sql_checker_tool = QuerySQLCheckerTool(
            db=self.db, llm=self.llm, description=query_sql_checker_tool_description
        )
        return [
            query_sql_database_tool,
            info_sql_database_tool,
            list_sql_database_tool,
            query_sql_checker_tool,
        ]
        
    def get_context(self) -> dict:
        """Return db context that you may want in agent prompt."""
        return self.db.get_context()
    

Db2iDatabaseToolkit.model_rebuild()
        
        
        
    
    