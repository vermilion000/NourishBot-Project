import sys
import logging
from mcp.server.fastmcp import FastMCP


logging.basicConfig(level = logging.INFO,filename = "app.log",filemode = 'a',encoding = "utf-8" )
logger = logging.getLogger("Agent_toolsl_Logger")
logger.info("creating MCP object")
mcp =FastMCP("Agent_tools")


async def execute_in_sandbox(code, dataset): return {"status": "success", "result": "sandbox_output"}
async def persist_result(table, payload): return {"status": "saved"}


@mcp.tool()
async def run_analysis(code: str, dataset: str) -> dict:
    """
    Executes a Python snippet against live data and returns the result.
    Use when the user wants to compute aggregates, filter records,
    or derive insights. The code must assign its final output to a
    variable named 'output'.
    
    Args:
        code: Python code to execute.
        dataset: One of 'sales', 'inventory', 'pipeline'.
    """
    logger.info(f"run_analysis | dataset={dataset}")
    return await execute_in_sandbox(code, dataset)


@mcp.tool()
async def write_to_db(table: str, payload: dict) -> dict:
    """
    Persists a result record to the analyst results table.
    Only call this after run_analysis has returned a verified output.
    
    Args:
        table: Target table name.
        payload: Key-value pairs to write as a new record.
    """
    logger.info(f"write_to_db | table={table}")
    return await persist_result(table, payload)

if __name__ == "__main__":
    mcp.run(transport="http")
