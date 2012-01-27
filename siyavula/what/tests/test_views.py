import os
import unittest2 as unittest
from plone.app.testing import login, logout
from Products.CMFCore.utils import getToolByName

from siyavula.what.tests.base import SiyavulaWhatTestBase

dirname = os.path.dirname(__file__)


class TestAddAnswerView(SiyavulaWhatTestBase):
    """ Test AddAnswerView """

    def setUp(self):
        super(TestAddAnswerView, self).setUp()
        acl_users = getToolByName(self.portal, 'acl_users')
        acl_users.userFolderAddUser('user1', 'secret', ['Member'], [])        

    
    def test_author(self):
        question = self._createQuestion()
        answer = self._createAnswer(question)
        view = answer.restrictedTraverse('@@render-answer')
        self.assertEqual(
            view.author(question), question.Creator(),
            'Author incorrect.'
        )

    def test_author_image(self):
        question = self._createQuestion()
        answer = self._createAnswer(question)
        view = answer.restrictedTraverse('@@render-answer')
        pmt = self.portal.portal_membership
        image = pmt.getPersonalPortrait(question.Creator()).absolute_url()
        self.assertEqual(
            view.author_image(question), image,
            'Image incorrect.'
        )
    
    def test_get_author_home_url(self):
        question = self._createQuestion()
        answer = self._createAnswer(question)
        view = answer.restrictedTraverse('@@render-answer')
        home_url = "%s/author/%s" % (self.portal.portal_url(), question.Creator())
        self.assertEqual(
            view.get_author_home_url(question), home_url,
            'Home URL incorrect.'
        )

    def test_can_delete_answer_as_creator(self):
        question = self._createQuestion()
        answer = self._createAnswer(question)
        view = answer.restrictedTraverse('@@render-answer')

        can_delete = view.can_delete_answer(answer)
        self.assertEqual(
            can_delete, True,
            'Creator cannot answer.'
        )

    def test_can_delete_answer_as_member(self):
        question = self._createQuestion()
        answer = self._createAnswer(question)
        logout()
        login(self.portal, 'user1')
        view = answer.restrictedTraverse('@@render-answer')

        can_delete = view.can_delete_answer(answer)
        self.assertEqual(
            can_delete, False,
            'Only creator and admin may delete answers.'
        )

    def test_can_delete_question_as_creator(self):
        question = self._createQuestion()
        answer = self._createAnswer(question)
        view = answer.restrictedTraverse('@@render-answer')

        can_delete = view.can_delete(question)
        self.assertEqual(
            can_delete, True,
            'Creator cannot delete question.'
        )

    def test_can_delete_question_as_member(self):
        question = self._createQuestion()
        answer = self._createAnswer(question)
        logout()
        login(self.portal, 'user1')
        view = answer.restrictedTraverse('@@render-answer')

        can_delete = view.can_delete(question)
        self.assertEqual(
            can_delete, False,
            'Only creator and admin may delete questions.'
        )

