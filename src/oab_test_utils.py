import re
import requests
from requests.auth import HTTPBasicAuth
import os
from dotenv import load_dotenv
load_dotenv()
N8N_API_USER = os.getenv("N8N_API_USER")
N8N_API_PASSWORD = os.getenv("N8N_API_PASSWORD")

def get_question_theme_via_n8n(question_text: str) -> str:
    prompt = f'''Você é um assistente jurídico treinado para classificar questões da prova da OAB. Abaixo está o enunciado de uma questão objetiva. Sua tarefa é ler atentamente o conteúdo da questão e classificá-la em um dos **17 temas jurídicos listados abaixo**.

    Retorne **apenas o nome exato do tema** que melhor representa o conteúdo da questão, conforme as descrições. Se não for possível determinar o tema com confiança, responda exatamente com: **"Não foi possível identificar um tema"**.

    ### Temas possíveis:

    1. Direito Constitucional  
    2. Direito Civil  
    3. Direito Penal  
    4. Direito Processual Civil  
    5. Direito Processual Penal  
    6. Direito Administrativo  
    7. Direito Tributário  
    8. Direito do Trabalho  
    9. Direito Previdenciário  
    10. Direito Eleitoral  
    11. Direito Internacional  
    12. Filosofia do Direito  
    13. Direitos Humanos  
    14. Código de Ética e Disciplina da OAB  
    15. Estatuto da Advocacia e da OAB  
    16. Teoria Geral do Processo  
    17. Presupostos Processuais

    ### Enunciado da questão:
    {question_text}

    ### Resposta esperada:
    Apenas o nome do tema mais adequado.'''

    try:
        response = requests.post(
            "https://bloomingtech.app.n8n.cloud/webhook/9c4bc093-e6bc-407f-92da-5b9558552e8c",
            data=prompt.encode('utf-8'),
            headers={"Content-Type": "text/plain"},
            auth=HTTPBasicAuth(N8N_API_USER, N8N_API_PASSWORD),
            timeout=10
        )

        #print(f"[DEBUG] Status Code: {response.status_code}")
        #print(f"[DEBUG] Response Text: {response.text}")

        response.raise_for_status()

        data = response.json()

        return data.get("output", "Não foi possível identificar um tema")

    except Exception as e:
        print(f"[ERRO] Classificação da questão falhou: {e}")
        return "Não foi possível identificar um tema"

# Formata provas provas 39, 40, 42
def OABTestFormatter(raw_test, test_name):
    texto_raw = ' '.join(raw_test).replace('\n', ' ').strip()

    # Encontra o início da parte útil da prova
    match = re.search(r'p[áa]gina\s*3', texto_raw, re.IGNORECASE)
    if not match:
        raise ValueError("Texto não contém algo parecido com 'página 3'")

    texto = texto_raw[match.end():]

    # Expressão regular para capturar as questões
    pattern = re.compile(
        r'(\d{1,2})\s+(.*?)\s+A\)\s+(.*?)\s+B\)\s+(.*?)\s+C\)\s+(.*?)\s+D\)\s+(.*?)(?=\s+\d{1,2}\s+|$)',
        re.DOTALL
    )

    formatted_questions = []

    for idx, match in enumerate(pattern.finditer(texto), start=1):
        raw_question_text = match.group(2).strip()

        # Remove números no início do enunciado, se houver (ex: "7 Bruno..." → "Bruno...")
        clean_question_text = re.sub(r'^\d{1,2}\s+', '', raw_question_text)

        alt_a = match.group(3).strip()
        alt_b = match.group(4).strip()
        alt_c = match.group(5).strip()
        alt_d = match.group(6).strip()

        tema = get_question_theme_via_n8n(clean_question_text)

        dict_question = {
            'numero': idx,
            'pergunta': clean_question_text,
            'a': alt_a,
            'b': alt_b,
            'c': alt_c,
            'd': alt_d,
            'prova': test_name,
            'tema': tema
        }

        formatted_questions.append(dict_question)

    return formatted_questions

# Formata provas 41 e 43
def OABTestFormatter41(raw_test, test_name):
    text = "\n".join(raw_test)
    blocks = re.split(r'\n(?=\d+\n)', text)

    formatted_questions = []

    for idx, block in enumerate(blocks):
        try:
            if not block.strip():
                continue

            question_number_match = re.match(r'(\d+)\n', block)
            question_number = int(question_number_match.group(1)) if question_number_match else idx + 1

            split_parts = re.split(r'\n\(?([A-Da-d])\)?[\s.-]', block)

            if len(split_parts) < 3:
                print(f"[WARNING] Block ignored (no alternatives): Question {question_number}")
                continue

            question_text = split_parts[0].strip().split("\n", 1)[-1].strip()

            raw_alternatives = split_parts[1:]
            alternatives = {
                raw_alternatives[i].lower(): raw_alternatives[i+1].strip().replace('\n', ' ')
                for i in range(0, len(raw_alternatives) - 1, 2)
            }

            tema = get_question_theme_via_n8n(question_text)

            dict_question = {
                'numero': question_number,
                'pergunta': question_text,
                'prova': test_name,
                'tema': tema,
                **alternatives
            }

            formatted_questions.append(dict_question)

        except Exception as e:
            print(f"[ERROR] Failed to process block {idx}: {e}")

    return formatted_questions


def OABAnswersFormatter(texto_bruto, test_name):
    lines = "\n".join(texto_bruto).splitlines()

    capturing = False
    list_answers = []
    question_number = 1

    for line in lines:
        if "TIPO 1" in line:
            capturing = True
            continue
        if capturing:
            if "TIPO 2" in line:
                break
            if line.startswith("##"):
                # Remove "##" e divide a linha por espaço
                answers = line.replace("##", "").strip().split()
                for answer in answers:
                    list_answers.append({
                        "pergunta": question_number,
                        "resposta": answer.lower(),
                        "prova": test_name
                    })
                    question_number += 1

    return list_answers

def OABAnswersFormatter39(texto_bruto, test_name):
    lines = "\n".join(texto_bruto).splitlines()

    capturing = False
    list_answers = []
    question_number = 1

    for line in lines:
        if "prova  1" in line:
            capturing = True
            continue
        if capturing:
            if "prova  2" in line:
                break
            if line.startswith("##"):
                # Remove "##" e divide a linha por espaço
                answers = line.replace("##", "").strip().split()
                for answer in answers:
                    list_answers.append({
                        "pergunta": question_number,
                        "resposta": answer.lower(),
                        "prova": test_name
                    })
                    question_number += 1

    return list_answers

def OABAnswersFormatter43(texto_bruto, test_name):
    lines = "\n".join(texto_bruto).splitlines()

    capturing = False
    list_answers = []
    question_number = 1

    for line in lines:
        if "PROVA TIPO  1" in line:  # Garante que pegue exatamente o TIPO 1
            capturing = True
            continue
        if capturing:
            # Se encontrar outra seção ou um novo tipo, interrompe
            if "PROVA TIPO" in line and "1" not in line:
                break
            if line.startswith("##"):
                # Remove prefixo "##" e limpa espaços extras
                answers = line.replace("##", "").strip().split()

                for answer in answers:
                    clean_answer = answer.strip("*").lower()
                    if clean_answer in {"a", "b", "c", "d"}:
                        list_answers.append({
                            "pergunta": question_number,
                            "resposta": clean_answer,
                            "prova": test_name
                        })
                        question_number += 1
                    else:
                        # Ignora anuladas ou entradas inválidas
                        continue

    return list_answers


def OABQuestionAnswerFormatter(questions, answers):
    question_num = 0
    question_answer = []
    while question_num < 79:
        correct_answer = answers[question_num]['resposta']
        # Remove perguntas mal formatadas ou anuladas
        if correct_answer == '*':
            question_num += 1
            continue
        if len(questions[question_num]) < 5:
            question_num += 1
            continue 
        question = questions[question_num]['pergunta']
        answer_text = questions[question_num][correct_answer]
        question_answer.append({"pergunta" : question, "resposta": answer_text})
        question_num += 1

    return question_answer