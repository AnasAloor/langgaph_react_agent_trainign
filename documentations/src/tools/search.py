"""
Web Search Tool
================
A simulated web search tool for demonstration purposes.
In production, this would integrate with real search APIs.
"""

from langchain_core.tools import tool
from typing import Optional
from datetime import datetime


# Simulated knowledge base for demo
KNOWLEDGE_BASE = {
    "langgraph": {
        "title": "LangGraph - Build Stateful AI Agents",
        "content": "LangGraph is a library for building stateful, multi-actor applications with LLMs. "
                  "It extends LangChain with cyclic computational capabilities, enabling complex agent workflows. "
                  "Key features: State management, Conditional edges, Parallel execution, Human-in-the-loop.",
        "url": "https://langchain-ai.github.io/langgraph/"
    },
    "react agent": {
        "title": "ReAct: Synergizing Reasoning and Acting in Language Models",
        "content": "ReAct (Reasoning + Acting) is a paradigm where LLMs interleave reasoning traces and actions. "
                  "The agent thinks step-by-step (Thought), takes an action (Action), and observes the result (Observation). "
                  "This loop continues until the task is complete.",
        "url": "https://arxiv.org/abs/2210.03629"
    },
    "gemini api": {
        "title": "Google Gemini API Documentation",
        "content": "Gemini is Google's most capable AI model family. The API provides access to Gemini 1.5 Pro, "
                  "Gemini 1.5 Flash, and other models. Features include multimodal understanding, "
                  "long context windows (up to 2M tokens), and function calling capabilities.",
        "url": "https://ai.google.dev/docs"
    },
    "langchain": {
        "title": "LangChain - Build LLM Applications",
        "content": "LangChain is a framework for developing applications powered by language models. "
                  "It provides modules for prompts, models, memory, chains, agents, and tools. "
                  "LangChain Expression Language (LCEL) enables easy composition of components.",
        "url": "https://python.langchain.com/"
    },
    "python": {
        "title": "Python Programming Language",
        "content": "Python is a high-level, general-purpose programming language. "
                  "Current stable version is Python 3.12. Known for readability and extensive libraries. "
                  "Widely used in AI/ML, web development, data science, and automation.",
        "url": "https://www.python.org/"
    },
    "weather": {
        "title": "Current Weather Information",
        "content": f"Weather data as of {datetime.now().strftime('%Y-%m-%d')}: "
                  "Temperature varies by location. For accurate weather, please specify a city. "
                  "Demo shows: New York - 45°F, London - 50°F, Tokyo - 55°F, Sydney - 75°F.",
        "url": "https://weather.example.com/"
    }
}


@tool
def web_search(query: str) -> str:
    """
    Search the web for information on a given topic.
    
    Args:
        query: The search query string
    
    Returns:
        Search results with title, content snippet, and source URL
    
    Note:
        This is a simulated search for demo purposes.
        In production, integrate with Google Search API, Tavily, or similar.
    """
    query_lower = query.lower()
    
    # Search through knowledge base
    results = []
    for key, data in KNOWLEDGE_BASE.items():
        if key in query_lower or any(word in query_lower for word in key.split()):
            results.append(data)
    
    if not results:
        # Return generic response if no match
        return (
            f"Search results for '{query}':\n"
            "No specific results found in demo knowledge base.\n"
            "In production, this would return real web search results.\n"
            "Tip: Try searching for 'LangGraph', 'ReAct agent', 'Gemini API', or 'Python'."
        )
    
    # Format results
    output = f"Search results for '{query}':\n\n"
    for i, result in enumerate(results, 1):
        output += f"{i}. **{result['title']}**\n"
        output += f"   {result['content']}\n"
        output += f"   Source: {result['url']}\n\n"
    
    return output


@tool
def get_current_time() -> str:
    """
    Get the current date and time.
    
    Returns:
        Current date and time in a readable format
    """
    now = datetime.now()
    return f"Current date and time: {now.strftime('%A, %B %d, %Y at %I:%M %p')}"


@tool
def get_weather(city: str) -> str:
    """
    Get weather information for a city (simulated).
    
    Args:
        city: Name of the city
    
    Returns:
        Weather information for the specified city
    """
    # Simulated weather data
    weather_data = {
        "new york": {"temp": 45, "condition": "Partly Cloudy", "humidity": 65},
        "london": {"temp": 50, "condition": "Rainy", "humidity": 80},
        "tokyo": {"temp": 55, "condition": "Clear", "humidity": 55},
        "sydney": {"temp": 75, "condition": "Sunny", "humidity": 60},
        "paris": {"temp": 48, "condition": "Overcast", "humidity": 70},
        "mumbai": {"temp": 85, "condition": "Humid", "humidity": 85},
    }
    
    city_lower = city.lower()
    if city_lower in weather_data:
        data = weather_data[city_lower]
        return (
            f"Weather in {city.title()}:\n"
            f"- Temperature: {data['temp']}°F ({(data['temp']-32)*5/9:.1f}°C)\n"
            f"- Condition: {data['condition']}\n"
            f"- Humidity: {data['humidity']}%"
        )
    else:
        return f"Weather data not available for '{city}'. Available cities: {', '.join(weather_data.keys())}"
