"""
Tools Module
=============
Collection of tools available for the ReAct Agent.

Tools are the "hands" of an agent - they allow the agent
to interact with the external world and perform actions.
"""

from .calculator import calculator, add, multiply
from .search import web_search, get_current_time, get_weather

# All available tools for the agent
ALL_TOOLS = [
    calculator,
    add,
    multiply,
    web_search,
    get_current_time,
    get_weather,
]

__all__ = [
    "calculator",
    "add", 
    "multiply",
    "web_search",
    "get_current_time",
    "get_weather",
    "ALL_TOOLS",
]
