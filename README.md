# 📧 Classificador de E-mails com IA (Backend)

Este projeto consiste em uma API desenvolvida em Python (Flask) que recebe arquivos de e-mail (PDF ou Texto), realiza o pré-processamento dos dados utilizando NLTK e utiliza a Inteligência Artificial do Google (Gemini) para categorizar a mensagem e sugerir uma resposta.

## 🛠️ Tecnologias Utilizadas

* **Python 3.x**
* **Flask:** Servidor Web e API.
* **Google GenAI SDK:** Conexão com a IA Gemini.
* **NLTK:** Limpeza e tratamento de texto.
* **pypdf:** Leitura de arquivos PDF.
* **Unidecode:** Tratamento de caracteres.

## 📦 Como Instalar e Rodar

### 1. Pré-requisitos
Certifique-se de ter o Python instalado. Recomenda-se o uso de um ambiente virtual.

### 2. Instalação das Dependências
Execute o comando abaixo no terminal para instalar todas as bibliotecas necessárias:

pip install flask flask-cors pypdf google-genai nltk unidecode python-dotenv

### 3. Configuração da API Key
1.  Crie um arquivo chamado `.env` na raiz do projeto (mesma pasta do `app.py`).
2.  Adicione sua chave do Google AI Studio neste arquivo:

GEMINI_API_KEY=Sua_Chave_Aqui_Sem_Aspas

### 4. Executando o Servidor
Inicie o backend com o comando:

python app.py

O servidor rodará localmente em: `http://127.0.0.1:5000`

> **Nota:** Na primeira execução, o script fará o download automático dos dicionários do NLTK (stopwords, rslp), o que pode levar alguns instantes.
