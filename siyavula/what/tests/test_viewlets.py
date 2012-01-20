import os

from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView as View
from plone.app.testing import login, logout

from base import SiyavulaWhatTestBase

from siyavula.what.browser.questionslistviewlet import QuestionsListViewlet 
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
        request.form['action'] = 'add-question'
        viewlet[0].update()

        self.assertTrue(
            len(self.portal.questions) == 1,
            'Create question failed.'
        )
        
        question = self.portal.questions.objectValues()[0]
        wft = getToolByName(question, 'portal_workflow')
        review_state = wft.getInfoFor(question, 'review_state', 'question_workflow')
        self.assertEqual(
            review_state, 'submitted',
            'The question should be in review state "submitted"'
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
    
    def setUp(self):
        super(TestQuestionsListViewlet, self).setUp()
        acl_users = getToolByName(self.portal, 'acl_users')
        acl_users.userFolderAddUser('user1', 'secret', ['Member'], [])        

    def _get_list_viewlet(self): 
        context = self.portal.questions
        manager_name = 'plone.belowcontent'
        viewlet_name = 'questions-list'
        layer = ISiyavulaWhatLayer
        viewlets = self._find_viewlet(context, manager_name, viewlet_name, layer)
        return viewlets[0]

    def test_viewletexists_in_custom_layer(self):
        viewlet = self._get_list_viewlet()
        self.assertTrue(viewlet, 'Questions-list viewlet not found.')

    def test_viewlet_not_in_default_layer(self):
        context = self.portal.questions
        manager_name = 'plone.belowcontent'
        viewlet_name = 'questions-list'
        viewlet = self._find_viewlet(context, manager_name, viewlet_name)
        self.assertTrue(not viewlet, 'Questions-list viewlet found in wrong layer.')
    
    def test_create_answer_without_text(self):
        question = self._createQuestion()
        viewlet = self._get_list_viewlet()

        request = self.portal.REQUEST
        request.form['siyavula.what.questionslist.form.submitted'] = 'submitted'
        viewlet.update()
        self.assertTrue(
            len(question) == 0,
            'Cannot create answer without text.'
        )

    def test_create_answer_with_text(self):
        question = self._createQuestion()
        viewlet = self._get_list_viewlet()

        request = self.portal.REQUEST
        request.form['siyavula.what.questionslist.form.submitted'] = 'submitted'
        request.form['questionid'] = question.getId()
        request.form['answer'] = 'first answer'
        request.form['action'] = 'add-answer'
        viewlet.update()

        self.assertTrue(
            len(question) == 1,
            'Create answer failed.'
        )

        wft = getToolByName(question, 'portal_workflow')
        review_state = wft.getInfoFor(question, 'review_state', 'question_workflow')
        self.assertEqual(
            review_state, 'answered',
            'The question should be in review state "answered"'
        )

    def test_create_answer_wrong_submit_data(self):
        question = self._createQuestion()
        viewlet = self._get_list_viewlet()

        request = self.portal.REQUEST
        request.form['form.submitted'] = 'submitted'
        request.form['answer'] = 'first answer'
        request.form['questionid'] = question.getId()
        viewlet.update()
        self.assertTrue(
            len(question) == 0,
            'Should not have created an answer.'
        )
    
    def test_questions(self):
        questions = []
        for i in range(0,5):
            questions.append(self._createQuestion())

        viewlet = self._get_list_viewlet()
        viewlet_questions = viewlet.questions()

        self.assertTrue(
            len(viewlet_questions) == 5,
            'List questions viewlet did not find correct questions.'
        )

        for question in questions:
            self.assertTrue(question in viewlet_questions)

    def test_delete_question(self):
        question = self._createQuestion()
        viewlet = self._get_list_viewlet()

        request = self.portal.REQUEST
        request.form['siyavula.what.questionslist.form.submitted'] = 'submitted'
        request.form['questionid'] = question.getId()
        request.form['action'] = 'delete-question'
        viewlet.update()

        self.assertTrue(
            len(self.portal.questions.objectIds()) == 0,
            'Question was not deleted.'
        )

    def test_delete_question_with_wrong_data(self):
        question = self._createQuestion()
        viewlet = self._get_list_viewlet()

        request = self.portal.REQUEST
        request.form['siyavula.what.questionslist.form.submitted'] = 'submitted'
        request.form['questionid'] = question.getId()
        viewlet.update()

        self.assertTrue(
            len(self.portal.questions.objectIds()) > 0,
            'Question should not have been deleted.'
        )

    def test_author(self):
        question = self._createQuestion()
        viewlet = self._get_list_viewlet()
        self.assertEqual(
            viewlet.author(question), question.Creator(),
            'Author incorrect.'
        )

    def test_author_image(self):
        question = self._createQuestion()
        viewlet = self._get_list_viewlet()
        pmt = self.portal.portal_membership
        image = pmt.getPersonalPortrait(question.Creator()).absolute_url()
        self.assertEqual(
            viewlet.author_image(question), image,
            'Image incorrect.'
        )
    
    def test_get_author_home_url(self):
        question = self._createQuestion()
        viewlet = self._get_list_viewlet()
        home_url = "%s/author/%s" % (self.portal.portal_url(), question.Creator())
        self.assertEqual(
            viewlet.get_author_home_url(question), home_url,
            'Home URL incorrect.'
        )
    
    def test_can_delete_question_as_creator(self):
        question = self._createQuestion()
        viewlet = self._get_viewlet()

        can_delete = viewlet.can_delete(question)
        self.assertEqual(
            can_delete, True,
            'Creator cannot delete question.'
        )

    def test_can_delete_question_as_member(self):
        question = self._createQuestion()
        logout()
        login(self.portal, 'user1')
        viewlet = self._get_viewlet()

        can_delete = viewlet.can_delete(question)
        self.assertEqual(
            can_delete, False,
            'Only creator and admin may delete questions.'
        )

    def test_can_delete_answer_as_creator(self):
        question = self._createQuestion()
        answer = self._createAnswer(question)
        viewlet = self._get_viewlet()

        can_delete = viewlet.can_delete_answer(answer)
        self.assertEqual(
            can_delete, True,
            'Creator cannot answer.'
        )

    def test_can_delete_answer_as_member(self):
        question = self._createQuestion()
        answer = self._createAnswer(question)
        logout()
        login(self.portal, 'user1')
        viewlet = self._get_viewlet()

        can_delete = viewlet.can_delete_answer(answer)
        self.assertEqual(
            can_delete, False,
            'Only creator and admin may delete answers.'
        )

    def _get_viewlet(self):
        request = self.portal.REQUEST
        context = self.portal.questions
        view = View(context, request)
        viewlet = QuestionsListViewlet(context, request, view, None) 
        return viewlet
