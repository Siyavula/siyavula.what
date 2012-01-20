import logging

from Products.CMFCore.utils import getToolByName

from siyavula.what import MessageFactory as _
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


def get_basic_mailsettings(context):
    errors = []

    member_id = context.Creator()
    pmt = getToolByName(context, 'portal_membership')
    owner = pmt.getMemberById(member_id)
    mail_to = owner.getProperty('email')
    if mail_to is None or len(mail_to) < 1:
        errors.append('The owner (%s) has no email address!' % \
            owner.getProperty('fullname'))

    mail_host = getToolByName(context, 'MailHost')
    if not mail_host:
        errors.append('Add a portal mail host.')

    portal_url = getToolByName(context, 'portal_url')
    portal = portal_url.getPortalObject()
    mail_from = portal.getProperty('email_from_address')
    if not mail_from:
        errors.append('Add a portal email address.')

    return errors, mail_host, mail_from, mail_to
