"""
ReAct Agent Demo - Source Package
===================================
A modular implementation of a ReAct Agent using LangGraph and Google Gemini.

Package Structure:
- agents/: Core agent implementations
- tools/: Tool definitions for agent capabilities
- prompts/: System prompts and templates
- utils/: Helper functions and utilities
"""

__version__ = "1.0.0"
__author__ = "AI Training Demo"

from .agents import ReActAgent, create_react_agent
from .tools import ALL_TOOLS
from .prompts import REACT_SYSTEM_PROMPT
from .utils import create_demo_banner, print_step

__all__ = [
    "ReActAgent",
    "create_react_agent",
    "ALL_TOOLS",
    "REACT_SYSTEM_PROMPT",
    "create_demo_banner",
    "print_step",
]
