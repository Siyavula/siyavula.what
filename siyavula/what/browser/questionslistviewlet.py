from plone.app.layout.viewlets.common import ViewletBase
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from emas.theme import MessageFactory as _

class QuestionsListViewlet(ViewletBase):
    """ Display the list of questions for a given context.
    """
    index = ViewPageTemplateFile('questionslistviewlet_templates/questionslist.pt')

    def update(self):
        super(QuestionsListViewlet, self).update()
        # get all questions relating to this context
        context = self.context
    
    def questions(self):
        return []
