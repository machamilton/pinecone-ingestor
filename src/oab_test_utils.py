import re

#formata provas 39,40,42
def OABTestFormatter(raw_test, test_name):
    # Junta todas as linhas em uma string única, removendo quebras de linha
    texto_raw = ' '.join(raw_test).replace('\n', ' ').strip()

    # Tenta encontrar a posição da expressão 'página 3', com ou sem acento, ignorando maiúsculas/minúsculas
    match = re.search(r'p[áa]gina\s*3', texto_raw, re.IGNORECASE)
    if not match:
        raise ValueError("Texto não contém algo parecido com 'página 3'")

    # Corta o texto a partir do final da correspondência com 'página 3'
    texto = texto_raw[match.end():]

    # Regex para extrair número da questão, enunciado e alternativas A-D
    pattern = re.compile(
        r'(\d{1,2})\s+(.*?)\s+A\)\s+(.*?)\s+B\)\s+(.*?)\s+C\)\s+(.*?)\s+D\)\s+(.*?)(?=\s+\d{1,2}\s+|$)',
        re.DOTALL
    )

    formatted_questions = []

    for match in pattern.finditer(texto):
        question_number = match.group(1)
        question_text = match.group(2).strip()
        alt_a = match.group(3).strip()
        alt_b = match.group(4).strip()
        alt_c = match.group(5).strip()
        alt_d = match.group(6).strip()

        dict_question = {
            'pergunta': question_text,
            'a': alt_a,
            'b': alt_b,
            'c': alt_c,
            'd': alt_d,
            'prova': test_name
        }

        formatted_questions.append(dict_question)

    return formatted_questions


#formata provas 41 e 43
def OABTestFormatter41(raw_test, test_name):
    text = "\n".join(raw_test)
    blocks = re.split(r'\n(?=\d+\n)', text)

    formatted_questions = []

    for idx, block in enumerate(blocks):
        try:
            if not block.strip():
                continue

            question_number_match = re.match(r'(\d+)\n', block)
            question_number = int(question_number_match.group(1)) if question_number_match else None

            # Split using the start of alternatives like: "\nA)", "\n(B)", "\na "
            split_parts = re.split(r'\n\(?([A-Da-d])\)?[\s.-]', block)

            if len(split_parts) < 3:
                print(f"[WARNING] Block ignored (no alternatives): Question {question_number or idx}")
                continue

            # The first element is the question statement
            question_text = split_parts[0].strip().split("\n", 1)[-1].strip()

            # Remaining parts are: [letter1, text1, letter2, text2, ...]
            raw_alternatives = split_parts[1:]

            alternatives = {
                raw_alternatives[i].lower(): raw_alternatives[i+1].strip().replace('\n', ' ')
                for i in range(0, len(raw_alternatives) - 1, 2)
            }

            if len(alternatives) < 4:
                print(f"[WARNING] Incomplete alternatives in question {question_number or idx}")

            formatted_questions.append({
                'pergunta': question_text,
                'prova': test_name,
                **alternatives
            })

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