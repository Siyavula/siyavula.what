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
            view = self.context.restrictedTraverse('@@add-answer')
            answer = view()
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
