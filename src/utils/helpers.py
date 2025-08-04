import os
import streamlit as st
import pandas as pd
from datetime import datetime
from src.generator.question_generator import QuestionGenerator

def rerun():
    st.session_state['rerun_trigger'] = not st.session_state.get('rerun_trigger', False)

class QuizManager:
    def __init__(self):
        self.questions = []
        self.user_answers = []
        self.results = []

    def generate_questions(self, generator: QuestionGenerator, subject: str, topic: str, difficulty: str, question_type: str, num_questions: int, exam_type: str = "GATE"):
        self.questions = []
        self.user_answers = []
        self.results = []

        try:
            for _ in range(num_questions):
                if question_type == "Multiple Choice":
                    question = generator.generate_mcq(subject, topic, difficulty.lower(), exam_type)
                    self.questions.append({
                        'type': 'MCQ',
                        'question': question.question,
                        'options': question.options,
                        'correct_answer': question.correct_answer,
                        'explanation': question.explanation or "No explanation provided."
                    })

                elif question_type == "Fill in the blank":
                    question = generator.generate_fill_blank(subject, topic, difficulty.lower(), exam_type)
                    self.questions.append({
                        'type': 'Fill in the blank',
                        'question': question.question,
                        'correct_answer': question.answer,
                        'explanation': question.explanation or "No explanation provided."
                    })

                elif question_type == "Numeric":
                    question = generator.generate_numerical(subject, topic, difficulty.lower(), exam_type)
                    self.questions.append({
                        'type': 'Numeric',
                        'question': question.question,
                        'correct_answer': str(question.answer),
                        'explanation': question.explanation or "No explanation provided."
                    })

                elif question_type == "True or False":
                    question = generator.generate_true_false(subject, topic, difficulty.lower(), exam_type)
                    self.questions.append({
                        'type': 'True or False',
                        'question': question.question,
                        'correct_answer': question.correct_answer,
                        'explanation': question.explanation or "No explanation provided."
                    })

        except Exception as e:
            st.error(f"Error generating question: {e}")
            return False

        return True

    def attempt_quiz(self):
        self.user_answers = []

        for i, q in enumerate(self.questions):
            st.markdown(f"**Question {i + 1}: {q['question']}**")

            if q['type'] == 'MCQ':
                user_answer = st.radio(
                    f"Select your answer for Question {i + 1}",
                    q['options'],
                    key=f"mcq_{i}"
                )
            elif q['type'] == 'True or False':
                user_answer = st.radio(
                    f"Select True or False for Question {i + 1}",
                    ["True", "False"],
                    key=f"tf_{i}"
                )
            else:
                user_answer = st.text_input(
                    f"Your answer for Question {i + 1}",
                    key=f"text_{i}"
                )

            self.user_answers.append(user_answer)

    def evaluate_quiz(self):
        self.results = []

        for i, (q, user_ans) in enumerate(zip(self.questions, self.user_answers)):
            correct_ans = q['correct_answer']

            if q['type'] in ['MCQ', 'True or False']:
                is_correct = user_ans == correct_ans
            else:
                is_correct = user_ans.strip().lower() == correct_ans.strip().lower()

            self.results.append({
                'question_number': i + 1,
                'question': q['question'],
                'type': q['type'],
                'options': q.get('options', []),
                'user_answer': user_ans,
                'correct_answer': correct_ans,
                'is_correct': is_correct,
                'explanation': q.get('explanation', "No explanation provided.")
            })

    def generate_result_dataframe(self):
        if not self.results:
            return pd.DataFrame()
        return pd.DataFrame(self.results)

    def save_to_csv(self, filename_prefix="quiz_results"):
        if not self.results:
            st.warning("No results to save!")
            return None

        df = self.generate_result_dataframe()

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{filename_prefix}_{timestamp}.csv"
        os.makedirs("results", exist_ok=True)
        full_path = os.path.join("results", filename)

        try:
            df.to_csv(full_path, index=False)
            st.success("Results saved successfully.")
            return full_path
        except Exception as e:
            st.error(f"Failed to save results: {e}")
            return None
