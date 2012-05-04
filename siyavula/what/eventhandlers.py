import logging

from Products.CMFCore.utils import getToolByName

from siyavula.what import MessageFactory as _
from siyavula.what.utils import get_basic_mailsettings

LOGGER = logging.getLogger('siyavula.what: eventhandlers')


def questionAnswered(answer, event):
    """ Send mail when a question is answered.
    """
    wft = getToolByName(answer, 'portal_workflow')
    question = answer.aq_parent
    review_state = wft.getInfoFor(
        question, 'review_state', 'question_workflow')
    if review_state in ['submitted', ]:
        wft.doActionFor(question, 'answer')

    # get the basic mail settings and details
    errors, mail_host, mail_from, mail_to = get_basic_mailsettings(question)

    if errors:
        for error in errors:
            LOGGER.warn(error)
    else:
        # Compose email
        subject = _(u"Your question was answered.")
        view = answer.restrictedTraverse('@@answered-message')
        message = view()

        # Send email
        mail_host.send(message, mail_to, mail_from, subject=subject,
                       charset='utf-8')

