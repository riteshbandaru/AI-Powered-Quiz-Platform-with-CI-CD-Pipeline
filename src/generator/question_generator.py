from langchain.output_parsers import PydanticOutputParser
from src.models.question_struct import MCQ, Blanks, Numerical, TrueFalse
from src.prompts.template import (
    mcq_prompt_template,
    fill_blank_prompt_template,
    numerical_prompt_template,
    true_false_template,
)
from src.llm.groq_client import groq_client
from src.config.settings import Settings as settings
from src.common.logger import get_logger
from src.common.custom_exception import CustomException


class QuestionGenerator:
    def __init__(self):
        self.llm = groq_client()
        self.logger = get_logger(self.__class__.__name__)

    def _retry_and_parse(self, prompt, parser, subject, topic, difficulty, exam_type):
        for attempt in range(settings.MAX_RETRIES):
            try:
                self.logger.info(f"[{attempt+1}/{settings.MAX_RETRIES}] Generating question on '{topic}' ({difficulty}) for {exam_type}")

                response = self.llm.invoke(prompt.format(
                    subject=subject,
                    topic=topic,
                    difficulty=difficulty,
                    exam_type=exam_type
                ))

                parsed = parser.parse(response.content)
                self.logger.info("Successfully parsed the question.")
                return parsed

            except Exception as e:
                self.logger.error(f"❌ Error: {str(e)}")
                if attempt == settings.MAX_RETRIES - 1:
                    raise CustomException(f"Generation failed after {settings.MAX_RETRIES} attempts", e)

    def generate_mcq(self, subject: str, topic: str, difficulty: str = "medium", exam_type: str = "GATE") -> MCQ:
        try:
            parser = PydanticOutputParser(pydantic_object=MCQ)
            question = self._retry_and_parse(mcq_prompt_template, parser, subject, topic, difficulty, exam_type)

            if len(question.options) != 4 or question.correct_answer not in question.options:
                raise ValueError("Invalid MCQ structure")

            return question

        except Exception as e:
            self.logger.error(f"MCQ generation failed: {str(e)}")
            raise CustomException("MCQ generation failed", e)

    def generate_fill_blank(self, subject: str, topic: str, difficulty: str = "medium", exam_type: str = "GATE") -> Blanks:
        try:
            parser = PydanticOutputParser(pydantic_object=Blanks)
            question = self._retry_and_parse(fill_blank_prompt_template, parser, subject, topic, difficulty, exam_type)

            if "___" not in question.question:
                raise ValueError("Fill-in-the-blank question must contain '___'")

            return question

        except Exception as e:
            self.logger.error(f"Fill-in-the-blank generation failed: {str(e)}")
            raise CustomException("Fill-in-the-blank generation failed", e)

    def generate_numerical(self, subject: str, topic: str, difficulty: str = "medium", exam_type: str = "GATE") -> Numerical:
        try:
            parser = PydanticOutputParser(pydantic_object=Numerical)
            question = self._retry_and_parse(numerical_prompt_template, parser, subject, topic, difficulty, exam_type)
            return question

        except Exception as e:
            self.logger.error(f"Numerical question generation failed: {str(e)}")
            raise CustomException("Numerical question generation failed", e)

    def generate_true_false(self, subject: str, topic: str, difficulty: str = "medium", exam_type: str = "GATE") -> TrueFalse:
        try:
            parser = PydanticOutputParser(pydantic_object=TrueFalse)
            question = self._retry_and_parse(true_false_template, parser, subject, topic, difficulty, exam_type)
            return question

        except Exception as e:
            self.logger.error(f"True/False question generation failed: {str(e)}")
            raise CustomException("True/False question generation failed", e)
