from objects.question import Question
from objects.answer import Answer

class MockDatabase():
    def __init__(self):
        self.questions = []
        self.answers = []

    def get_question(self):
        return self.questions[-1]
    
    def get_related_answers(self, question:Question):
        related_answers = []
        for answer in self.answers:
            answer:Answer
            if question.uuid == answer.question_uuid:
                related_answers.append(answer)
        return related_answers

    def add_question(self, question:Question):
        self.questions.append(question)

    def add_aswer(self, answer:Answer):
        self.answers.append(answer)

    def _inject_mock_data(self):
        question1 = Question("Is this a question?")
        question2 = Question("Is this also a question?")
        self.questions.append(question1)
        self.questions.append(question2)

        self.answers.append(
            Answer(question_uuid=question1.uuid,
                   user_uuid=None,
                   answer_score=1,
                   relevance_score=1,
                   discussion="Answer to question 1.")
        )
        self.answers.append(
            Answer(question_uuid=question1.uuid,
                   user_uuid=None,
                   answer_score=1,
                   relevance_score=0,
                   discussion="Something unrelated to question 1.")
        )
        self.answers.append(
            Answer(question_uuid=question2.uuid,
                   user_uuid=None,
                   answer_score=-1,
                   relevance_score=1,
                   discussion="Related but no agreement to question 2.")
        )
