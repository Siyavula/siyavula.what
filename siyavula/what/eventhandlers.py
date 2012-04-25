import logging

from Products.CMFCore.utils import getToolByName

from siyavula.what import MessageFactory as _
from siyavula.what.utils import get_basic_mailsettings

LOGGER = logging.getLogger('siyavula.what: eventhandlers')


def questionAnswered(question, event):
    """ Send mail when a question is answered.
    """
    wft = getToolByName(question, 'portal_workflow')
    review_state = wft.getInfoFor(
        question, 'review_state', 'question_workflow')
    if review_state in ['submitted', ]:
        wft.doActionFor(question, 'answer')

    # get the basic mail settings and details
    errors, mail_host, mail_from, mail_to = get_basic_mailsettings(question)
    if errors:
        for error in errors:
            LOGGER.warn(error)
        return errors

    # Compose email
    subject = _(u"Your question was answered.")
    view = question.restrictedTraverse('@@answered-message')
    message = view()

    # Send email
    mail_host.secureSend(message, mail_to, mail_from, subject=subject)

