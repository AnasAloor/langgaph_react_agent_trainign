# 🎯 ReAct Agent Demo - Presentation Slides

## Slide Deck for Training Session

Use these slides with [Marp](https://marp.app/), [Reveal.js](https://revealjs.com/), or copy to PowerPoint.

---

# Slide 1: Title

## Building Agentic AI
### with LangGraph & Google Gemini

**ReAct Agent Implementation Demo**

🗓️ Training Session | ⏱️ 20-30 Minutes

---

# Slide 2: Agenda

## What We'll Cover Today

| Time | Topic |
|------|-------|
| 5 min | 🎯 Introduction to AI Agents |
| 5 min | 🧠 ReAct Pattern & LangGraph |
| 10 min | 💻 Live Demo |
| 5 min | 📁 Code Architecture |
| 5 min | ❓ Q&A |

---

# Slide 3: What is an AI Agent?

## AI Agent = Autonomous AI System

### Traditional Chatbot:
```
Query → LLM → Response
```

### AI Agent:
```
Query → Think → Act → Observe → Think → ... → Response
```

**Key Difference:** Agents can use **tools** and **reason** through problems!

---

# Slide 4: The ReAct Pattern

## ReAct = Reasoning + Acting

```
┌─────────────────────────────────┐
│         ReAct Loop               │
│                                  │
│   💭 THOUGHT: "I need to..."    │
│        ↓                         │
│   ⚡ ACTION: use_tool(args)      │
│        ↓                         │
│   👁️ OBSERVATION: "Result..."   │
│        ↓                         │
│   🔄 REPEAT or 📝 RESPOND        │
└─────────────────────────────────┘
```

---

# Slide 5: ReAct Example

## Query: "What is 25 × 4 + 50?"

```
💭 THOUGHT: I need to multiply first, then add.

⚡ ACTION: calculator("25 * 4")
👁️ OBSERVATION: Result: 100

💭 THOUGHT: Now add 50 to the result.

⚡ ACTION: calculator("100 + 50")
👁️ OBSERVATION: Result: 150

📝 ANSWER: 25 × 4 + 50 = 150
```

---

# Slide 6: LangGraph Overview

## State-Based Agent Workflows

**LangGraph Components:**

| Component | Purpose |
|-----------|---------|
| **StateGraph** | Define workflow structure |
| **Nodes** | Process functions |
| **Edges** | Flow connections |
| **State** | Shared data store |

```python
graph = StateGraph(AgentState)
graph.add_node("agent", agent_function)
graph.add_node("tools", tool_executor)
```

---

# Slide 7: Agent Architecture

## System Overview

```
┌──────────────────────────────────────┐
│            ReAct Agent               │
├──────────────────────────────────────┤
│                                      │
│   User → [LangGraph] → [Gemini LLM]  │
│               ↓                      │
│          [Tool Node]                 │
│          ┌────────┐                  │
│          │ Calc   │                  │
│          │ Search │                  │
│          │ Time   │                  │
│          └────────┘                  │
│               ↓                      │
│          Response                    │
└──────────────────────────────────────┘
```

---

# Slide 8: Code Structure

## Project Organization

```
agentic_ai_demo/
├── main.py           # Entry point
├── src/
│   ├── agents/       # ReAct Agent
│   ├── tools/        # Calculator, Search
│   ├── prompts/      # System prompts
│   └── utils/        # Helpers
├── config/           # Settings
├── docs/             # Documentation
└── notebooks/        # Jupyter demo
```

---

# Slide 9: Tool Definition

## Creating Agent Tools

```python
from langchain_core.tools import tool

@tool
def calculator(expression: str) -> str:
    """Evaluate math expressions."""
    result = eval(expression)
    return f"Result: {result}"

@tool
def search(query: str) -> str:
    """Search for information."""
    return fetch_data(query)
```

---

# Slide 10: Building the Agent

## LangGraph Implementation

```python
# 1. Define state
class AgentState(TypedDict):
    messages: List[BaseMessage]

# 2. Build graph
graph = StateGraph(AgentState)
graph.add_node("agent", agent_node)
graph.add_node("tools", ToolNode(tools))

# 3. Add edges
graph.add_conditional_edges(
    "agent", 
    should_continue
)

# 4. Compile
agent = graph.compile()
```

---

# Slide 11: Live Demo Time! 🚀

## Let's See It In Action

```bash
# Interactive mode
python main.py

# Demo queries
python main.py --demo

# Single query
python main.py --query "What is 2+2?"
```

**Demo Queries:**
1. Math: "What is 25 × 4 + 50?"
2. Search: "What is LangGraph?"
3. Time: "What time is it?"

---

# Slide 12: Key Takeaways

## What We Learned

✅ **ReAct Pattern** - Think → Act → Observe

✅ **LangGraph** - State machines for agents

✅ **Tools** - Extend agent capabilities

✅ **Gemini** - Powerful LLM backbone

✅ **Modular Design** - Clean code architecture

---

# Slide 13: Next Steps

## Continue Your Learning

### Extend This Demo:
- Add more tools (web, database)
- Implement memory
- Add error handling

### Advanced Topics:
- Multi-agent systems
- Human-in-the-loop
- Production deployment

### Resources:
- LangGraph Docs
- ReAct Paper
- Gemini API Docs

---

# Slide 14: Questions?

## Q&A Time

**Contact:**
- 📧 training@example.com
- 🔗 github.com/demo-repo

**Resources:**
- 📚 docs.langchain.com/langgraph
- 📄 arxiv.org/abs/2210.03629

---

# Slide 15: Thank You!

## Happy Building! 🎉

```
     🤖
    /|\\
    / \\
   
"Go build something amazing!"
```

**Code Repository:** Available in training materials

---

## Notes for Presenter

### Before the Session:
1. Test API key works
2. Run `python main.py --demo` to verify
3. Have backup slides ready

### During Demo:
1. Start with simple math query
2. Show step-by-step output
3. Explain each reasoning step
4. Let audience suggest queries

### Common Questions:
- "Why LangGraph?" → Better control over agent loop
- "Can I use OpenAI?" → Yes, swap the LLM
- "Is it production-ready?" → Add error handling first
