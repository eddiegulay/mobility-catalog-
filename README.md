# LangGraph Research Agent

A clean, expandable LangGraph project for building AI research agents using **LangChain**, **LangGraph**, and **Groq** as the LLM backend.

## 🌟 Features

- **Modular Architecture**: Clean separation of concerns with dedicated modules for agents, graphs, config, and utilities
- **State Management**: Proper LangGraph state handling with TypedDict schemas
- **Graph Orchestration**: Well-defined workflow with nodes and edges
- **Groq Integration**: Fast LLM inference using Groq's API
- **Extensible Design**: Easy to add new agents and workflows
- **Type Safety**: Full type hints throughout the codebase

## 📁 Project Structure

```
.
├── config/
│   ├── settings.py       # Environment configuration
│   └── llm.py           # Groq LLM initialization
├── agents/
│   └── research_agent.py # Research agent implementation
├── graphs/
│   └── research_graph.py # LangGraph workflow definition
├── utils/
│   ├── logger.py        # Logging utilities
│   └── formatting.py    # Output formatting helpers
├── main.py              # Application entrypoint
├── pyproject.toml       # uv dependency configuration
├── .env.example         # Environment template
└── README.md           # This file
```

## 🚀 Quick Start

### Prerequisites

- Python 3.11 or higher
- [uv](https://github.com/astral-sh/uv) package manager
- Groq API key ([get one here](https://console.groq.com/keys))

### Installation

1. **Install uv** (if you haven't already):
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. **Clone or navigate to the project**:
   ```bash
   cd /path/to/mobility-catalog-
   ```

3. **Create your `.env` file**:
   ```bash
   cp .env.example .env
   ```

4. **Add your Groq API key to `.env`**:
   ```bash
   # Edit .env and add:
   GROQ_API_KEY=your_actual_api_key_here
   ```

5. **Install dependencies**:
   ```bash
   uv sync
   ```

### Usage

**Interactive Mode (Recommended)** - Ask multiple questions in a conversation:
```bash
uv run python interactive.py
```

This starts an interactive session where you can:
- Ask multiple research questions
- See formatted responses immediately
- Continue asking without restarting
- Type `quit` or press Ctrl+C to exit

**Single Query Mode** - For one-off questions:
```bash
uv run python main.py "What are the key benefits of LangGraph for building AI agents?"
```

**Or run main.py interactively**:
```bash
uv run python main.py
# Then enter your query when prompted
```

### Example Output

**Interactive Mode:**
```
🔍 Your Question: What are the key benefits of LangGraph?

🤔 Researching... (Query #1)

📝 Summary:
------------------------------------------------------------
LangGraph provides a powerful framework for building stateful 
AI agents with explicit control flow, enabling complex multi-step 
reasoning and tool integration.

✨ Key Points:
------------------------------------------------------------
1. Graph-based architecture allows for complex, non-linear workflows
2. State management through typed schemas ensures data consistency
3. Conditional edges enable dynamic decision-making
4. Built-in integration with LangChain ecosystem

📚 Sources:
------------------------------------------------------------
LLM Query Analysis, LLM Research Database, LLM Synthesis Engine
```

**JSON Mode (main.py):**
```json
{
  "query": "What are the key benefits of LangGraph for building AI agents?",
  "summary": "LangGraph provides a powerful framework for building stateful AI agents with explicit control flow, enabling complex multi-step reasoning and tool integration.",
  "key_points": [
    "State management through typed schemas ensures data consistency",
    "Graph-based architecture allows for complex, non-linear workflows",
    "Conditional edges enable dynamic decision-making during execution",
    "Built-in integration with LangChain ecosystem"
  ],
  "sources_consulted": [
    "LLM Query Analysis",
    "LLM Research Database",
    "LLM Synthesis Engine"
  ]
}
```

## 🧠 How It Works

### Research Agent Workflow

The research agent follows a three-stage pipeline:

1. **Analyze Query** (`analyze_query_node`)
   - Examines the user's query
   - Identifies key research aspects
   - Creates internal notes for guidance

2. **Research** (`research_node`)
   - Uses the Groq LLM to gather information
   - Generates comprehensive findings
   - Updates internal research notes

3. **Synthesize** (`synthesize_node`)
   - Consolidates research findings
   - Creates a concise summary
   - Extracts key points
   - Formats output as structured JSON

### State Management

The agent uses a `ResearchState` TypedDict:
```python
class ResearchState(TypedDict):
    query: str                    # User's research question
    summary: str                  # Synthesized summary
    key_points: list[str]         # Key findings
    sources_consulted: list[str]  # Information sources
    internal_notes: str           # Intermediate processing
```

### Graph Structure

```
START → analyze_query → research → synthesize → END
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `GROQ_API_KEY` | Your Groq API key | *Required* |
| `MODEL_NAME` | Groq model to use | `llama-3.3-70b-versatile` |
| `TEMPERATURE` | LLM temperature | `0.7` |
| `MAX_TOKENS` | Maximum tokens per response | `2048` |
| `DEBUG` | Enable debug logging | `false` |

### Available Models

- `llama-3.3-70b-versatile` (default, recommended)
- `mixtral-8x7b-32768`
- `llama-3.1-70b-versatile`
- See [Groq Models](https://console.groq.com/docs/models) for more options

## 📦 Adding New Agents

The project is designed for easy expansion. To add a new agent:

1. **Create a new agent file** in `agents/`:
   ```python
   # agents/my_new_agent.py
   from typing import TypedDict
   
   class MyAgentState(TypedDict):
       # Define your state schema
       pass
   
   def my_node(state: MyAgentState) -> MyAgentState:
       # Implement your node logic
       pass
   ```

2. **Create a new graph** in `graphs/`:
   ```python
   # graphs/my_new_graph.py
   from langgraph.graph import StateGraph, START, END
   from agents.my_new_agent import MyAgentState, my_node
   
   workflow = StateGraph(MyAgentState)
   workflow.add_node("my_node", my_node)
   workflow.add_edge(START, "my_node")
   workflow.add_edge("my_node", END)
   
   my_graph = workflow.compile()
   ```

3. **Update `main.py`** to use the new agent (or create a separate entrypoint)

## 🐛 Troubleshooting

### "GROQ_API_KEY is required"
- Ensure you've created a `.env` file from `.env.example`
- Add your Groq API key to the `.env` file
- Verify the file is in the project root directory

### Import Errors
- Run `uv sync` to ensure all dependencies are installed
- Check that you're using Python 3.11 or higher: `python --version`

### Slow Response Times
- Consider using a smaller model for faster responses
- Reduce `MAX_TOKENS` in your `.env` file

## 📚 Resources

- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [LangChain Documentation](https://python.langchain.com/)
- [Groq Documentation](https://console.groq.com/docs)
- [LangGraph Tutorials](https://langchain-ai.github.io/langgraph/tutorials/)

## 📄 License

This project follows the same license as the parent repository.

## 🤝 Contributing

This is a starter template designed to be customized for your specific needs. Feel free to:
- Add new agents for different research domains
- Implement tool integration (web search, database queries, etc.)
- Add conditional edges for smarter routing
- Create multi-agent systems with subgraphs

---

**Built with LangGraph 🦜 | Powered by Groq ⚡**
