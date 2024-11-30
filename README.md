## PDF Genie: Um Assistente de Perguntas e Respostas para PDFs com IA

Este aplicativo Streamlit permite que você converse com seus documentos PDF usando o poder de Grandes Modelos de Linguagem (LLMs) e embeddings de texto. Faça upload de seus PDFs, faça perguntas em linguagem natural e obtenha respostas perspicazes com base no conteúdo de seus documentos.

Acesso o aplicativo via web aqui:
https://my-as05.streamlit.app/

## Recursos

* **Carregamento de PDFs:** Carregue facilmente vários documentos PDF.
* **Perguntas e Respostas Conversacionais:** Participe de uma conversa natural com seus documentos.
* **Embeddings OpenAI:** Utiliza os embeddings de linguagem da OpenAI para uma busca semântica precisa.
* **Armazenamento Vetorial FAISS:** Armazena e recupera informações de seus documentos de forma eficiente.
* **Framework Langchain:** Aproveita o Langchain para aplicativos simplificados com LLM.

## Instalação e Configuração

1. **Clone o Repositório:**
   git clone git@github.com:SamuelVLC/AS05.git
   
   cd your-repository-name

2. **Crie um Ambiente Virtual (Recomendado):**
   ```
   conda --version
   wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
   bash Miniconda3-latest-Linux-x86_64.sh
   source ~/.bashrc
   conda --version
   rm Miniconda3-latest-Linux-x86_64.sh
   ```
   ```
   conda create -p venv python==3.10
   conda activate venv
   ```
3. **Instale as Dependências:**
   ```
   pip install -r requirements.txt
   ```
   Assegure-se de que as versões listadas em requirements.txt estão corretas para evitar possíveis incompatibilidades:
   ```
    streamlit
    google-generativeai
    python-dotenv
    langchain
    PyPDF2
    chromadb
    faiss-cpu
    langchain_google_genai
    langchain==0.2.17
    langchain-core==0.2.43
    langchain-community
   ```
4. **Configure a sua Chave da API da OpenAI:**

   * Crie um arquivo `.streamlit/secrets.toml` no diretório do projeto e adicione sua chave da API da OpenAI:
   ```
     GOOGLE_API_KEY= "sua_chave_api_aqui"
   ```
5. **inicie o Aplicativo:**
   ```
    /home/your_user/AS05/venv/bin/streamlit run app.py
   ```
   O aplicativo será aberto automaticamente no seu navegador localmente

## Como usar

1. **Carregue seus PDFs:** Utilize a barra lateral para fazer upload de um ou mais arquivos PDF.
2. **Clique em "Processar":** O sistema irá processar os arquivos e gerar um índice.
3. **Formule suas Perguntas:** Digite suas perguntas na caixa de texto.
4. **Receba as Respostas:** O assistente fornecerá respostas com base nos PDFs carregados.

## Créditos
Tópicos em Computação III - Text Mining\
Prof.: Dr. Wladmir Cardoso Brandão\
Aluno: Samuel Lobo Chiodi
