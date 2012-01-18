import json
from zope.component import getUtility
from zope.app.intid.interfaces import IIntIds
from z3c.relationfield import RelationValue

from Products.Five import BrowserView
from siyavula.what import MessageFactory as _


class AddQuestionView(BrowserView):
    """ Add a question to the questions folder and associate it with the
        given context.
    """
    def addQuestion(self):
        request = self.request
        context = self.context

        portal = context.restrictedTraverse('@@plone_portal_state').portal()
        questions = portal._getOb('questions')
        new_id = questions.generateId('question')
        intids = getUtility(IIntIds)
        related_id = intids.getId(self.context)
        question_text = request.get('question')

        questions.invokeFactory('siyavula.what.question',
                                id=new_id,
                                relatedContent=RelationValue(related_id),
                                question=question_text)
        
        question = questions._getOb(new_id)
        return question

    def addQuestionJSON(self):
        question = self.addQuestion() 
        message = "Question %s was added" %question.question
        result = 'success'
        return json.dumps({result: result,
                           message: message})
