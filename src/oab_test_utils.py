import re

def OABTestFormatter39(raw_test, test_name):
    texto = ' '.join(raw_test).replace('\n', ' ').strip()

    # Expressão regular para separar questões
    questions_pattern = re.split(r'(?=\b\d{1,2}\b\s+)', texto)

    formatted_questions = []

    for question in questions_pattern:
        if not question.strip():
            continue

        # Separa enunciado das alternativas
        parts = re.split(r'\bA\)\s', question, maxsplit=1)
        if len(parts) < 2:
            continue

        question_text = parts[0].strip()
        brute_options = 'A) ' + parts[1].strip()

        # Captura alternativas A a D (e opcionalmente E se houver)
        options = re.findall(r'([A-D])\)\s(.*?)(?=\s[A-D]\)|$)', brute_options, re.DOTALL)

        dict_questions = {'pergunta': question_text}
        for leter, alt_text in options:
            dict_questions[leter.lower()] = alt_text.strip()

        formatted_questions.append(dict_questions)

    return formatted_questions

def OABTestFormatter40(raw_test, test_name):
    texto = ' '.join(raw_test).replace('\n', ' ').strip()

    # Expressão regular para separar questões
    questions_pattern = re.split(r'(?=\b\d{1,2}\b\s+)', texto)

    formatted_questions = []

    for question in questions_pattern:
        if not question.strip():
            continue

        # Separa enunciado das alternativas
        parts = re.split(r'\bA\)\s', question, maxsplit=1)
        if len(parts) < 2:
            continue

        question_text = parts[0].strip()
        brute_options = 'A) ' + parts[1].strip()

        # Captura alternativas A a D (e opcionalmente E se houver)
        options = re.findall(r'([A-D])\)\s(.*?)(?=\s[A-D]\)|$)', brute_options, re.DOTALL)

        dict_questions = {'pergunta': question_text, 'prova': test_name}
        for leter, alt_text in options:
            dict_questions[leter.lower()] = alt_text.strip()

        formatted_questions.append(dict_questions)

    return formatted_questions

def OABTestFormatter41(raw_test):
    texto = ' '.join(raw_test).replace('\n', ' ').strip()

    # Expressão regular para separar questões
    questions_pattern = re.split(r'(?=\b\d{1,2}\b\s+)', texto)

    formatted_questions = []

    for question in questions_pattern:
        if not question.strip():
            continue

        # Separa enunciado das alternativas
        parts = re.split(r'\bA\)\s', question, maxsplit=1)
        if len(parts) < 2:
            continue

        question_text = parts[0].strip()
        brute_options = 'A) ' + parts[1].strip()

        # Captura alternativas A a D (e opcionalmente E se houver)
        options = re.findall(r'([A-D])\)\s(.*?)(?=\s[A-D]\)|$)', brute_options, re.DOTALL)

        dict_questions = {'pergunta': question_text}
        for leter, alt_text in options:
            dict_questions[leter.lower()] = alt_text.strip()

        formatted_questions.append(dict_questions)

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