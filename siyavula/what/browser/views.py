import json
from zope.security import checkPermission
from zExceptions import NotFound
from z3c.relationfield.relation import create_relation

from Products.CMFCore.utils import getToolByName

from Products.Five import BrowserView
from siyavula.what import MessageFactory as _


HOST_NAME_MAP = {'maths'  : 'everythingmaths.co.za',
                 'science': 'everythingscience.co.za',
                }


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
        self.request.response.setHeader('X-Theme-Disabled', 'True')
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
        self.request.response.setHeader('X-Theme-Disabled', 'True')
        result = self.deleteQuestion() and 'success' or 'failure'
        message = "Question was deleted."
        questionid = self.request.get('questionid')
        if not result:
            message = "Question was not deleted."
            result = 'failure'
        return json.dumps({'result': result,
                           'message': message,
                           'questionid': questionid})


class AddAnswerView(BrowserView):
    """ Add an answer for a given the question.
    """
    def can_show(self):
        permission = 'Siyavula What: Add Answer'
        pmt = getToolByName(self.context, 'portal_membership')
        return pmt.checkPermission(permission, self.context) and True or False

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
        self.request.response.setHeader('X-Theme-Disabled', 'True')
        answer = self.addAnswer() 
        message = "Answer %s was added" %answer.text
        result = 'success'
        view = answer.restrictedTraverse('@@render-answer')
        html = view()
        return json.dumps({'result' : result,
                           'message': message,
                           'html'   : html})
    
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
        self.request.response.setHeader('X-Theme-Disabled', 'True')
        result = self.deleteAnswer() and 'success' or 'failure'
        message = "Answer was deleted."
        answerid = self.request.form.get('answerid')
        if not result:
            message = "Answer was not deleted."
            result = 'failure'
        return json.dumps({'result': result,
                           'message': message,
                           'answerid': answerid})


class AnsweredMessageView(BrowserView):
    
    def related_content(self):
        return self.context.relatedContent.to_object

    def get_content_url(self, content):
        """ We try to use the correct domain based on the folder in which
            the content resides.
            We use the navigation root of the content passed in and the 
            constant HOST_NAME_MAP above to build the url.
            If we cannot match any entry in HOST_NAME_MAP we use the 
            HTTP_HOST value of the current request.
        """
        pps = content.restrictedTraverse('@@plone_portal_state')
        default_host = self.request.HTTP_HOST
        navroot = pps.navigation_root()
        host = HOST_NAME_MAP.get(navroot.getId(), default_host)
        path = '/'.join(content.getPhysicalPath()[3:])
        return 'http://%s/%s' %(host, path)
