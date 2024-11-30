import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import google.generativeai as genai
from langchain_community.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])  # Ensure this line is added to set your API key

# -------------------------------------------------------------------------------------------------------------------------- Extract data from pdf
def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

# -------------------------------------------------------------------------------------------------------------------------- Other functions and OpenAI key instance
def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
    chunks = text_splitter.split_text(text)
    return chunks

def get_vectorstore(text_chunks):
    embeddings = GoogleGenerativeAIEmbeddings(model = "models/embedding-001")
    vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
    vector_store.save_local("faiss_index")

def get_conversational_chain():
    prompt_template = """
    Answer the question as detailed as possible from the provided context, make sure to provide all the details, if the answer is not in
    provided context just say, "answer is not available in the context", don't provide the wrong answer\n\n
    Context:\n {context}?\n
    Question: \n{question}\n

    Answer:
    """

    model = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.3)

    prompt = PromptTemplate(template = prompt_template, input_variables = ["context", "question"])
    chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)

    return chain

# -------------------------------------------------------------------------------------------------------------------------- User input
def handle_userinput(user_question):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    
    # Verificar se os PDFs estão na sessão
    if "pdf_docs" in st.session_state:
        pdf_docs = st.session_state.pdf_docs
        raw_text = get_pdf_text(pdf_docs)
        text_chunks = get_text_chunks(raw_text)
        new_db = FAISS.from_texts(text_chunks, embedding=embeddings)
    else:
        st.error("Nenhum documento disponível para processamento.")
        return

    docs = new_db.similarity_search(user_question)

    chain = get_conversational_chain()

    response = chain(
        {"input_documents": docs, "question": user_question},
        return_only_outputs=True
    )

    print(response)
    st.write("Resposta: ", response["output_text"])


# -------------------------------------------------------------------------------------------------------------------------- Main function
# -------------------------------------------------------------------------------------------------------------------------- Main function
def main():
    # Configuração da página deve ser a primeira coisa a ser feita
    st.set_page_config(page_title="PDF Genie", page_icon=":magic_wand: :page_facing_up:")

    # Agora, o restante do código pode seguir normalmente
    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None

    st.title("PUC MINAS - Tópicos 3")  # Título
    st.header('Engenharia de Computação | 2/2024')
    st.header(':blue[PDF Genie] :magic_wand: :page_facing_up:')
    st.text("Tópicos em Computação III \nProf.: Wladmir Cardoso Brandão\nAluno: Samuel Lobo Chiodi\n")
    st.text("Este é um assistente baseado em LLM capaz de indexar vetores de uma coleção de \ndocumentos PDF que responde perguntas feitas sobre os arquivos lidos")

    user_question = st.text_input("Faça uma pergunta sobre os PDFs enviados:")
    if user_question:
        handle_userinput(user_question)

    # ----------------------------------------------------------------------------------------------------------------------- PDFs processing
    with st.sidebar:
        st.subheader("Importar documentos")
        pdf_docs = st.file_uploader("Envie seus PDFs aqui e clique em 'Processar'", accept_multiple_files=True)
        if st.button("Processar"):
            if pdf_docs:
                # Armazenando os PDFs na sessão
                st.session_state.pdf_docs = pdf_docs
                with st.spinner("Processando..."):
                    try:
                        raw_text = get_pdf_text(pdf_docs)
                        text_chunks = get_text_chunks(raw_text)
                        vectorstore = get_vectorstore(text_chunks)
                        st.session_state.conversation = get_conversational_chain()
                        st.success("Documentos processados com sucesso!")
                    except Exception as e:
                        st.error(f"Erro ao processar PDFs: {e}")
            else:
                st.warning("Por favor, envie documentos PDF antes de processar.")



if __name__ == '__main__':
    main()
