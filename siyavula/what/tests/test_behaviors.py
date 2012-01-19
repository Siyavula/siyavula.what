import os

from zope.interface import alsoProvides 
from zope.component import queryMultiAdapter
from zope.viewlet.interfaces import IViewletManager

from Products.Five.browser import BrowserView as View
from Products.CMFCore.utils import getToolByName

from plone.uuid.interfaces import IUUID
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID

from z3c.relationfield.relation import create_relation

from base import SiyavulaWhatTestBase
from base import PROJECTNAME
from base import INTEGRATION_TESTING

from siyavula.what.interfaces import ISiyavulaWhatLayer
from siyavula.what.behaviors.allowquestionsbehavior import IAllowQuestionsBehavior

dirname = os.path.dirname(__file__)


class TestAllowQuestionsBehavior(SiyavulaWhatTestBase):
    """ Test the behavior that enables questions on dexterity content.
    """
    
    def test_questions_disabled(self):
        types = getToolByName(self.portal, 'portal_types')
        fti = types.getTypeInfo('siyavula.what.question')
        fti.behaviors = \
            ('siyavula.what.behaviors.allowquestionsbehavior.IAllowQuestionsBehavior',)
        
        context = self._createQuestion()
        manager_name = 'plone.belowcontent'
        viewlet_name = 'question-add'
        layer = ISiyavulaWhatLayer
        viewlet = self._find_viewlet(context, manager_name, viewlet_name, layer)
        
        self.assertTrue(
            viewlet[0].render() ==  "",
            'Questions are disable; viewlet should not render.'
        )

    def test_questions_enabled(self):
        types = getToolByName(self.portal, 'portal_types')
        fti = types.getTypeInfo('siyavula.what.question')
        fti.behaviors = \
            ('siyavula.what.behaviors.allowquestionsbehavior.IAllowQuestionsBehavior',)
        
        context = self._createQuestion()
        context.allowQuestions = True
        manager_name = 'plone.belowcontent'
        viewlet_name = 'question-add'
        layer = ISiyavulaWhatLayer
        viewlet = self._find_viewlet(context, manager_name, viewlet_name, layer)
        
        self.assertTrue(
            len(viewlet[0].render()) > 0,
            'Questions are enabled; viewlet should render.'
        )
