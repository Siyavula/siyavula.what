import os

from Products.CMFCore.utils import getToolByName

from plone.uuid.interfaces import IUUID
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID

from z3c.relationfield.relation import create_relation

from base import SiyavulaWhatTestBase
from base import PROJECTNAME
from base import INTEGRATION_TESTING

dirname = os.path.dirname(__file__)


class TestQuestion(SiyavulaWhatTestBase):
    """ Basic methods to test questions """
    
    def test_workflow(self):
        import pdb;pdb.set_trace()
        context = self.portal.questions
        newid = context.invokeFactory(
            'siyavula.what.question',
            id='testquestion01',
            text='test question 01',
        )
        question = context._getOb(newid)
        wft = getToolByName(self.portal, 'portal_workflow')
        self.assertEqual(
            wft.getChainFor(question),
            ('question_workflow',),
            'Question workflow is incorrect,'
        )


    def test_question_fti(self):
        pass

class TestAnswer(SiyavulaWhatTestBase):
    """ Basic methods to test answers """

    def test_answer_fti(self):
        pass
