from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from plone.uuid.interfaces import IUUID
from plone.app.layout.viewlets.common import ViewletBase

from siyavula.what import MessageFactory as _

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
            portal_props = getToolByName(self.context, 'portal_properties')
            site_props = portal_props.get('site_properties')
            encoding = site_props.getProperty('default_charset', 'urt-8')
            viewname = ('@@%s' %action).encode(encoding)
            view = self.context.restrictedTraverse(viewname)
            view()
            url = self.context.absolute_url()
            relatedContent = self.context.relatedContent.to_object
            if relatedContent:
                url = relatedContent.absolute_url()
            self.request.response.redirect(url)
            return

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

