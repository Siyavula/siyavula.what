from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from plone.uuid.interfaces import IUUID
from plone.app.layout.viewlets.common import ViewletBase

from emas.theme import MessageFactory as _

class QuestionsListViewlet(ViewletBase):
    """ Display the list of questions for a given context.
    """
    index = ViewPageTemplateFile('questionslistviewlet_templates/questionslist.pt')

    def update(self):
        super(QuestionsListViewlet, self).update()

        # if the form was not posted to this method we do nothing
        if self.request.form.get('siyavula.what.questionslist.form.submitted'):
            action = self.request.form.get('action', '').lower()
            if not action: return
           
            # action can be 'add-answer' or 'delete-answer'
            viewname = '@@%s' %action
            view = self.context.restrictedTraverse(viewname)
            view()
            self.request.response.redirect(self.context.absolute_url())

    def render(self):
        """ We render an empty string when a specific piece of content
            does not allow questions.
        """
        if self.allowQuestions():
            return super(QuestionsListViewlet, self).render()
        else:
            return ""
    
    def allowQuestions(self):
        """ Check if the content in question (self.context) allows
            questions.
        """
        allow = getattr(self.context, 'allowQuestions', False)
        return allow
    
    def questions(self):
        """ Return all questions that have the current context set
            as 'relatedContent'.
        """
        context = self.context
        uuid = IUUID(context)
        pc = getToolByName(context, 'portal_catalog')
        query = {'portal_type': 'siyavula.what.question',
                 'relatedContentUID': uuid,
                 'sort_on': 'created',
                }
        brains = pc(query)
        return brains and [b.getObject() for b in brains] or []

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
