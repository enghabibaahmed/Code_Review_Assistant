# AI Code Review Assistant

An AI assistant that reviews Python code and suggests improvements.
It uses RAG over best-practice documentation, three chains and a structured output parser.

## How it works
1. The user pastes or uploads Python code in a Streamlit app.
2. The backend (a Kaggle notebook running Mistral Nemo) does three steps:
   - **Analyze code**: summarizes what the code does
   - **Detect issues**: retrieves the matching rules (RAG) and checks the code against them
   - **Suggest improvements**: writes the explanation and fix, using PEP 8 / PEP 257 / OWASP documentation (RAG)
3. The output parser returns: **File, Issue, Severity, Explanation, Suggested Fix**.

## Tools
Kaggle, ngrok, Streamlit, VS Code, GitHub, Mistral Nemo, LangChain, FAISS, sentence-transformers

## Project files
- `notebook.ipynb`: backend (model, RAG, chains, parser, API)
- `app.py`: Streamlit user interface
- `knowledge_base/my_rules.md`: my own coding rules with severities

The PEP 8, PEP 257 and OWASP documents are downloaded by the notebook.

## How to run
1. Open `notebook.ipynb` on Kaggle (GPU T4 x2 on, Internet on, `NGROK_TOKEN` secret added) and run all cells.
2. Copy the public URL printed by the ngrok cell.
3. Run the app: `pip install -r requirements.txt` then `streamlit run app.py`
4. Paste the URL in the sidebar, add code and click **Review code**.

## Limitations
- Python code only.
- The model can make mistakes: it may report a false issue or miss one.
- The ngrok URL changes every time the notebook restarts.
- Reviews take a few minutes because the model runs on a free Kaggle GPU.