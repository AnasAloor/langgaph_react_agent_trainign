"""
Utility Functions
==================
Helper functions for visualization, logging, and debugging.
"""

import json
from datetime import datetime
from typing import Any, Dict, List
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, ToolMessage


def format_message(message: BaseMessage) -> str:
    """
    Format a message for display.
    
    Args:
        message: LangChain message object
        
    Returns:
        Formatted string representation
    """
    if isinstance(message, HumanMessage):
        return f"👤 Human: {message.content}"
    elif isinstance(message, AIMessage):
        content = message.content or "[Tool Call]"
        tool_info = ""
        if hasattr(message, "tool_calls") and message.tool_calls:
            tools = [tc["name"] for tc in message.tool_calls]
            tool_info = f"\n   🔧 Tools: {', '.join(tools)}"
        return f"🤖 Agent: {content}{tool_info}"
    elif isinstance(message, ToolMessage):
        return f"⚙️  Tool ({message.name}): {message.content[:100]}..."
    else:
        return f"📝 {type(message).__name__}: {message.content}"


def print_step(step: Dict[str, Any], step_num: int = None) -> None:
    """
    Pretty print an agent execution step.
    
    Args:
        step: Step dictionary from graph execution
        step_num: Optional step number for display
    """
    prefix = f"Step {step_num}" if step_num else "Step"
    print(f"\n{'='*60}")
    print(f"📌 {prefix}")
    print('='*60)
    
    for node_name, state in step.items():
        print(f"\n🔹 Node: {node_name}")
        if "messages" in state:
            for msg in state["messages"]:
                print(f"   {format_message(msg)}")


def print_conversation(messages: List[BaseMessage]) -> None:
    """
    Print the full conversation history.
    
    Args:
        messages: List of conversation messages
    """
    print("\n" + "="*60)
    print("📜 Conversation History")
    print("="*60)
    
    for i, msg in enumerate(messages, 1):
        print(f"\n[{i}] {format_message(msg)}")


def create_demo_banner(title: str = "ReAct Agent Demo") -> str:
    """
    Create an ASCII art banner for the demo.
    
    Args:
        title: Title text
        
    Returns:
        ASCII banner string
    """
    width = max(60, len(title) + 10)
    border = "═" * width
    padding = " " * ((width - len(title)) // 2)
    
    return f"""
╔{border}╗
║{padding}{title}{padding}║
║{' ' * ((width - 29) // 2)}Built with LangGraph + Gemini{' ' * ((width - 29) // 2)}║
╚{border}╝
"""


def log_execution(query: str, response: str, duration: float = None) -> Dict:
    """
    Create a structured log entry for agent execution.
    
    Args:
        query: User query
        response: Agent response
        duration: Execution time in seconds
        
    Returns:
        Log entry dictionary
    """
    return {
        "timestamp": datetime.now().isoformat(),
        "query": query,
        "response": response,
        "duration_seconds": duration,
    }


def save_logs(logs: List[Dict], filepath: str = "execution_logs.json") -> None:
    """
    Save execution logs to a JSON file.
    
    Args:
        logs: List of log entries
        filepath: Output file path
    """
    with open(filepath, "w") as f:
        json.dump(logs, f, indent=2)
    print(f"💾 Logs saved to {filepath}")
