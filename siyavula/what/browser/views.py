import json
from zExceptions import NotFound
from z3c.relationfield.relation import create_relation

from Products.Five import BrowserView
from siyavula.what import MessageFactory as _


class AddQuestionView(BrowserView):
    """ Add a question to the questions folder and associate it with the
        given context.
    """
    def addQuestion(self):
        request = self.request
        context = self.context

        question_text = request.get('question', '')
        if not question_text:
            return

        portal = context.restrictedTraverse('@@plone_portal_state').portal()
        questions = portal._getOb('questions')
        new_id = questions.generateId('question')
        relation = create_relation(context.getPhysicalPath())

        questions.invokeFactory('siyavula.what.question',
                                id=new_id,
                                relatedContent=relation,
                                text=question_text)
        
        question = questions._getOb(new_id)
        return question

    def addQuestionJSON(self):
        question = self.addQuestion() 
        message = "Question %s was added" %question.text
        result = 'success'
        return json.dumps({result: result,
                           message: message})


class AddAnswerView(BrowserView):
    """ Add an answer for a given the question.
    """
    def addAnswer(self):
        request = self.request
        context = self.context

        answer_text = request.get('answer', '')
        if not answer_text:
            return

        portal = context.restrictedTraverse('@@plone_portal_state').portal()
        questions = portal._getOb('questions')

        questionid = self.request.get('questionid', None)
        question = questions._getOb(questionid)
        if not question:
            raise NotFound('The question %s could not be found.' %questionid)

        new_id = question.generateId('answer')

        question.invokeFactory('siyavula.what.answer',
                                id=new_id,
                                text=answer_text)
        
        answer = question._getOb(new_id)
        return answer

    def addAnswerJSON(self):
        answer = self.addAnswer() 
        message = "Answer %s was added" %answer.text
        result = 'success'
        return json.dumps({result: result,
                           message: message})
