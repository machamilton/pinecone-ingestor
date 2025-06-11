import re

def OABTestFormatter(raw_test):
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