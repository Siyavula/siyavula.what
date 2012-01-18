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

        # if the form was not posted to this method we return
        if not self.request.form.get('form.submitted'): return

        if self.request.get('method', '').lower() == 'post':
            view = self.context.restrictedTraverse('@@add-answer')
            answer = view()
            self.request.response.redirect(self.context.absolute_url())

    
    def questions(self):
        context = self.context
        uuid = IUUID(context)
        pc = getToolByName(context, 'portal_catalog')
        query = {'portal_type': 'siyavula.what.question',
                 'relatedContentUID': uuid,
                 'sort_on': 'created',
                }
        brains = pc(query)
        return brains and [b.getObject() for b in brains] or []
