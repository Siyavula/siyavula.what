import json
from zExceptions import NotFound
from z3c.relationfield.relation import create_relation

from Products.CMFCore.utils import getToolByName

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
        view = question.restrictedTraverse('@@render-question')
        html = view()
        result = 'success'
        return json.dumps({'result' : result,
                           'message': message,
                           'html'   : html})


class DeleteQuestionView(BrowserView):
    def deleteQuestion(self):
        request = self.request
        context = self.context

        questionid = request.form.get('questionid')
        if questionid is None: return False

        portal = context.restrictedTraverse('@@plone_portal_state').portal()
        questions = portal._getOb('questions')
        questions._delObject(questionid)
        return True

    def deleteQuestionJSON(self):
        result = self.deleteQuestion()
        message = "Question was deleted."
        result = 'success'
        if not result:
            message = "Question was not deleted."
            result = 'failure'
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
    
    def allowQuestions(self):
        """ Check if the content in question (self.context) allows
            questions.
        """
        allow = getattr(self.context, 'allowQuestions', False)
        return allow

    def author(self, question):
        return question.Creator()

    def author_image(self, question):
        username = question.Creator()
        if username is None:
            # return the default user image if no username is given
            return 'defaultUser.gif'
        else:
            pmt = getToolByName(self.context, 'portal_membership')
            return pmt.getPersonalPortrait(username).absolute_url()
        
    def get_author_home_url(self, question):
        username = question.Creator()
        if username is None:
            return None
        else:
            return "%s/author/%s" % (self.context.portal_url(), username)

    def can_delete(self, question):
        pmt = getToolByName(self.context, 'portal_membership')
        return pmt.checkPermission('Delete objects', question) and True or False

    def can_delete_answer(self, answer):
        pmt = getToolByName(self.context, 'portal_membership')
        portal_properties = getToolByName(self.context, 'portal_properties')
        encoding = portal_properties.get('default_charset', 'utf-8')
        member = pmt.getAuthenticatedMember().getId().encode(encoding)
        return answer.Creator() == member and True or False


class DeleteAnswerView(BrowserView):
    def deleteAnswer(self):
        request = self.request
        context = self.context

        questionid = request.form.get('questionid')
        answerid = request.form.get('answerid')
        if questionid is None or answerid is None: return False

        portal = context.restrictedTraverse('@@plone_portal_state').portal()
        questions = portal._getOb('questions')
        question = questions._getOb(questionid)
        question._delObject(answerid)
        return True

    def deleteAnswerJSON(self):
        result = self.deleteAnswer()
        message = "Answer was deleted."
        result = 'success'
        if not result:
            message = "Answer was not deleted."
            result = 'failure'
        return json.dumps({result: result,
                           message: message})


class AnsweredMessageView(BrowserView):
    
    def related_content(self):
        return self.context.relatedContent.to_object
