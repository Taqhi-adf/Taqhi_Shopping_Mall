# Architecture

```text
                         User
                           |
                 +---------+---------+
                 |                   |
                 v                   v
          Streamlit Dashboard     FastAPI
                 |                   |
                 +---------+---------+
                           |
                       LangGraph
                           |
          +----------------+----------------+
          |                |                |
          v                v                v
      SQL Tool        Weather Tool       RAG Tool
          |                |                |
          v                v                v
      SQL Server       Open-Meteo       PDF + FAISS
          |                |                |
          +----------------+----------------+
                           |
                           v
                   Deterministic Rules
                           |
                           v
                       Ollama
                       Qwen3 4B
                           |
                           v
                    Human-readable answer

LangSmith can trace LangChain/LangGraph runs when enabled.
```

The LLM explains evidence; Python rules perform environmental comparisons.
