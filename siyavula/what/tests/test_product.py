import os

from Products.CMFCore.utils import getToolByName

from base import SiyavulaWhatTestBase
from base import PROJECTNAME
from base import INTEGRATION_TESTING

dirname = os.path.dirname(__file__)


class TestProductInstallation(SiyavulaWhatTestBase):
    def test_layer(self):
        pass        

    def test_setuphandlers(self):
        self.assertTrue(
            'questions' in self.portal.objectIds(),
            'Questions folder was not created.'
        )
        questions = self.portal._getOb('questions')
        wft = getToolByName(self.portal, 'portal_workflow')
        self.assertEqual(
            wft.getInfoFor(questions, 'review_state'), 'private')
