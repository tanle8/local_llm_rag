Local RAG: Langchain + Ollama + ChromaDB Streamlit
This project demonstrates how to build and run a Retrieval-Augmented Generation (RAG) system locally and for free using Langchain, Ollama, and ChromaDB. The system leverages the llama2:latest model from Ollama to provide powerful natural language understanding and generation capabilities.

Overview
Retrieval-Augmented Generation (RAG) is a powerful approach that combines the strengths of information retrieval and text generation. In this project, we use Langchain to handle the document processing and querying, Ollama for the language model, and ChromaDB as the vector database for efficient similarity searches. The entire setup is wrapped in a Streamlit application, providing an interactive and user-friendly interface.

Setup Instructions
Follow these steps to set up and run the project on your local machine:

1. Install Ollama
Ollama is a platform that provides access to state-of-the-art language models. Install Ollama by following the instructions on their official website.

2. Pull the llama2:latest Model
Once Ollama is installed, you need to pull the llama2:latest model. Open your terminal and run the following command:

sh
Copy code
ollama pull llama2:latest
This command will download the latest version of the llama2 model, which will be used for text generation.

3. Create a Virtual Environment
It's recommended to create a virtual environment to manage the project's dependencies. Run the following command to create a virtual environment:

sh
Copy code
python3 -m venv .venv
4. Activate the Virtual Environment
Activate the virtual environment using the appropriate command for your operating system:

For Windows:

sh
Copy code
.venv\Scripts\activate
For macOS/Linux:

sh
Copy code
source .venv/bin/activate
5. Install the Requirements
With the virtual environment activated, install the required Python packages using the provided requirements.txt file:

sh
Copy code
pip install -r requirements.txt
6. Run the Streamlit Application
Finally, start the Streamlit application by running:

sh
Copy code
streamlit run main.py
This command will launch the Streamlit app, and you should see a URL in the terminal. Open this URL in your web browser to interact with the RAG system.

Project Structure
main.py: The main entry point for the Streamlit application.
requirements.txt: Lists all the required Python packages.
README.md: This file, containing setup instructions and project overview.
How It Works
Document Ingestion: Upload a PDF document via the Streamlit app. The system processes the document, splitting it into manageable chunks and filtering metadata.
Vector Store Creation: The chunks are embedded using FastEmbedEmbeddings and stored in ChromaDB, which facilitates efficient similarity searches.
Query Processing: Enter a query in the Streamlit app. The system retrieves relevant document chunks from ChromaDB based on their similarity to the query.
Answer Generation: The retrieved chunks are fed into the Ollama language model (llama2) to generate a comprehensive response to the query.
Benefits
Local and Free: Run the entire system locally without any cloud dependencies or costs.
Interactive UI: The Streamlit app provides an easy-to-use interface for uploading documents and querying.
State-of-the-Art Model: Leverage the power of the latest llama2 model for high-quality text generation.
