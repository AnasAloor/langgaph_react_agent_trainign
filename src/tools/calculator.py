"""
Calculator Tool
================
A simple calculator tool for mathematical operations.
Demonstrates how to create tools for LangGraph agents.
"""

from langchain_core.tools import tool
from typing import Union
import math


@tool
def calculator(expression: str) -> str:
    """
    Evaluate a mathematical expression safely.
    
    Args:
        expression: A mathematical expression to evaluate (e.g., "2 + 2", "sqrt(16)", "10 * 5")
    
    Returns:
        The result of the mathematical expression as a string.
    
    Examples:
        - calculator("2 + 2") -> "4"
        - calculator("sqrt(16)") -> "4.0"
        - calculator("10 ** 2") -> "100"
    """
    try:
        # Safe math functions allowed
        safe_dict = {
            "sqrt": math.sqrt,
            "pow": math.pow,
            "sin": math.sin,
            "cos": math.cos,
            "tan": math.tan,
            "log": math.log,
            "log10": math.log10,
            "exp": math.exp,
            "abs": abs,
            "round": round,
            "pi": math.pi,
            "e": math.e,
        }
        
        # Evaluate the expression safely
        result = eval(expression, {"__builtins__": {}}, safe_dict)
        return f"Result: {result}"
    except Exception as e:
        return f"Error evaluating expression: {str(e)}"


@tool
def add(a: float, b: float) -> str:
    """Add two numbers together.
    
    Args:
        a: First number
        b: Second number
    
    Returns:
        Sum of the two numbers
    """
    return f"Result: {a + b}"


@tool
def multiply(a: float, b: float) -> str:
    """Multiply two numbers together.
    
    Args:
        a: First number
        b: Second number
    
    Returns:
        Product of the two numbers
    """
    return f"Result: {a * b}"
