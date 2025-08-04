from typing import List, Optional
from pydantic import BaseModel, Field, validator


class MCQ(BaseModel):
    question: str = Field(description="Multiple-choice question text.")
    options: List[str] = Field(description="Exactly four options.")
    correct_answer: str = Field(description="Correct answer from the options.")
    explanation: Optional[str] = Field(default=None, description="Explanation for the correct answer (optional).")

    @validator('question', pre=True)
    def clean_question(cls, v):
        if isinstance(v, dict):
            return v.get('description', str(v))
        return str(v)


class Blanks(BaseModel):
    question: str = Field(description="Fill-in-the-blank question with a '_____' in the sentence.")
    answer: str = Field(description="Correct word or phrase that fills in the blank.")
    explanation: Optional[str] = Field(default=None, description="Explanation for why the answer is correct (optional).")

    @validator('question', pre=True)
    def clean_question(cls, v):
        if isinstance(v, dict):
            return v.get('description', str(v))
        return str(v)


class TrueFalse(BaseModel):
    question: str = Field(description="A statement that is either true or false.")
    answer: bool = Field(description="The truth value of the statement.")
    explanation: Optional[str] = Field(default=None, description="Explanation justifying the answer (optional).")

    @validator('question', pre=True)
    def clean_question(cls, v):
        if isinstance(v, dict):
            return v.get('description', str(v))
        return str(v)


class Numerical(BaseModel):
    question: str = Field(description="Numerical question requiring a numeric answer.")
    answer: float = Field(description="Correct numeric value.")
    explanation: Optional[str] = Field(default=None, description="Explanation showing how the answer was derived (optional).")

    @validator('question', pre=True)
    def clean_question(cls, v):
        if isinstance(v, dict):
            return v.get('description', str(v))
        return str(v)
