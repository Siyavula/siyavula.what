from Products.CMFCore.utils import getToolByName

from z3c.relationfield.relation import create_relation

from zope.interface import alsoProvides 
from zope.component import queryMultiAdapter
from zope.viewlet.interfaces import IViewletManager

from Products.Five.browser import BrowserView as View

from plone.app.testing import PloneSandboxLayer
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting
import unittest2 as unittest
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID

from plone.testing import z2

from siyavula.what.interfaces import ISiyavulaWhatLayer

PROJECTNAME = "siyavula.what"

class TestCase(PloneSandboxLayer):
    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        import siyavula.what
        self.loadZCML(package=siyavula.what)
        z2.installProduct(app, PROJECTNAME)

    def setUpPloneSite(self, portal):
        self.applyProfile(portal, '%s:default' % PROJECTNAME)

    def tearDownZope(self, app):
        z2.uninstallProduct(app, PROJECTNAME)

FIXTURE = TestCase()
INTEGRATION_TESTING = IntegrationTesting(
    bases=(FIXTURE,), name="fixture:Integration")


class SiyavulaWhatTestBase(unittest.TestCase):
    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

    def _createQuestion(self):
        container = self.portal.questions
        new_id = container.generateId('question')
        rel = create_relation(container.getPhysicalPath())

        container.invokeFactory('siyavula.what.question',
                                id=new_id,
                                relatedContent=rel,
                                text='test question 01')
        question = container._getOb(new_id)
        return question

    def _createAnswer(self, question):
        new_id = question.generateId('answer')
        newid = question.invokeFactory(
            'siyavula.what.answer',
            id=new_id,
            text='test answer 01',
        )
        answer = question._getOb(newid)
        return answer
    
    def _find_viewlet(self, manager_name, viewlet_name, layer=None):
        context = self.portal.questions
        request = self.portal.REQUEST
        if layer:
            alsoProvides(request, layer)

        view = View(context, request)
        manager = queryMultiAdapter(
            (context, request, view),
            IViewletManager,
            manager_name,
            default=None
        )
        self.failUnless(manager)

        manager.update()
        viewlets = manager.viewlets
        viewlet = [v for v in viewlets if v.__name__ == viewlet_name]
        return viewlet
