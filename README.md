# Local RAG: Langchain + Ollama + ChromaDB Streamlit

Build your own RAG and run it locally and free.

## Setups

- Install Ollama from `https://ollama.ai/`
- Pull the `llama2:latest` model on Ollama using the command `ollama pull llama2:latest`
- Create venv using `python3 -m venv .venv`
- Install the requirements using `pip install -r requirements.txt`
- Run the streamlit app using `streamlit run main.py`

## Project Structure
- main.py: The main entry point for the Streamlit application.
- rag.py
- requirements.txt: Lists all the required Python packages.
- README.md: This file, containing setup instructions and project overview.

## How It Works
- Document Ingestion: Upload a PDF document via the Streamlit app. The system processes the document, splitting it into manageable chunks and filtering metadata.
- Vector Store Creation: The chunks are embedded using FastEmbedEmbeddings and stored in ChromaDB, enabling efficient similarity searches.
- Query Processing: Enter a query in the Streamlit app. The system retrieves relevant document chunks from ChromaDB based on their similarity to the query.
- Answer Generation: The retrieved chunks are fed into the Ollama language model (llama2) to generate a comprehensive response to the query.

## Benefits
- Local and Free: Run the entire system locally without any cloud dependencies or costs.
- Interactive UI: The Streamlit app provides an easy-to-use interface for uploading documents and querying.
- State-of-the-Art Model: Leverage the power of the latest llama2 model for high-quality text generation.

## Troubleshooting
- Ensure that Ollama is properly installed and the llama2:latest model is pulled before running the application.
- Verify that the virtual environment is activated before installing the requirements and running the app.
- Check for any error messages in the terminal and address any missing dependencies or incorrect paths.
