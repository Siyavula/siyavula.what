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


class TestQuestionAddViewlet(SiyavulaWhatTestBase):
    """ Test question adding viewlet """
    
    def test_viewletexists_in_custom_layer(self):
        context = self.portal.questions
        manager_name = 'plone.belowcontent'
        viewlet_name = 'question-add'
        layer = ISiyavulaWhatLayer
        viewlet = self._find_viewlet(context, manager_name, viewlet_name, layer)
        self.assertTrue(viewlet, 'Question-add viewlet not found.')

    def test_viewlet_not_in_default_layer(self):
        context = self.portal.questions
        manager_name = 'plone.belowcontent'
        viewlet_name = 'question-add'
        viewlet = self._find_viewlet(context, manager_name, viewlet_name)
        self.assertTrue(not viewlet, 'Question-add viewlet found in wrong layer.')
    
    def test_create_question_without_text(self):
        context = self.portal.questions
        manager_name = 'plone.belowcontent'
        viewlet_name = 'question-add'
        layer = ISiyavulaWhatLayer
        viewlet = self._find_viewlet(context, manager_name, viewlet_name, layer)

        request = self.portal.REQUEST
        request.form['siyavula.what.questionadd.form.submitted'] = 'submitted'
        viewlet[0].update()
        self.assertTrue(
            len(self.portal.questions) == 0,
            'Cannot create question without text.'
        )

    def test_create_question_with_text(self):
        context = self.portal.questions
        manager_name = 'plone.belowcontent'
        viewlet_name = 'question-add'
        layer = ISiyavulaWhatLayer
        viewlet = self._find_viewlet(context, manager_name, viewlet_name, layer)

        request = self.portal.REQUEST
        request.form['siyavula.what.questionadd.form.submitted'] = 'submitted'
        request.form['question'] = 'first question'
        viewlet[0].update()
        self.assertTrue(
            len(self.portal.questions) == 1,
            'Create question failed.'
        )

    def test_create_question_wrong_submit_data(self):
        context = self.portal.questions
        manager_name = 'plone.belowcontent'
        viewlet_name = 'question-add'
        layer = ISiyavulaWhatLayer
        viewlet = self._find_viewlet(context, manager_name, viewlet_name, layer)

        request = self.portal.REQUEST
        request.form['form.submitted'] = 'submitted'
        request.form['question'] = 'first question'
        viewlet[0].update()
        self.assertTrue(
            len(self.portal.questions) == 0,
            'Should not have created a question.'
        )

class TestQuestionsListViewlet(SiyavulaWhatTestBase):
    """ Test questions list viewlet """

    def test_viewletexists_in_custom_layer(self):
        context = self.portal.questions
        manager_name = 'plone.belowcontent'
        viewlet_name = 'questions-list'
        layer = ISiyavulaWhatLayer
        viewlet = self._find_viewlet(context, manager_name, viewlet_name, layer)
        self.assertTrue(viewlet, 'Questions-list viewlet not found.')

    def test_viewlet_not_in_default_layer(self):
        context = self.portal.questions
        manager_name = 'plone.belowcontent'
        viewlet_name = 'questions-list'
        viewlet = self._find_viewlet(context, manager_name, viewlet_name)
        self.assertTrue(not viewlet, 'Questions-list viewlet found in wrong layer.')
    
    def test_create_answer_without_text(self):
        question = self._createQuestion()
        context = self.portal.questions
        manager_name = 'plone.belowcontent'
        viewlet_name = 'questions-list'
        layer = ISiyavulaWhatLayer
        viewlet = self._find_viewlet(context, manager_name, viewlet_name, layer)

        request = self.portal.REQUEST
        request.form['siyavula.what.questionslist.form.submitted'] = 'submitted'
        viewlet[0].update()
        self.assertTrue(
            len(question) == 0,
            'Cannot create answer without text.'
        )

    def test_create_answer_with_text(self):
        question = self._createQuestion()
        context = self.portal.questions
        manager_name = 'plone.belowcontent'
        viewlet_name = 'questions-list'
        layer = ISiyavulaWhatLayer
        viewlet = self._find_viewlet(context, manager_name, viewlet_name, layer)

        request = self.portal.REQUEST
        request.form['siyavula.what.questionslist.form.submitted'] = 'submitted'
        request.form['questionid'] = question.getId()
        request.form['answer'] = 'first answer'
        viewlet[0].update()
        self.assertTrue(
            len(question) == 1,
            'Create answer failed.'
        )

    def test_create_answer_wrong_submit_data(self):
        question = self._createQuestion()
        context = self.portal.questions
        manager_name = 'plone.belowcontent'
        viewlet_name = 'questions-list'
        layer = ISiyavulaWhatLayer
        viewlet = self._find_viewlet(context, manager_name, viewlet_name, layer)

        request = self.portal.REQUEST
        request.form['form.submitted'] = 'submitted'
        request.form['answer'] = 'first answer'
        request.form['questionid'] = question.getId()
        viewlet[0].update()
        self.assertTrue(
            len(question) == 0,
            'Should not have created an answer.'
        )
