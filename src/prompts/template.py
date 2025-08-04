from langchain.prompts import PromptTemplate

mcq_prompt_template = PromptTemplate(
    template=(
        "Generate a {difficulty} level multiple-choice question from the topic '{topic}' under the subject '{subject}' "
        "that aligns with competitive exams like {exam_type}.\n\n"
        "Return ONLY a JSON object with these fields:\n"
        "- 'question': A conceptual or calculative question\n"
        "- 'options': An array of 4 unique options\n"
        "- 'correct_answer': The correct one from the options\n"
        "- 'explanation' (optional but preferred): Why the answer is correct\n\n"
        "Example format:\n"
        '{{\n'
        '  "question": "Which law explains the conservation of momentum?",\n'
        '  "options": ["Newton’s First Law", "Newton’s Second Law", "Newton’s Third Law", "Law of Gravitation"],\n'
        '  "correct_answer": "Newton’s Third Law",\n'
        '  "explanation": "Newton’s Third Law states that every action has an equal and opposite reaction, which explains momentum conservation."\n'
        '}}\n\n'
        "Your response:"
    ),
    input_variables=["subject", "topic", "difficulty", "exam_type"]
)

fill_blank_prompt_template = PromptTemplate(
    template=(
        "Generate a {difficulty} level fill-in-the-blank question from the topic '{topic}' under the subject '{subject}' "
        "suitable for competitive exams like {exam_type}.\n\n"
        "Return ONLY a JSON object with these fields:\n"
        "- 'question': A sentence with '_____' indicating the blank\n"
        "- 'answer': The correct word or phrase\n"
        "- 'explanation' (optional but preferred): Justify why that answer fits\n\n"
        "Example format:\n"
        '{{\n'
        '  "question": "Ohm’s law states that V = _____ * I.",\n'
        '  "answer": "R",\n'
        '  "explanation": "Ohm’s Law relates voltage (V), current (I), and resistance (R) with V = IR."\n'
        '}}\n\n'
        "Your response:"
    ),
    input_variables=["subject", "topic", "difficulty", "exam_type"]
)

numerical_prompt_template = PromptTemplate(
    template=(
        "Generate a {difficulty} level numerical question from the topic '{topic}' under the subject '{subject}' "
        "for exams like {exam_type}.\n\n"
        "Return ONLY a JSON object with:\n"
        "- 'question': A clear numerical problem\n"
        "- 'answer': A number (float or int)\n"
        "- 'explanation' (optional but preferred): Briefly show the calculation or logic used\n\n"
        "Example:\n"
        '{{\n'
        '  "question": "Calculate the resistance if V=10V and I=2A.",\n'
        '  "answer": 5,\n'
        '  "explanation": "Using Ohm’s Law, R = V/I = 10/2 = 5 Ohms."\n'
        '}}\n\n'
        "Your response:"
    ),
    input_variables=["subject", "topic", "difficulty", "exam_type"]
)

true_false_template = PromptTemplate(
    template=(
        "Generate a {difficulty} level true/false question from the topic '{topic}' in the subject '{subject}' "
        "relevant for {exam_type}.\n\n"
        "Return ONLY a JSON object with:\n"
        "- 'statement': A conceptual or factual statement\n"
        "- 'answer': 'True' or 'False'\n"
        "- 'explanation' (optional but preferred): Clarify why the answer is true or false\n\n"
        "Example:\n"
        '{{\n'
        '  "statement": "In a vacuum, all objects fall at the same rate.",\n'
        '  "answer": "True",\n'
        '  "explanation": "Air resistance is absent in vacuum, so only gravity acts equally on all objects."\n'
        '}}\n\n'
        "Your response:"
    ),
    input_variables=["subject", "topic", "difficulty", "exam_type"]
)
