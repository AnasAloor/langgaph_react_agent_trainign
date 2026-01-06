# 🎓 Training Guide: Building Agentic AI with LangGraph

## Session Overview

**Topic:** ReAct Agent Implementation with LangGraph & Gemini  
**Duration:** 20-30 minutes  
**Level:** Intermediate  
**Prerequisites:** Basic Python, Understanding of LLMs

---

## 📋 Session Agenda

| Time | Section | Description |
|------|---------|-------------|
| 0-5 min | Introduction | What are AI Agents? Why ReAct? |
| 5-10 min | Concepts | ReAct pattern, LangGraph basics |
| 10-20 min | Live Demo | Hands-on code walkthrough |
| 20-25 min | Code Deep-Dive | Architecture review |
| 25-30 min | Q&A | Discussion & wrap-up |

---

## 🎯 Learning Objectives

By the end of this session, participants will:

1. ✅ Understand the **ReAct paradigm** (Reasoning + Acting)
2. ✅ Know how to build **agents with LangGraph**
3. ✅ Implement **custom tools** for agents
4. ✅ Design effective **system prompts**
5. ✅ Run and debug **agentic AI workflows**

---

## 📚 Part 1: Introduction (5 minutes)

### What is an AI Agent?

> An AI Agent is an autonomous system that can:
> - **Perceive** its environment (through inputs)
> - **Reason** about what actions to take
> - **Act** using tools and APIs
> - **Learn** from observations

### Traditional Chatbot vs AI Agent

| Chatbot | AI Agent |
|---------|----------|
| Single response | Multi-step reasoning |
| No tool access | Uses external tools |
| Stateless | Maintains context |
| Limited capability | Extensible |

### Why ReAct?

The **ReAct** (Reasoning + Acting) pattern enables:
- 🧠 **Explicit reasoning** before actions
- 🔧 **Tool use** for real-world interactions  
- 👁️ **Observation** of results
- 🔄 **Iterative refinement**

---

## 📚 Part 2: Core Concepts (5 minutes)

### The ReAct Loop

```
┌─────────────────────────────────────┐
│         ReAct Reasoning Loop         │
├─────────────────────────────────────┤
│                                      │
│   Query → THOUGHT → ACTION           │
│              ↑          ↓            │
│              └── OBSERVATION ←┘      │
│                      ↓               │
│                  Response            │
│                                      │
└─────────────────────────────────────┘
```

### Example ReAct Trace

```
User: What is 25 * 4 + 50?

THOUGHT: I need to break this into two calculations.
         First multiply 25 by 4, then add 50.

ACTION: calculator("25 * 4")

OBSERVATION: Result: 100

THOUGHT: Now I need to add 50 to 100.

ACTION: calculator("100 + 50")

OBSERVATION: Result: 150

RESPONSE: 25 × 4 + 50 = 150
```

### LangGraph Components

| Component | Purpose |
|-----------|---------|
| **StateGraph** | Defines the workflow structure |
| **Nodes** | Functions that process state |
| **Edges** | Connections between nodes |
| **State** | Data passed through the graph |

---

## 📚 Part 3: Live Demo (10 minutes)

### Step 1: Environment Setup

```bash
# Install dependencies
pip install langchain langgraph langchain-google-genai

# Set API key
export GOOGLE_API_KEY="your-key-here"
```

### Step 2: Run the Demo

```bash
# Interactive mode
python main.py

# Demo mode with examples
python main.py --demo

# Single query
python main.py --query "What is LangGraph?"
```

### Demo Queries to Try

1. **Math Problem:**
   ```
   What is 25 multiplied by 4, then add 50?
   ```

2. **Information Query:**
   ```
   What is LangGraph and how does it work?
   ```

3. **Multi-Step Task:**
   ```
   What's the weather in Tokyo and what time is it?
   ```

4. **Complex Reasoning:**
   ```
   If I have 3 apples at $2 each and 5 oranges at $1.50 each,
   what's my total cost?
   ```

---

## 📚 Part 4: Code Architecture (5 minutes)

### Key Files to Review

#### 1. Agent Implementation (`src/agents/react_agent.py`)

```python
class ReActAgent:
    def __init__(self, llm, tools=None, system_prompt=None):
        self.tools = tools or ALL_TOOLS
        self.llm_with_tools = llm.bind_tools(self.tools)
        self.graph = self._build_graph()
    
    def _build_graph(self):
        graph = StateGraph(AgentState)
        graph.add_node("agent", self._agent_node)
        graph.add_node("tools", ToolNode(self.tools))
        graph.set_entry_point("agent")
        graph.add_conditional_edges("agent", self._should_continue)
        graph.add_edge("tools", "agent")
        return graph.compile()
```

#### 2. Tool Definition (`src/tools/calculator.py`)

```python
from langchain_core.tools import tool

@tool
def calculator(expression: str) -> str:
    """Evaluate a mathematical expression."""
    result = eval(expression, {"__builtins__": {}}, safe_dict)
    return f"Result: {result}"
```

#### 3. System Prompt (`src/prompts/react_prompts.py`)

```python
REACT_SYSTEM_PROMPT = """You are a helpful AI assistant 
that uses the ReAct (Reasoning + Acting) approach.

## Your Approach:
1. **Think** - Analyze the user's question
2. **Act** - Use available tools when needed
3. **Observe** - Process the results
4. **Respond** - Provide a clear answer
"""
```

### State Flow Diagram

```
Initial State          After Agent          After Tools
─────────────          ───────────          ───────────
[HumanMessage]    →    [HumanMessage,   →   [HumanMessage,
                        AIMessage]          AIMessage,
                                            ToolMessage]
```

---

## 📚 Part 5: Key Takeaways

### ✅ What We Covered

1. **ReAct Pattern**
   - Thought → Action → Observation loop
   - Explicit reasoning before acting
   - Iterative problem solving

2. **LangGraph**
   - State-based agent workflows
   - Conditional edges for control flow
   - Built-in tool execution

3. **Tool Integration**
   - `@tool` decorator for custom tools
   - Function calling with LLMs
   - Error handling

4. **Best Practices**
   - Clear system prompts
   - Modular code structure
   - Streaming for visibility

### 🚀 Next Steps

1. **Extend the Agent:**
   - Add more tools (web scraping, database queries)
   - Implement memory for multi-turn conversations
   - Add error recovery mechanisms

2. **Production Considerations:**
   - Add observability (LangSmith)
   - Implement rate limiting
   - Add input validation

3. **Advanced Topics:**
   - Multi-agent systems
   - Human-in-the-loop
   - Fine-tuning for specific domains

---

## 🔗 Resources

### Documentation
- [LangGraph Docs](https://langchain-ai.github.io/langgraph/)
- [LangChain Tools](https://python.langchain.com/docs/modules/tools/)
- [Gemini API](https://ai.google.dev/docs)

### Papers
- [ReAct: Synergizing Reasoning and Acting](https://arxiv.org/abs/2210.03629)
- [Toolformer](https://arxiv.org/abs/2302.04761)

### Videos
- [Building Agents with LangGraph](https://www.youtube.com/langchain)

---

## ❓ FAQ

**Q: Why LangGraph instead of plain LangChain?**
> LangGraph provides better control over the agent loop with explicit state management and conditional edges.

**Q: Can I use OpenAI instead of Gemini?**
> Yes! Just install `langchain-openai` and swap the LLM initialization.

**Q: How do I add memory to the agent?**
> LangGraph supports checkpointing. Add a `MemorySaver` to persist state between conversations.

**Q: Is this production-ready?**
> This is a demo. For production, add error handling, rate limiting, monitoring, and security measures.

---

## 📝 Exercise (Optional)

**Challenge:** Add a new tool to the agent!

1. Create a new tool in `src/tools/`:
```python
@tool
def word_count(text: str) -> str:
    """Count words in text."""
    count = len(text.split())
    return f"Word count: {count}"
```

2. Add it to `ALL_TOOLS` in `src/tools/__init__.py`

3. Test with:
```
python main.py --query "How many words are in 'Hello world how are you'?"
```

---

*Happy Learning! 🎉*
