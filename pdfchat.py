import streamlit as st
from PyPDF2 import PdfReader
from langchain_text_splitters import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import faiss
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import openai
from langchain.callbacks import get_openai_callback
def main():
    st.set_page_config(page_title="ChatToPDF")
    st.header("ChatToPDF")
    
    pdf = st.file_uploader("Upload a PDF", type="pdf")
    
    if pdf is not None:
        pdf_reader = PdfReader(pdf)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text   
            
        text_splitter = CharacterTextSplitter(
            separator="\n",
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len
        )
        
        chunks = text_splitter.split_text(text)
        embeddings = OpenAIEmbeddings()
        knowledge_base = faiss.FAISS.from_texts(chunks,embeddings)
        
        user_question=st.text_input("Ask a question about your PDF: ")
        
        if user_question:
            docs = knowledge_base.similarity_search(user_question)
            llm = openai.OpenAI(api_key="")
            chain = load_qa_chain(llm,chain_type="stuff")
            with get_openai_callback() as cb:
                response = chain.run(input_docs=docs,question=user_question)
                print(cb)
        st.write(response)
            
main()
    
