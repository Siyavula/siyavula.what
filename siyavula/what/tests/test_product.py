import os

from Products.CMFCore.utils import getToolByName
from plone.browserlayer.utils import registered_layers

from siyavula.what.interfaces import ISiyavulaWhatLayer

from base import SiyavulaWhatTestBase
from base import PROJECTNAME
from base import INTEGRATION_TESTING

dirname = os.path.dirname(__file__)


class TestProductInstallation(SiyavulaWhatTestBase):
    def test_layer(self):
        self.assertTrue(
            ISiyavulaWhatLayer in registered_layers(),
            'Custom layer not available.'
        )

    def test_setuphandlers(self):
        self.assertTrue(
            'questions' in self.portal.objectIds(),
            'Questions folder was not created.'
        )
        questions = self.portal._getOb('questions')
        wft = getToolByName(self.portal, 'portal_workflow')
        self.assertEqual(
            wft.getInfoFor(questions, 'review_state'), 'private')
