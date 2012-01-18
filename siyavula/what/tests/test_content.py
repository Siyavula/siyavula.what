import os

from Products.CMFCore.utils import getToolByName

from zope.component import getUtility
from zope.app.intid.interfaces import IIntIds
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

    def test_allowed_types(self):
        container = self.portal.questions
        new_id = container.generateId('question')
        container.invokeFactory('siyavula.what.question',
                                id=new_id,
                                text='test question 01')
        self.assertTrue(new_id in container, 'Question create failed')


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

    def test_attributes(self):
        container = self.portal.questions
        question = self._createQuestion()
        self.assertEqual(
            question.text,
            'test question 01',
            'Text set incorrectly.'
        )
        self.assertEqual(
            container,
            question.relatedContent.to_object,
            'Related content set incorrectly.'
        )

    def test_add_answer(self):
        question = self._createQuestion()
        new_id = question.generateId('answer')

        question.invokeFactory('siyavula.what.answer',
                                id=new_id,
                                text='answer_text')
        self.assertTrue(new_id in question, 'Answer was not created')

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
        question = self._createQuestion()
        answer = self._createAnswer(question)
        wft = getToolByName(self.portal, 'portal_workflow')
        self.assertEqual(
            wft.getChainFor(answer),
            (),
            'Answer workflow is incorrect'
        )
           
    def test_attributes(self):
        question = self._createQuestion()
        answer = self._createAnswer(question)
        self.assertEqual(
            answer.text, 'test answer 01', 'Answer text incorrect')
    
    def _createQuestion(self):
        context = self.portal.questions
        newid = context.invokeFactory(
            'siyavula.what.question',
            id='testquestion01',
            text='test question 01',
        )
        question = context._getOb(newid)
        return question

    def _createAnswer(self, question):
        newid = question.invokeFactory(
            'siyavula.what.answer',
            id='testanswer01',
            text='test answer 01',
        )
        answer = question._getOb(newid)
        return answer
