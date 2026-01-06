"""
Prompts Module
===============
System prompts and prompt templates for the ReAct Agent.

The ReAct paradigm follows this pattern:
1. THOUGHT: Agent reasons about the current situation
2. ACTION: Agent decides what tool to use
3. OBSERVATION: Agent observes the result
4. REPEAT: Until task is complete

This module contains carefully crafted prompts that guide
the agent through this reasoning process.
"""

# System prompt for the ReAct Agent
REACT_SYSTEM_PROMPT = """You are a helpful AI assistant that uses the ReAct (Reasoning + Acting) approach.

## Your Approach:
1. **Think** - Analyze the user's question and plan your approach
2. **Act** - Use available tools when needed to gather information
3. **Observe** - Process the results from tools
4. **Respond** - Provide a clear, helpful answer

## Available Tools:
You have access to the following tools:
- **calculator**: Evaluate mathematical expressions
- **add**: Add two numbers
- **multiply**: Multiply two numbers
- **web_search**: Search for information on any topic
- **get_current_time**: Get the current date and time
- **get_weather**: Get weather for a city

## Guidelines:
- Always think step-by-step before acting
- Use tools when you need external information or calculations
- Be concise but thorough in your responses
- If a tool fails, try an alternative approach
- Explain your reasoning when helpful

## Response Format:
- For factual questions: Provide direct, accurate answers
- For calculations: Show the result clearly
- For multi-step problems: Walk through your reasoning
"""


# Alternative: Shorter system prompt
REACT_SYSTEM_PROMPT_SHORT = """You are a helpful assistant using ReAct reasoning.
Think step-by-step, use tools when needed, and provide clear answers.
Available tools: calculator, web_search, get_current_time, get_weather."""


# Human message template for structured queries
HUMAN_TEMPLATE = """
User Query: {query}

Please help me with this request. Use your available tools if needed.
"""


# Few-shot examples for the ReAct pattern
REACT_EXAMPLES = """
## Example 1: Math Problem
User: What is 25 multiplied by 4, then add 100?
Thought: I need to break this into two calculations.
Action: multiply(25, 4)
Observation: Result: 100
Thought: Now I need to add 100 to this result.
Action: calculator("100 + 100")
Observation: Result: 200
Answer: 25 × 4 + 100 = 200

## Example 2: Information Query
User: What is LangGraph?
Thought: I should search for information about LangGraph.
Action: web_search("LangGraph")
Observation: [Search results about LangGraph...]
Answer: LangGraph is a library for building stateful AI agents...

## Example 3: Multi-step Query
User: What's the weather in Tokyo and what time is it there?
Thought: I need to get weather and time information.
Action: get_weather("Tokyo")
Observation: Weather in Tokyo: 55°F, Clear...
Action: get_current_time()
Observation: Current time: ...
Answer: In Tokyo, it's currently 55°F and clear. The time is...
"""


def get_system_prompt(verbose: bool = True) -> str:
    """
    Get the appropriate system prompt based on verbosity setting.
    
    Args:
        verbose: If True, return detailed prompt with examples
        
    Returns:
        System prompt string
    """
    if verbose:
        return REACT_SYSTEM_PROMPT
    return REACT_SYSTEM_PROMPT_SHORT


def format_human_message(query: str) -> str:
    """
    Format a human message with the query.
    
    Args:
        query: User's query string
        
    Returns:
        Formatted human message
    """
    return HUMAN_TEMPLATE.format(query=query)
