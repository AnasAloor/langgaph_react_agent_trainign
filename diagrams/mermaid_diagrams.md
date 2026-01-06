# 📊 Mermaid Diagrams for ReAct Agent Demo

This document contains all the architectural and flow diagrams for the training session.

---

## 1. ReAct Agent Execution Flow

```mermaid
flowchart TD
    subgraph Input
        A[👤 User Query] --> B[📥 HumanMessage]
    end
    
    subgraph LangGraph["🔄 LangGraph State Machine"]
        B --> C{🤖 Agent Node}
        C -->|"Add System Prompt"| D[💭 LLM Reasoning]
        D -->|"Generate Response"| E{🔀 Decision Point}
        
        E -->|"Tool Calls Present"| F[🔧 Tool Node]
        E -->|"No Tool Calls"| G[✅ Final Response]
        
        F -->|"Execute Tools"| H[📊 Tool Results]
        H -->|"Add Observations"| C
    end
    
    subgraph Output
        G --> I[📤 Response to User]
    end
    
    style A fill:#e1f5fe
    style I fill:#c8e6c9
    style C fill:#fff3e0
    style F fill:#fce4ec
```

---

## 2. ReAct Reasoning Loop (Detailed)

```mermaid
flowchart LR
    subgraph Thought["💭 THOUGHT"]
        T1[Analyze Query]
        T2[Plan Approach]
        T3[Identify Tools Needed]
    end
    
    subgraph Action["⚡ ACTION"]
        A1[Select Tool]
        A2[Prepare Arguments]
        A3[Execute Tool Call]
    end
    
    subgraph Observation["👁️ OBSERVATION"]
        O1[Receive Results]
        O2[Parse Output]
        O3[Update State]
    end
    
    T1 --> T2 --> T3
    T3 --> A1 --> A2 --> A3
    A3 --> O1 --> O2 --> O3
    O3 -->|"Need More Info?"| T1
    O3 -->|"Task Complete"| Final[📝 Generate Answer]
    
    style Thought fill:#e3f2fd
    style Action fill:#fff8e1
    style Observation fill:#f3e5f5
```

---

## 3. System Architecture Overview

```mermaid
flowchart TB
    subgraph User["👤 User Layer"]
        UI[CLI / API Interface]
    end
    
    subgraph Application["🖥️ Application Layer"]
        Main[main.py]
        Config[config/settings.py]
    end
    
    subgraph Agent["🤖 Agent Layer"]
        RA[ReActAgent]
        State[AgentState]
        Graph[StateGraph]
    end
    
    subgraph LLM["🧠 LLM Layer"]
        Gemini[Google Gemini API]
        Binding[Tool Binding]
    end
    
    subgraph Tools["🔧 Tools Layer"]
        Calc[calculator.py]
        Search[search.py]
    end
    
    subgraph Prompts["📝 Prompts Layer"]
        System[System Prompt]
        Templates[Message Templates]
    end
    
    UI --> Main
    Main --> Config
    Main --> RA
    RA --> State
    RA --> Graph
    Graph --> Binding
    Binding --> Gemini
    RA --> Calc
    RA --> Search
    RA --> System
    
    style User fill:#e1f5fe
    style Agent fill:#fff3e0
    style LLM fill:#e8f5e9
    style Tools fill:#fce4ec
```

---

## 4. LangGraph State Machine

```mermaid
stateDiagram-v2
    [*] --> AgentNode: START
    
    AgentNode --> Decision: LLM Response
    
    Decision --> ToolNode: tool_calls exist
    Decision --> End: no tool_calls
    
    ToolNode --> AgentNode: tool results
    
    End --> [*]: Final Response
    
    note right of AgentNode
        Invokes LLM with:
        - System prompt
        - Message history
        - Available tools
    end note
    
    note right of ToolNode
        Executes requested tools
        Adds results to messages
    end note
```

---

## 5. Tool Execution Flow

```mermaid
sequenceDiagram
    participant U as User
    participant A as Agent
    participant L as LLM (Gemini)
    participant T as Tools
    
    U->>A: "What is 25 * 4?"
    A->>L: Process with tools bound
    L-->>A: ToolCall: multiply(25, 4)
    A->>T: Execute multiply(25, 4)
    T-->>A: Result: 100
    A->>L: Continue with observation
    L-->>A: "The result is 100"
    A-->>U: Final Answer: 100
```

---

## 6. Project Module Dependencies

```mermaid
flowchart BT
    subgraph External["External Dependencies"]
        LG[langgraph]
        LC[langchain-core]
        GG[langchain-google-genai]
    end
    
    subgraph Config["config/"]
        Settings[settings.py]
    end
    
    subgraph Src["src/"]
        subgraph Utils["utils/"]
            Helpers[helpers.py]
        end
        
        subgraph Prompts["prompts/"]
            ReactPrompts[react_prompts.py]
        end
        
        subgraph Tools["tools/"]
            Calculator[calculator.py]
            Search[search.py]
        end
        
        subgraph Agents["agents/"]
            ReactAgent[react_agent.py]
        end
    end
    
    Main[main.py]
    
    ReactAgent --> Tools
    ReactAgent --> Prompts
    ReactAgent --> LG
    ReactAgent --> LC
    ReactAgent --> GG
    Main --> ReactAgent
    Main --> Utils
    Main --> Settings
    
    style External fill:#f5f5f5
    style Src fill:#e3f2fd
```

---

## 7. Message Flow in AgentState

```mermaid
flowchart LR
    subgraph Initial["Initial State"]
        M1["[HumanMessage]"]
    end
    
    subgraph Step1["After Agent Node"]
        M2["[HumanMessage,
        AIMessage+ToolCalls]"]
    end
    
    subgraph Step2["After Tool Node"]
        M3["[HumanMessage,
        AIMessage+ToolCalls,
        ToolMessage(s)]"]
    end
    
    subgraph Final["Final State"]
        M4["[HumanMessage,
        AIMessage+ToolCalls,
        ToolMessage(s),
        AIMessage(Final)]"]
    end
    
    M1 -->|"Agent processes"| M2
    M2 -->|"Tools execute"| M3
    M3 -->|"Agent responds"| M4
    
    style Initial fill:#e1f5fe
    style Final fill:#c8e6c9
```

---

## 8. ReAct vs Traditional Chatbot

```mermaid
flowchart TB
    subgraph Traditional["Traditional Chatbot"]
        T1[User Query] --> T2[LLM]
        T2 --> T3[Response]
    end
    
    subgraph ReAct["ReAct Agent"]
        R1[User Query] --> R2[LLM]
        R2 --> R3{Need Tools?}
        R3 -->|Yes| R4[Execute Tools]
        R4 --> R5[Observe Results]
        R5 --> R2
        R3 -->|No| R6[Response]
    end
    
    style Traditional fill:#ffebee
    style ReAct fill:#e8f5e9
```

---

## 9. Complete Demo Workflow

```mermaid
flowchart TD
    Start([🎬 Start Demo]) --> Setup[📦 Install Dependencies]
    Setup --> Key[🔑 Set API Key]
    Key --> Run[🚀 Run main.py]
    
    Run --> Mode{Select Mode}
    
    Mode -->|--demo| Demo[📋 Demo Queries]
    Mode -->|--query| Single[❓ Single Query]
    Mode -->|default| Interactive[💬 Interactive]
    
    Demo --> Execute[🔄 Execute Agent]
    Single --> Execute
    Interactive --> Execute
    
    Execute --> Stream{Stream Steps?}
    Stream -->|Yes| Steps[📊 Show Each Step]
    Stream -->|No| Direct[📤 Direct Response]
    
    Steps --> Display[🖥️ Display Results]
    Direct --> Display
    
    Display --> More{More Queries?}
    More -->|Yes| Execute
    More -->|No| End([🏁 End])
    
    style Start fill:#c8e6c9
    style End fill:#ffcdd2
```

---

## 10. Class Diagram

```mermaid
classDiagram
    class ReActAgent {
        +tools: List[Tool]
        +llm_with_tools: ChatModel
        +graph: StateGraph
        +system_prompt: str
        +__init__(llm, tools, system_prompt)
        +invoke(query) str
        +stream(query) Iterator
        -_build_graph() StateGraph
        -_agent_node(state) dict
        -_should_continue(state) str
    }
    
    class AgentState {
        +messages: List[BaseMessage]
    }
    
    class Tool {
        +name: str
        +description: str
        +func: Callable
    }
    
    class StateGraph {
        +nodes: Dict
        +edges: List
        +add_node(name, func)
        +add_edge(from, to)
        +compile() CompiledGraph
    }
    
    ReActAgent --> AgentState : manages
    ReActAgent --> Tool : uses
    ReActAgent --> StateGraph : contains
```

---

## Usage Notes

### Rendering Mermaid Diagrams

1. **VS Code**: Install "Mermaid Preview" extension
2. **GitHub**: Diagrams render automatically in markdown
3. **Jupyter**: Use `mermaid` magic or `IPython.display`
4. **Web**: Use [Mermaid Live Editor](https://mermaid.live)

### Copying to Presentations

1. Render diagram in Mermaid Live Editor
2. Export as SVG or PNG
3. Insert into PowerPoint/Google Slides

---

*These diagrams are designed for the ReAct Agent training session.*
