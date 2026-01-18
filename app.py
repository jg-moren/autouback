from flask import Flask, request, jsonify
from pypdf import PdfReader
from flask_cors import CORS
from google.genai import Client
import json
import nltk
from nltk import tokenize
import unidecode
import os
from dotenv import load_dotenv 

load_dotenv()

#nltk.download('all')
nltk.download('stopwords')
nltk.download('rslp')

app = Flask(__name__)
CORS(app)


client = Client(api_key=os.getenv("GEMINI_API_KEY"))
MODEL_ID = "gemini-2.5-flash"


def extrair_texto_pdf(file):

    reader = PdfReader(file)

    texto = ""

    for page in reader.pages:
        linha = page.extract_text()
        texto += linha

    return texto



def processar_com_ia(texto_email):
    prompt = f"""
    Analise o seguinte e-mail e responda estritamente em formato JSON.
    
    Critérios:
    - Categoria 'Produtivo': E-mails que tratam de trabalho, solicitações, dúvidas técnicas ou agendamentos.
    - Categoria 'Improdutivo': Spams, correntes, propagandas ou mensagens sem nexo.

    E-mail: "{texto_email}"

    O JSON deve ter exatamente este formato:
    {{
        "categoria": "Produtivo ou Improdutivo",
        "resposta_sugerida": "Escreva aqui uma resposta profissional em formato de email se for produtivo, ou uma mensagem padrão de arquivamento se for improdutivo."
    }}
    """
    
    try:
        response = client.models.generate_content(
            model=MODEL_ID,
            contents=prompt
        )
        
        texto_limpo = response.text.replace('```json', '').replace('```', '').strip()
        dados = json.loads(texto_limpo)
        
        return dados
    except Exception as e:
        return {
            "categoria": "Erro", 
            "resposta_sugerida": e    
        }


palavras_irrelevantes = nltk.corpus.stopwords.words('portuguese')
token_pontuacao = tokenize.WordPunctTokenizer()
stemmer = nltk.RSLPStemmer()

def processar_texto( texto ):

    tokens = token_pontuacao.tokenize(texto)

    #remover paralvras irrelevantes 
    frase_processada = [palavra.lower() for palavra in tokens if palavra.lower() not in palavras_irrelevantes]
    
    #remove simbolos
    frase_processada = [palavra for palavra in frase_processada if palavra.isalpha()]

    #remove acentos
    frase_processada = [unidecode.unidecode(palavra) for palavra in frase_processada]
    
    #aplica o Stemmer (RSLP)
    #frase_processada = [stemmer.stem(palavra) for palavra in frase_processada]
    
    return ' '.join(frase_processada)
    #return avaliacao

@app.route('/upload', methods=['POST'])
def processar_email():
    conteudo_texto = ""

    if 'file' in request.files:
        arquivo = request.files['file']
        if arquivo.filename.endswith('.pdf'):
            conteudo_texto = extrair_texto_pdf(arquivo)
        else:
            conteudo_texto = arquivo.read().decode('utf-8')
    elif 'text' in request.form:
        conteudo_texto = request.form['text']

    #print(conteudo_texto)

    conteudo_texto = processar_texto(conteudo_texto)

    #print(conteudo_texto)



    result = processar_com_ia(conteudo_texto)
    
    return result

    categoria = "Produtivo" if "urgente" in conteudo_texto.lower() else "Improdutivo"
    resposta = "Olá, recebemos sua mensagem e daremos prioridade." if categoria == "Produtivo" else "Obrigado pelo contato."

    result =  jsonify({
        "categoria": categoria,
        "resposta_sugerida": resposta,
        "texto_extraido": conteudo_texto[:100] # Retorna os primeiros 100 caracteres para conferência
    })

    return result

if __name__ == '__main__':
    app.run(port=5000, debug=True)
