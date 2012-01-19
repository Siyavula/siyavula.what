import os

from zope.interface import alsoProvides 
from zope.component import queryMultiAdapter
from zope.viewlet.interfaces import IViewletManager

from Products.Five.browser import BrowserView as View

from plone.uuid.interfaces import IUUID
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID

from z3c.relationfield.relation import create_relation

from base import SiyavulaWhatTestBase
from base import PROJECTNAME
from base import INTEGRATION_TESTING

from siyavula.what.interfaces import ISiyavulaWhatLayer

dirname = os.path.dirname(__file__)


class TestAllowQuestionsSchemaExtender(SiyavulaWhatTestBase):
    """ Test the schema extender that enables questions on
        archetypes content.
    """
    
    def test_questions_disabled(self):
        self.portal.invokeFactory('Document', id='test_page')
        context = self.portal.test_page
        context.allowQuestions = False

        manager_name = 'plone.belowcontent'
        viewlet_name = 'question-add'
        layer = ISiyavulaWhatLayer
        viewlet = self._find_viewlet(context, manager_name, viewlet_name, layer)
        
        self.assertTrue(
            viewlet[0].render() ==  "",
            'Questions are disable; viewlet should not render.'
        )

    def test_questions_enabled(self):
        self.portal.invokeFactory('Document', id='test_page')
        context = self.portal.test_page
        context.allowQuestions = True

        manager_name = 'plone.belowcontent'
        viewlet_name = 'question-add'
        layer = ISiyavulaWhatLayer
        viewlet = self._find_viewlet(context, manager_name, viewlet_name, layer)
        
        self.assertTrue(
            len(viewlet[0].render()) > 0,
            'Questions are enabled; viewlet should render.'
        )
