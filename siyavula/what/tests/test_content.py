import os

from Products.CMFCore.utils import getToolByName
from zope.component import createObject
from zope.component import queryUtility

from plone.uuid.interfaces import IUUID
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID

from z3c.relationfield.relation import create_relation
from plone.dexterity.interfaces import IDexterityFTI

from base import SiyavulaWhatTestBase
from base import PROJECTNAME
from base import INTEGRATION_TESTING

from siyavula.what.answer import IAnswer
from siyavula.what.question import IQuestion
from siyavula.what.question_container import IQuestioncontainer

dirname = os.path.dirname(__file__)


class TestQuestionContainer(SiyavulaWhatTestBase):
    """ Basic methods to test questions container """
    
    def test_questionscontainer_fti(self):
        fti = queryUtility(
            IDexterityFTI, name='siyavula.what.questioncontainer')
        self.assertNotEquals(fti, None, 'No questionscontainer fti')

    def test_questionscontainer_schema(self):
        fti = queryUtility(
            IDexterityFTI, name='siyavula.what.questioncontainer')
        schema = fti.lookupSchema()
        self.assertEquals(
            IQuestioncontainer, schema, 'Question container schema incorrect.')

    def test_questionscontainer_factory(self):
        fti = queryUtility(
            IDexterityFTI, name='siyavula.what.questioncontainer')
        factory = fti.factory
        new_object = createObject(factory)
        self.failUnless(
            IQuestioncontainer.providedBy(new_object),
            'Question container provides wrong interface.')

    def test_questionscontainer_workflow(self):
        context = self.portal
        newid = context.invokeFactory(
            'siyavula.what.questioncontainer',
            id='testquestioncontainer',
        )
        container = context._getOb(newid)
        wft = getToolByName(self.portal, 'portal_workflow')
        self.assertEqual(
            wft.getChainFor(container),
            ('simple_publication_workflow',),
            'Question container workflow is incorrect'
        )

class TestQuestion(SiyavulaWhatTestBase):
    """ Basic methods to test questions """
    
    def test_question_fti(self):
        fti = queryUtility(IDexterityFTI, name='siyavula.what.question')
        self.assertNotEquals(None, fti)

    def test_question_schema(self):
        fti = queryUtility(IDexterityFTI, name='siyavula.what.question')
        schema = fti.lookupSchema()
        self.assertEquals(IQuestion, schema, 'Question schema incorrect.')

    def test_question_factory(self):
        fti = queryUtility(IDexterityFTI, name='siyavula.what.question')
        factory = fti.factory
        new_object = createObject(factory)
        self.failUnless(IQuestion.providedBy(new_object))

    def test_question_workflow(self):
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
            'Question workflow is incorrect'
        )


class TestAnswer(SiyavulaWhatTestBase):
    """ Basic methods to test answers """

    def test_answer_fti(self):
        fti = queryUtility(IDexterityFTI, name='siyavula.what.answer')
        self.assertNotEquals(None, fti)

    def test_answer_schema(self):
        fti = queryUtility(IDexterityFTI, name='siyavula.what.answer')
        schema = fti.lookupSchema()
        self.assertEquals(IAnswer, schema, 'Answer schema incorrect.')

    def test_answer_factory(self):
        fti = queryUtility(IDexterityFTI, name='siyavula.what.answer')
        factory = fti.factory
        new_object = createObject(factory)
        self.failUnless(IAnswer.providedBy(new_object))

    def test_answer_workflow(self):
        context = self.portal.questions
        newid = context.invokeFactory(
            'siyavula.what.question',
            id='testquestion01',
            text='test question 01',
        )
        question = context._getOb(newid)
        newid = question.invokeFactory(
            'siyavula.what.answer',
            id='testanswer01',
            text='test answer 01',
        )
        answer = question._getOb(newid)
        wft = getToolByName(self.portal, 'portal_workflow')
        self.assertEqual(
            wft.getChainFor(answer),
            (),
            'Answer workflow is incorrect'
        )
