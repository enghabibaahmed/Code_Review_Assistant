# AI Code Review Assistant

An AI assistant that reviews Python code and suggests improvements.
It uses RAG (best-practice docs), chains, an agent and a structured output parser.

## How it works
1. The user pastes Python code in a Streamlit app.
2. The backend (a Kaggle notebook running Mistral Nemo) analyzes the code,
   detects issues using the knowledge base, and suggests fixes.
3. Results are shown as: File, Issue, Severity, Explanation, Suggested Fix.

## Tools
Kaggle, ngrok, Streamlit, VS Code, GitHub, Mistral Nemo, LangChain

## Project files
- `notebook.ipynb`: backend (model, RAG, chains, agent)
- `app.py`: Streamlit user interface
- `knowledge_base/`: documentation and best-practice rules

## How to run
1. Run `notebook.ipynb` on Kaggle (GPU on, Internet on).
2. Copy the ngrok URL it prints.
3. Run the app: `streamlit run app.py`