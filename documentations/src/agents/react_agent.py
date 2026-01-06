"""
ReAct Agent Implementation
===========================
A ReAct (Reasoning + Acting) agent built with LangGraph.

This module implements the core agent logic using LangGraph's
state machine capabilities for managing the agent's reasoning loop.

Architecture:
┌─────────────────────────────────────────────────────────┐
│                    ReAct Agent Graph                     │
├─────────────────────────────────────────────────────────┤
│  START ──> [Agent Node] ──> [Conditional Edge]          │
│                │                    │                    │
│                │              ┌─────┴─────┐              │
│                │              │           │              │
│                │         [Tools Node]  [END]             │
│                │              │                          │
│                └──────────────┘                          │
└─────────────────────────────────────────────────────────┘
"""

import os
import sys
from typing import Annotated, TypedDict, Sequence
from typing_extensions import TypedDict

from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from src.tools import ALL_TOOLS
from src.prompts import REACT_SYSTEM_PROMPT


# ============================================================================
# STATE DEFINITION
# ============================================================================

class AgentState(TypedDict):
    """
    State schema for the ReAct Agent.
    
    The state is passed through each node in the graph and
    accumulates information as the agent reasons and acts.
    
    Attributes:
        messages: List of conversation messages (uses add_messages reducer)
    """
    messages: Annotated[Sequence[BaseMessage], add_messages]


# ============================================================================
# AGENT CLASS
# ============================================================================

class ReActAgent:
    """
    ReAct Agent using LangGraph.
    
    This agent implements the ReAct paradigm:
    - Reasoning: Think about what to do
    - Acting: Use tools to accomplish tasks
    - Observing: Process tool outputs
    
    Example Usage:
        >>> from langchain_google_genai import ChatGoogleGenerativeAI
        >>> llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash")
        >>> agent = ReActAgent(llm)
        >>> response = agent.invoke("What is 25 * 4?")
    """
    
    def __init__(self, llm, tools=None, system_prompt: str = None):
        """
        Initialize the ReAct Agent.
        
        Args:
            llm: Language model instance (e.g., ChatGoogleGenerativeAI)
            tools: List of tools (defaults to ALL_TOOLS)
            system_prompt: Custom system prompt (defaults to REACT_SYSTEM_PROMPT)
        """
        self.tools = tools or ALL_TOOLS
        self.system_prompt = system_prompt or REACT_SYSTEM_PROMPT
        
        # Bind tools to the LLM
        self.llm_with_tools = llm.bind_tools(self.tools)
        
        # Build the agent graph
        self.graph = self._build_graph()
    
    def _build_graph(self) -> StateGraph:
        """
        Build the LangGraph state machine.
        
        Returns:
            Compiled StateGraph ready for execution
        """
        # Initialize the graph with our state schema
        graph = StateGraph(AgentState)
        
        # Add nodes
        graph.add_node("agent", self._agent_node)
        graph.add_node("tools", ToolNode(self.tools))
        
        # Set entry point
        graph.set_entry_point("agent")
        
        # Add conditional edge from agent
        graph.add_conditional_edges(
            "agent",
            self._should_continue,
            {
                "continue": "tools",  # If tool call needed
                "end": END,           # If response ready
            }
        )
        
        # Tools always return to agent
        graph.add_edge("tools", "agent")
        
        # Compile and return
        return graph.compile()
    
    def _agent_node(self, state: AgentState) -> dict:
        """
        Agent node - invokes the LLM with tools.
        
        Args:
            state: Current agent state
            
        Returns:
            Updated state with new message
        """
        messages = state["messages"]
        
        # Add system message if not present
        if not messages or not isinstance(messages[0], SystemMessage):
            messages = [SystemMessage(content=self.system_prompt)] + list(messages)
        
        # Invoke LLM
        response = self.llm_with_tools.invoke(messages)
        
        return {"messages": [response]}
    
    def _should_continue(self, state: AgentState) -> str:
        """
        Determine if agent should continue or end.
        
        Args:
            state: Current agent state
            
        Returns:
            "continue" if tool calls present, "end" otherwise
        """
        last_message = state["messages"][-1]
        
        # Check if there are tool calls
        if hasattr(last_message, "tool_calls") and last_message.tool_calls:
            return "continue"
        
        return "end"
    
    def invoke(self, query: str) -> str:
        """
        Run the agent with a user query.
        
        Args:
            query: User's question or request
            
        Returns:
            Agent's final response as a string
        """
        # Create initial state
        initial_state = {
            "messages": [HumanMessage(content=query)]
        }
        
        # Run the graph
        result = self.graph.invoke(initial_state)
        
        # Extract final response
        final_message = result["messages"][-1]
        return final_message.content
    
    def stream(self, query: str):
        """
        Stream the agent's execution step by step.
        
        Args:
            query: User's question or request
            
        Yields:
            State updates at each step
        """
        initial_state = {
            "messages": [HumanMessage(content=query)]
        }
        
        for step in self.graph.stream(initial_state):
            yield step
    
    def get_graph_visualization(self) -> str:
        """
        Get a Mermaid diagram of the agent graph.
        
        Returns:
            Mermaid diagram string
        """
        try:
            return self.graph.get_graph().draw_mermaid()
        except Exception:
            # Fallback if draw_mermaid is not available
            return """
graph TD
    START([Start]) --> agent[Agent Node]
    agent --> decision{Tool Calls?}
    decision -->|Yes| tools[Tool Node]
    decision -->|No| END([End])
    tools --> agent
"""


# ============================================================================
# FACTORY FUNCTION
# ============================================================================

def create_react_agent(
    api_key: str = None,
    model: str = "gemini-1.5-flash",
    temperature: float = 0.1,
    tools: list = None,
) -> ReActAgent:
    """
    Factory function to create a ReAct Agent with Gemini.
    
    Args:
        api_key: Google API key (or set GOOGLE_API_KEY env var)
        model: Model name (default: gemini-1.5-flash)
        temperature: Sampling temperature
        tools: Custom tools list
        
    Returns:
        Configured ReActAgent instance
    """
    from langchain_google_genai import ChatGoogleGenerativeAI
    
    # Get API key
    api_key = api_key or os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
    
    if not api_key:
        raise ValueError(
            "API key required. Set GOOGLE_API_KEY environment variable "
            "or pass api_key parameter."
        )
    
    # Initialize LLM
    llm = ChatGoogleGenerativeAI(
        model=model,
        google_api_key=api_key,
        temperature=temperature,
    )
    
    # Create and return agent
    return ReActAgent(llm=llm, tools=tools)
