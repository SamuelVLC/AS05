# Samuel Lobo Chiodi
# 30/11/2024

#-------------------------------------------------------------------------------------------------------------------------- Extract data from pdf
import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings, HuggingFaceInstructEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from htmlTemplates import css, bot_template, user_template
from langchain.llms import HuggingFaceHub
#-------------------------------------------------------------------------------------------------------------------------- Extract data from pdf
def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

#-------------------------------------------------------------------------------------------------------------------------- Other functions and Open AI key instance
def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks


def get_vectorstore(text_chunks):
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    return vectorstore


def get_conversation_chain(vectorstore):
    llm = ChatOpenAI()
    
    memory = ConversationBufferMemory(
        memory_key='chat_history', return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory
    )
    return conversation_chain

#-------------------------------------------------------------------------------------------------------------------------- User input
def handle_userinput(user_question):
    response = st.session_state.conversation({'question': user_question})
    st.session_state.chat_history = response['chat_history']

    for i, message in enumerate(st.session_state.chat_history):
        if i % 2 == 0:
            st.write(user_template.replace(
                "{{MSG}}", message.content), unsafe_allow_html=True)
        else:
            st.write(bot_template.replace(
                "{{MSG}}", message.content), unsafe_allow_html=True)

#-------------------------------------------------------------------------------------------------------------------------- Main function
def main():
    load_dotenv()
    st.set_page_config(page_title="PDF Genie", page_icon=":magic_wand: :page_facing_up:")
    st.write(css, unsafe_allow_html=True)

    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None

    st.title("PUC MINAS - Tópicos 3")  # Title
    st.header('Engenharia de Computação | 2/2024')
    st.header(':blue[PDF Genie] :magic_wand: :page_facing_up:')
    st.text("Tópicos em Computação III \nProf.: Wladmir Cardoso Brandão\nAluno: Samuel Lobo Chiodi\n")
    st.text("Este é um assistente baseado em LLM capaz de indexar vetores de uma coleção de \ndocumentos PDF que responde perguntas feitas sobre os arquivos lidos")
    user_question = st.text_input("Faça uma pergunta sobre os PDFs enviados:")
    if user_question:
        handle_userinput(user_question)
#----------------------------------------------------------------------------------------------------------------------- PDFs processing
    with st.sidebar:
        st.subheader("Importar documentos")
        pdf_docs = st.file_uploader(
            "Envie seus PDFs aqui e clique em 'Processar'", accept_multiple_files=True)
        if st.button("Processar"):
            with st.spinner("Processando..."):
                raw_text = get_pdf_text(pdf_docs)
                text_chunks = get_text_chunks(raw_text)
                vectorstore = get_vectorstore(text_chunks)
                st.session_state.conversation = get_conversation_chain(
                    vectorstore)

if __name__ == '__main__':
    main()
