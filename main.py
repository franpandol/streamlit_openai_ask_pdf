import os
import logging
from dotenv import load_dotenv
from PyPDF2 import PdfReader
import streamlit as st
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
from langchain.callbacks import get_openai_callback

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.environ['OPENAI_API_KEY']  # Fails fast if not set

# Lazy loading of resources
llm = None
chain = None

def get_chain():
    """Lazy load and return the chain."""
    global chain
    if chain is None:
        llm = OpenAI()  # Local variable, as it's not needed outside this function
        chain = load_qa_chain(llm, chain_type='stuff')
    return chain

def extract_text_from_pdf(pdf):
    """Extract text from the provided PDF file."""
    try:
        pdf_reader = PdfReader(pdf)
    except:
        st.error("Failed to extract text from PDF. Please upload a valid PDF file.")
        return None

    text = ""
    for page in pdf_reader.pages:
        page_text = page.extract_text()
        if page_text is not None:
            text += page_text
    return text

def process_text(text):
    """Process the extracted text and split it into chunks."""
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks

def create_knowledge_base(chunks):
    """Create and save the knowledge base from text chunks."""
    embeddings = OpenAIEmbeddings()
    knowledge_base = FAISS.from_texts(chunks, embeddings)
    knowledge_base.save_local("faiss_index")
    return knowledge_base

def main():
    st.title("Chat with your PDF")
    pdf = st.file_uploader('Upload your PDF Document', type='pdf')
    
    if pdf is not None:
        text = extract_text_from_pdf(pdf)
        if text is None:
            return  # Stop if text extraction failed

        chunks = process_text(text)
        knowledge_base = create_knowledge_base(chunks)

        query = st.text_input('Ask a question to the PDF')
        cancel_button = st.button('Cancel')
        
        if cancel_button:
            st.stop()
        
        if query:
            chain = get_chain()  # Load resources
            with st.spinner('Processing your question...'):
                docs = knowledge_base.similarity_search(query)
                with get_openai_callback() as cost:
                    response = chain.run(input_documents=docs, question=query)
                    logger.info(f"Cost: {cost}")
                st.write(response)

if __name__ == "__main__":
    main()
