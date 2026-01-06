# 🤖 ReAct Agent Demo

## Building Agentic AI with LangGraph & Google Gemini

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![LangGraph](https://img.shields.io/badge/LangGraph-latest-green.svg)](https://langchain-ai.github.io/langgraph/)
[![Gemini](https://img.shields.io/badge/Gemini-1.5-orange.svg)](https://ai.google.dev/)

A production-ready demonstration of building **Agentic AI applications** using the **ReAct paradigm** with **LangGraph** state machines and **Google Gemini** LLM.

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Key Concepts](#-key-concepts)
- [Architecture](#-architecture)
- [Project Structure](#-project-structure)
- [Quick Start](#-quick-start)
- [Usage Examples](#-usage-examples)
- [Training Guide](#-training-guide)
- [API Reference](#-api-reference)

---

## 🎯 Overview

This demo teaches you how to build an **autonomous AI agent** that can:

- **Think** - Reason about problems step-by-step
- **Act** - Use tools to interact with the world
- **Observe** - Process results and learn from them
- **Iterate** - Repeat until the task is complete

### What You'll Learn

1. **ReAct Pattern** - The Reasoning + Acting paradigm
2. **LangGraph** - Building stateful agent workflows
3. **Tool Integration** - Extending agent capabilities
4. **Prompt Engineering** - Crafting effective system prompts

---

## 🧠 Key Concepts

### ReAct (Reasoning + Acting)

The ReAct paradigm combines **chain-of-thought reasoning** with **action execution**:

```
┌─────────────────────────────────────────────────────────┐
│                    ReAct Loop                            │
├─────────────────────────────────────────────────────────┤
│                                                          │
│   User Query ───────────────────────────────────────┐   │
│                                                      │   │
│                                                      ▼   │
│                                              ┌───────────┴───────────┐
│                                              │       THOUGHT         │
│                                              │  "I need to first..." │
│                                              └───────────┬───────────┘
│                                                          │
│                                                          ▼
│                                              ┌───────────┴───────────┐
│                                              │        ACTION         │
│                                              │   Use: calculator()   │
│                                              └───────────┬───────────┘
│                                                          │
│                                                          ▼
│                                              ┌───────────┴───────────┐
│                                              │     OBSERVATION       │
│                                              │   Result: 100         │
│                                              └───────────┬───────────┘
│                                                          │
│                              ┌────────────────┬──────────┘
│                              │                │
│                              ▼                ▼
│                        [More steps?]    [Task Complete]
│                              │                │
│                              └────────────────┼───────────────────▶ Response
│                                               │
└───────────────────────────────────────────────────────────────────────────┘
```

### LangGraph State Machine

LangGraph manages the agent's execution flow using a **directed graph**:

```
START ──▶ [Agent Node] ──▶ {Decision} ──▶ [Tool Node] ──┐
                              │                          │
                              │ (No tool calls)          │
                              ▼                          │
                            END ◀────────────────────────┘
```

### Tools

Tools extend the agent's capabilities:

| Tool | Purpose | Example |
|------|---------|---------|
| `calculator` | Math operations | `calculator("sqrt(16)")` |
| `web_search` | Information lookup | `web_search("LangGraph")` |
| `get_weather` | Weather data | `get_weather("Tokyo")` |
| `get_current_time` | Current time | `get_current_time()` |

---

## 🏗️ Architecture

### High-Level Architecture

```
┌────────────────────────────────────────────────────────────────┐
│                     ReAct Agent System                          │
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────┐     ┌─────────────┐     ┌─────────────┐       │
│  │   User      │────▶│  LangGraph  │────▶│   Gemini    │       │
│  │  Interface  │◀────│   Engine    │◀────│    LLM      │       │
│  └─────────────┘     └──────┬──────┘     └─────────────┘       │
│                             │                                   │
│                             ▼                                   │
│                      ┌─────────────┐                           │
│                      │   Tools     │                           │
│                      │ ┌─────────┐ │                           │
│                      │ │ Calc    │ │                           │
│                      │ ├─────────┤ │                           │
│                      │ │ Search  │ │                           │
│                      │ ├─────────┤ │                           │
│                      │ │ Weather │ │                           │
│                      │ └─────────┘ │                           │
│                      └─────────────┘                           │
│                                                                 │
└────────────────────────────────────────────────────────────────┘
```

### Data Flow

```
┌──────────┐    ┌───────────┐    ┌──────────┐    ┌───────────┐
│  Query   │───▶│  Agent    │───▶│  Tool    │───▶│ Response  │
│          │    │  State    │    │  Results │    │           │
└──────────┘    └───────────┘    └──────────┘    └───────────┘
                     │                │
                     ▼                ▼
               ┌───────────┐    ┌───────────┐
               │ Messages  │    │   State   │
               │   List    │    │  Updates  │
               └───────────┘    └───────────┘
```

---

## 📁 Project Structure

```
agentic_ai_demo/
├── main.py                 # Application entry point
├── requirements.txt        # Python dependencies
├── README.md              # This documentation
│
├── config/                # Configuration module
│   ├── __init__.py
│   └── settings.py        # App settings & LLM config
│
├── src/                   # Source code
│   ├── __init__.py
│   │
│   ├── agents/            # Agent implementations
│   │   ├── __init__.py
│   │   └── react_agent.py # ReAct Agent with LangGraph
│   │
│   ├── tools/             # Tool definitions
│   │   ├── __init__.py
│   │   ├── calculator.py  # Math tools
│   │   └── search.py      # Search & utility tools
│   │
│   ├── prompts/           # System prompts
│   │   ├── __init__.py
│   │   └── react_prompts.py
│   │
│   └── utils/             # Utilities
│       ├── __init__.py
│       └── helpers.py     # Display & logging helpers
│
├── docs/                  # Documentation
│   └── training_guide.md
│
├── diagrams/             # Architecture diagrams
│   └── mermaid_diagrams.md
│
└── notebooks/            # Jupyter notebooks (optional)
    └── demo.ipynb
```

---

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set API Key

```bash
# Linux/Mac
export GOOGLE_API_KEY="your-api-key-here"

# Windows
set GOOGLE_API_KEY=your-api-key-here
```

Get your free API key at: [Google AI Studio](https://makersuite.google.com/app/apikey)

### 3. Run the Demo

```bash
# Interactive mode
python main.py

# Demo mode (predefined queries)
python main.py --demo

# Single query
python main.py --query "What is 25 * 4 + 50?"
```

---

## 💡 Usage Examples

### Basic Usage

```python
from src.agents import create_react_agent

# Create agent
agent = create_react_agent(api_key="your-key")

# Ask a question
response = agent.invoke("What is the square root of 144?")
print(response)
```

### Streaming Execution

```python
# Watch the agent think step-by-step
for step in agent.stream("What's 2+2 and what's the weather in Tokyo?"):
    print(step)
```

### Custom Tools

```python
from langchain_core.tools import tool

@tool
def my_custom_tool(input: str) -> str:
    """My custom tool description."""
    return f"Processed: {input}"

# Add to agent
agent = create_react_agent(
    api_key="your-key",
    tools=[my_custom_tool]
)
```

---

## 📚 Training Guide

### Session Outline (20-30 minutes)

| Time | Topic | Activity |
|------|-------|----------|
| 5 min | Introduction | ReAct concept overview |
| 5 min | Architecture | Walk through code structure |
| 10 min | Live Demo | Run interactive queries |
| 5 min | Code Review | Examine key components |
| 5 min | Q&A | Discussion |

### Key Teaching Points

1. **Why Agents?** - Autonomous AI that can use tools
2. **ReAct Pattern** - Think → Act → Observe loop
3. **LangGraph** - State machine for agent control flow
4. **Tools** - How to extend agent capabilities

---

## 📖 API Reference

### ReActAgent

```python
class ReActAgent:
    def __init__(self, llm, tools=None, system_prompt=None):
        """Initialize the ReAct Agent."""
        
    def invoke(self, query: str) -> str:
        """Run agent with a query, return response."""
        
    def stream(self, query: str):
        """Stream agent execution steps."""
```

### Factory Function

```python
def create_react_agent(
    api_key: str = None,
    model: str = "gemini-1.5-flash",
    temperature: float = 0.1,
    tools: list = None,
) -> ReActAgent:
    """Create a configured ReAct Agent."""
```

---

## 🎓 Further Learning

- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [ReAct Paper](https://arxiv.org/abs/2210.03629)
- [Google Gemini API](https://ai.google.dev/docs)
- [LangChain Tools Guide](https://python.langchain.com/docs/modules/tools/)

---

## 📄 License

MIT License - Feel free to use for learning and education!

---

Built with ❤️ for AI Training & Education
