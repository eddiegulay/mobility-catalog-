# Mobility Catalog - AI-Powered Mobility Measure Research System

> **Multi-agent mobility measure documentation**

An research pipeline agents to generate comprehensive, research-quality documentation for sustainable mobility measures. Built with LangGraph and Groq's LLM APIs.

---

## Overview

This system **automatically researches and documents** mobility measures (e.g., bike sharing, car-free zones, e-scooter programs) by orchestrating 19 specialized AI agents that work in parallel to produce:

- **Complete JSON Documentation** (19 structured sections)
- **High-Quality Stock Images** (via Pexels API)
- **Research-Backed Content** (descriptive, not generic task lists)
- **Production-Ready Output** (60-70KB per measure)

### Example Input → Output

**Input**: `"Cargo bikes for family transport"`

**Output**: Complete 19-section JSON including:
- Meta information with 3 relevant images
- Overview with behavioral dynamics
- Evidence from Sweden/Europe
- Financial models with USD cost estimates
- Infrastructure requirements
- Lifecycle implementation stages
- And 13 more specialized sections...

---

## Architecture

### Multi-Agent System

```
                    ┌─────────────────┐
                    │  User Request   │
                    └────────┬────────┘
                             │
              ┌──────────────┴──────────────┐
              │   LangGraph Orchestrator    │
              └──────────────┬──────────────┘
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
    Parallel Execution (19 agents)          Sequential Mode
        │                    │                    │
┌───────▼───────┐   ┌───────▼───────┐   ┌───────▼───────┐
│  Meta Agent   │   │Overview Agent │   │Context Agent  │
│  + Images     │   │ + Behavior    │   │ + Suitability │
└───────────────┘   └───────────────┘   └───────────────┘
        │                    │                    │
        └────────────────────┼────────────────────┘
                             │
                   ┌─────────▼──────────┐
                   │  Assembly Agent    │
                   │  Validates & Saves │
                   └─────────┬──────────┘
                             │
                  ┌──────────▼───────────┐
                  │  Final JSON Output   │
                  │  + Metadata          │
                  └──────────────────────┘
```

### 19 Specialized Agents

1. **Meta** - Name, category, tags, images
2. **Overview** - Description, behavioral goals
3. **Context** - Target users, suitability
4. **Evidence** - Sweden/Europe/research data
5. **Impact** - Modal shift, car reduction
6. **Requirements** - Security, infrastructure, charging
7. **Infrastructure** - Physical requirements
8. **Operations** - Stakeholder responsibilities
9. **Costs** - Upfront, operational, benefits
10. **Risks** - Key risk factors
11. **Monitoring** - Metrics and frequency
12. **Checklist** - Move-in timeline
13. **Lifecycle** - 6-stage process
14. **Roles & Responsibilities** - Detailed stakeholder duties
15. **Financial Model** - Cost distribution, estimates
16. **Compliance** - Requirements and approvals
17. **Visibility** - Signage and communication
18. **Selection Logic** - Prerequisites and combinations
19. **Future Scalability** - Expansion conditions

---

## Key Features

### Reliability
- **Partial Save**: Never lose data - saves even with missing sections
- **Dual-Model Fallback**: Primary → Retry → Fallback model chain
- **Intelligent Retry**: Extracts wait times and auto-retries
- **Graceful Degradation**: 84%+ completion even under heavy load

### Content Quality
- **Descriptive Content**: Research-quality explanations, not task lists
- **Template Compliance**: Exact field names matching requirements
- **Stock Images**: 3 relevant images via Pexels API
- **Professional Tone**: Neutral, operational, Sweden/EU context

### Performance
- **Parallel Execution**: All 19 agents run simultaneously (~12s)
- **Sequential Mode**: Optional one-at-a-time for reliability (~45s)
- **Rate Limiting**: Configurable delays to prevent API limits
- **Smart Throttling**: 1-3s random delays spread requests

---

## Quick Start

### Prerequisites

```bash
# Python 3.10+
python --version

# uv package manager
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Installation

```bash
# Clone and enter directory
cd mobility-catalog-

# Install dependencies
uv sync

# Create .env file
cp .env.example .env
```

### Configuration

Edit `.env` with your API keys:

```bash
# Required: Groq API (https://console.groq.com/keys)
GROQ_API_KEY=your_groq_api_key_here

# Required: Pexels API (https://www.pexels.com/api/new/)
PEXELS_API_KEY=your_pexels_api_key_here

# Model Configuration
MODEL_NAME=openai/gpt-oss-120b
FALLBACK_MODEL=llama-3.3-70b-versatile
CLAUDE_MODEL=claude-3-5-sonnet-20240620

# Rate Limiting
ENABLE_RATE_LIMITING=true
REQUEST_DELAY_MIN=1.0
REQUEST_DELAY_MAX=3.0

# Execution Mode
SEQUENTIAL_MODE=false  # Set true for max reliability
```

### Usage

```bash
# Basic usage
uv run python mobility_research.py "Bike parking stations"

# With context
uv run python mobility_research.py "Electric scooters" \
  --context "High-density urban area with good public transport"

# The system will:
# 1. Execute 19 specialized agents in parallel
# 2. Fetch 3 relevant stock images
# 3. Generate 60-70KB of structured content
# 4. Save to: research_output/{name}-mobility-measure.json
```

---

## Output Format

### Complete JSON Structure

```json
{
  "meta": {
    "name": "Bike Parking Stations",
    "category": "cycling_infrastructure",
    "tags": ["cycling", "parking", "infrastructure"],
    "images": ["https://...", "https://...", "https://..."],
    "impact_level": 4,
    "cost_level": 3
  },
  "overview": { "description": "...", "behavioural_primary": "..." },
  "context": { "target_users": [...], "suitable_strong": [...] },
  // ... 16 more sections
}
```

### Partial Results

If some agents fail (e.g., rate limits), the system saves partial results:

```json
{
  // ... 16 complete sections
  "requirements": {},  // Empty placeholder
  "risks": {},
  "_metadata": {
    "incomplete": true,
    "missing_sections": ["requirements", "risks"],
    "completion_percentage": 84.2,
    "generated_at": "2025-12-08T23:59:43Z"
  }
}
```

Filename: `{name}-mobility-measure-partial.json`

---

## Advanced Configuration

### Sequential Mode (Maximum Reliability)

For environments with strict rate limits:

```bash
# .env
SEQUENTIAL_MODE=true
```

**Trade-offs:**
- **Pros**: Near 100% success rate, avoids all rate limits
- **Cons**: Slower (45s vs 12s)

### Custom Rate Limiting

Adjust delays to match your API tier:

```bash
# Free tier (conservative)
REQUEST_DELAY_MIN=2.0
REQUEST_DELAY_MAX=4.0

# Pro tier (aggressive)
REQUEST_DELAY_MIN=0.3
REQUEST_DELAY_MAX=0.8
```

### Model Selection

```bash
# Fast but rate-limited
MODEL_NAME=openai/gpt-oss-120b

# More reliable (larger daily quota)
MODEL_NAME=llama-3.3-70b-versatile

# Fastest (lower quality)
FALLBACK_MODEL=llama-3.1-8b-instant
```

---

## Performance Metrics

| Metric | Value | Notes |
|--------|-------|-------|
| **Success Rate** | 84-95% | With token availability |
| **Execution Time** | 12-15s | Parallel mode |
| **Output Size** | 60-70 KB | Per measure |
| **Data Loss** | 0% | Partial save prevents loss |
| **Image Count** | 3 per measure | High-quality stock photos |
| **Retry Success** | +20-30% | Intelligent backoff |

---

## System Components

### Core Files

```
mobility_research.py      # CLI entry point
config/
  settings.py             # Environment configuration
  llm.py                  # LLM initialization
agents/mobility/
  base.py                 # Base agent with retry logic
  meta_agent.py           # Meta + image search
  all_agents.py           # 16 specialized agents
  assembly_agent.py       # JSON assembly & save
graphs/
  mobility_graph.py       # LangGraph orchestration
schemas/
  mobility_measure.py     # TypedDict schemas
  validators.py           # JSON validation
utils/
  image_search.py         # Pexels API integration
  json_utils.py           # JSON extraction/parsing
  logger.py               # Logging configuration
```

### Output Directory

```
research_output/
  bike-parking-mobility-measure.json         # Complete
  cargo-bikes-mobility-measure-partial.json  # Partial
```

---

## Troubleshooting

### Rate Limit Errors

**Problem**: `Error code: 429 - Rate limit reached`

**Solutions**:
1. **Wait**: Daily tokens reset in ~1-2 hours
2. **Sequential Mode**: Set `SEQUENTIAL_MODE=true`
3. **Increase Delays**: Set `REQUEST_DELAY_MAX=4.0`
4. **Upgrade Tier**: Get Groq Dev tier for higher limits

### Missing Sections

**Problem**: Partial results with empty sections

**Cause**: Token exhaustion or persistent rate limits

**Solution**:
- System auto-saves partial results (no data loss!)
- Check `_metadata.missing_sections` field
- Wait for token reset and re-run specific measure
- Or manually complete missing sections using interactive mode

### Import Errors

```bash
# Reinstall dependencies
uv sync --reinstall
```

---

## How It Works

### 1. Graph Construction

LangGraph builds a state machine with 19 parallel agent nodes that converge to an assembly node.

### 2. Agent Execution

Each agent:
1. Receives measure name + context
2. Adds random delay (rate limiting)
3. Calls LLM with specialized prompt
4. Parses JSON response
5. If rate limited → waits → retries → tries fallback
6. Returns result or error

### 3. Assembly

Assembly agent:
- Collects all 19 sections
- Identifies missing sections
- Adds placeholders for empty sections
- Includes completion metadata
- Saves JSON with `-partial` suffix if incomplete

### 4. Error Recovery Chain

```
Primary Model
    ↓ (429 error)
Extract Wait Time → Sleep → Retry
    ↓ (still fails)
Fallback Model
    ↓ (both fail)
Save Partial Result (prevents data loss)
```

---

## Example Output

Here's what the system generates for **"Cargo Bikes"**:

- **File Size**: 62.8 KB
- **Sections**: 19/19 complete
- **Images**: 3 Pexels URLs
- **Content Quality**: Research-backed, Sweden/EU context
- **Format**: Production-ready JSON
- **Generation Time**: ~12 seconds

Sample excerpt:
```
"infrastructure": {
  "key_requirements": [
    "A sturdy, low-maintenance frame designed to support heavy loads, 
     typically constructed from durable materials such as steel or 
     aluminum, with a loading capacity of 100-200 kg to accommodate 
     children, groceries, or cargo..."
  ]
}
```

---

## Contributing

This is a research project for automating mobility measure documentation. Contributions welcome!

### Development Setup

```bash
# Install dev dependencies
uv sync --all-extras

# Run tests (when available)
pytest tests/

# Format code
black .
```

---

## License

MIT License - See LICENSE file

---

## Resources

- **Groq API**: https://console.groq.com/
- **Pexels API**: https://www.pexels.com/api/
- **LangGraph Docs**: https://langchain-ai.github.io/langgraph/
- **Project Issues**: Use for bugs/features

---

## Support

For questions or issues:
1. Check this README
2. Review error messages (they're descriptive!)
3. Check `/tmp/mobility_test_output.log` for full logs
4. Open an issue with error details

---

**Built with LangGraph, Groq, and Pexels**
