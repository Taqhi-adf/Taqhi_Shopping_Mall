# Taqhi_Shopping_Mall

Industry-style local GenAI retail operations platform using:

- LangChain
- LangChain Tools
- LangGraph
- LangSmith tracing
- Ollama / Qwen3 4B
- FAISS + HuggingFace embeddings
- PDF RAG
- FastAPI
- Streamlit dashboard
- Microsoft SQL Server
- Open-Meteo
- Docker
- GitHub Actions CI/CD

## What this project does

The system combines:

1. SQL Server product catalog
2. Product handling PDF knowledge base
3. Live environmental data from Open-Meteo
4. Deterministic temperature/humidity/pressure/expiry rules
5. LangGraph orchestration
6. Local Ollama LLM explanation
7. FastAPI endpoints
8. Streamlit dashboard
9. Optional LangSmith observability
10. CI/CD through GitHub Actions

## IKEA and LuLu reference

The taxonomy is inspired by public category structures, not copied inventory.

IKEA publicly lists furniture, storage/organisation, kitchens, kitchenware/tableware, textiles, lighting, bathroom, children, outdoor, home decoration and food-related areas. IKEA's Hyderabad store guide also lists showroom and market-hall departments such as living room, dining, kitchen, bedroom, children, cookware, textiles, lighting, rugs, home organisation and food. 

LuLu Mall publicly lists categories such as beauty & wellness, restaurants/cafes, kids wear, footwear/bags, home/lifestyle, sports, travel luggage, mobile/electronics, books/gifts, food court, health/wellness, jewellery, toys and fashion. LuLu Hypermarket publicly lists grocery, dairy/bakery, frozen foods, electronics, home & kitchen, baby care and other categories.

The product catalog in this project is synthetic.

## Prerequisites

Windows 11:
- Python 3.10+
- Microsoft SQL Server Express/Developer
- SQL Server Management Studio
- ODBC Driver 18 for SQL Server
- Ollama
- Git
- Optional Docker Desktop

## Installation

```powershell
cd C:\Users\DELL\Desktop
# Extract this folder here
cd Taqhi_Shopping_Mall

python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Copy `.env.example` to `.env`.

For SQL Express:

```env
SQL_SERVER=localhost\SQLEXPRESS
SQL_DATABASE=TaqhiShoppingMall
SQL_TRUSTED_CONNECTION=yes
```

## Start Ollama

```powershell
ollama pull qwen3:4b
ollama run qwen3:4b
```

## SQL Server

```powershell
python setup_database.py
```

Then execute these in SSMS:

```text
sql/schema.sql
sql/seed.sql
```

## Product PDF

```powershell
python create_product_pdf.py
```

## Build RAG

```powershell
python build_rag.py
```

This creates `rag_store/`.

## Run FastAPI

```powershell
uvicorn api.main:app --reload --port 8000
```

Open:

```text
http://127.0.0.1:8000/docs
```

Endpoints:

- GET `/health`
- GET `/weather`
- GET `/products`
- GET `/products/{product_id}`
- POST `/ask`

Example:

```json
{
  "question": "Is GROC-001 within its documented environmental limits under the current weather?"
}
```

## Run dashboard

```powershell
streamlit run app/streamlit_app.py
```

## Run CLI

```powershell
python main.py
```

## LangSmith

Optional:

```env
LANGSMITH_TRACING=true
LANGSMITH_API_KEY=your_key
LANGSMITH_PROJECT=Taqhi_Shopping_Mall
```

Never commit the API key.

## Tests

```powershell
pytest -q
ruff check .
```

## Docker

```powershell
docker build -t taqhi-shopping-mall:latest .
docker run --rm -p 8501:8501 taqhi-shopping-mall:latest
```

## CI/CD

Push to GitHub. `.github/workflows/ci.yml` runs Ruff, tests and Python compilation.

Create a release:

```powershell
git tag v1.0.0
git push origin v1.0.0
```

The CD workflow builds and publishes the Docker image to GitHub Container Registry.

## Safety

The demo limits are synthetic. Real product storage, expiry, food-safety, electrical and chemical requirements must come from approved manufacturer/supplier documentation, labels, SDS documents and validated procedures.
