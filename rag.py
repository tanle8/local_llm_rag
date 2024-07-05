from langchain_community.vectorstores.chroma import Chroma
from langchain_community.chat_models.ollama import ChatOllama
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
from langchain.schema.output_parser import StrOutputParser
from langchain_community.document_loaders.pdf import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema.runnable import RunnablePassthrough
from langchain.prompts import PromptTemplate
from langchain_community.vectorstores.utils import filter_complex_metadata


class ChatPDF:
    vector_store = None
    retriever = None
    chain = None

    def __init__(self):
        """
        Initialize the chat model (ChatOllama), a text splitter, and a prompt
        template. This set up the basic components needed for processing PDF
        contents and generating responses.
        """
        MODEL = "llama2:latest"
        self.model = ChatOllama(model=MODEL)
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=1024,
                                                            chunk_overlap=100)
        self.prompt = PromptTemplate.from_template(
            """
            [INST]<<SYS>> You are an assistant for question-answering tasks.
            Use the following pieces of retrieved context to answer the question.
            If you don't know the answer, just say that you don't know. 
            Make a long, comprehensive answer.<</SYS>> 
            Question: {question}
            Context: {context} 
            Answer: [/INST]
            """
        )

    def ingest(self, pdf_path):
        """
        PDF Ingestion:
        - Load the PDF document, splits it into chunks,
        - Filters metadata from the chunks to simplify them.
        - Creates a `Chroma` vector store from these chunks using
        `FastEmbedEmbeddings` for embedding generation.
        - Sets up a retriever on the vector store for finding relevant content
        based on similarity.
        """
        docs = PyPDFLoader(file_path=pdf_path).load()
        chunks = self.text_splitter.split_documents(docs)
        chunks = filter_complex_metadata(chunks)

        vector_store = Chroma.from_documents(documents=chunks,
                                             embedding=FastEmbedEmbeddings())
        self.retriever = vector_store.as_retriever(
            search_type="similarity_score_threshold",
            search_kwargs={
                'k': 3,
                'score_threshold': 0.5
            },
        )

        self.chain = ({
                          "context": self.retriever,
                          "question": RunnablePassthrough()
                      }
                      | self.prompt
                      | self.model
                      | StrOutputParser()
                      )

    def ask(self, query: str):
        """
        Query handling:
        - If a PDF has been processed (self.chain is set up), it takes a query,
        processes it through the setup chain (context retrival, prompt
        formation, model querying, and output parsing), and returns the
        response.
        - IF no PDF is processed, it advises the user to upload a document first.
        """
        if not self.chain:
            return "Please ingest a PDF file first."
        return self.chain.invoke(query)

    def clear(self):
        """
        Clear state: Resets the state of the ChatPDF instance, clearing any
        loaded data and retriever setup.
        """
        self.vector_store = None
        self.retriever = None
        self.chain = None
