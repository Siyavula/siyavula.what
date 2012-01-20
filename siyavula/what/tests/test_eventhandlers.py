import os

from zope.component import getSiteManager
from zope.component import eventtesting
from zope.lifecycleevent import IObjectModifiedEvent
from zope.lifecycleevent import ObjectModifiedEvent

from Products.CMFPlone.tests.utils import MockMailHost
from Products.MailHost.interfaces import IMailHost

from base import SiyavulaWhatTestBase

from siyavula.what.interfaces import ISiyavulaWhatLayer
from siyavula.what.question import IQuestion
from siyavula.what.eventhandlers import questionAnswered

dirname = os.path.dirname(__file__)


class TestEventHandlers(SiyavulaWhatTestBase):
    """ Test the event handlers.
    """
    def setUp(self):
        super(TestEventHandlers, self).setUp()
        eventtesting.setUp()

    def _test_question_answered(self):
        context = self.portal.questions
        manager_name = 'plone.belowcontent'
        viewlet_name = 'question-add'
        layer = ISiyavulaWhatLayer
        viewlet = self._find_viewlet(context, manager_name, viewlet_name, layer)

        question = self._createQuestion()
        eventtesting.clearEvents()
        request = self.portal.REQUEST
        request.form['siyavula.what.questionslist.form.submitted'] = 'submitted'
        request.form['questionid'] = question.getId()
        request.form['answer'] = 'first answer'
        request.form['action'] = 'add-answer'
        viewlet[0].update()

        events = eventtesting.getEvents(
            IObjectModifiedEvent,
            filter=lambda obj: IQuestion.providedBy(obj)
        )
        self.assertTrue(len(events) > 0, 'Missing event.')

    def test_questionAnswered_incorrect_data(self):
        question = self._createQuestion()

        event = ObjectModifiedEvent(question)
        reported_errors = questionAnswered(question, event)

        self.assertTrue(len(reported_errors) > 0, 'No errors were reported.')
        expected_errors = \
            ['The owner () has no email address!', 'Add a portal email address.']
        for error in expected_errors:
            self.assertTrue(
                error in reported_errors,
                'The error %s was not reported.' %error
        )
    
    def test_questionAnswered(self):
        self.portal._original_MailHost = self.portal.MailHost
        self.portal.MailHost = mailhost = MockMailHost('MailHost')
        sm = getSiteManager(context=self.portal)
        sm.unregisterUtility(provided=IMailHost)
        sm.registerUtility(mailhost, provided=IMailHost)

        question = self._createQuestion()
        pmt = self.portal.portal_membership
        pmt.getMemberById('test_user_1_').setMemberProperties(
            {'email': 'tester@example.com'})
        self.portal.email_from_address = 'admin@example.com'

        event = ObjectModifiedEvent(question)
        errors = questionAnswered(question, event)

        self.assertTrue(errors is None, 'Errors were reported.')
        self.assertTrue(mailhost.messages, 'No message in mailhost.')

    def beforeTearDown(self):
        self.portal.MailHost = self.portal._original_MailHost
        sm = getSiteManager(context=self.portal)
        sm.unregisterUtility(provided=IMailHost)
        sm.registerUtility(aq_base(self.portal._original_MailHost), provided=IMailHost)

