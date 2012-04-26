import logging

from Products.CMFCore.utils import getToolByName

from siyavula.what import MessageFactory as _
LOGGER = logging.getLogger('siyavula.what: utils')


def get_basic_mailsettings(context):
    import pdb; pdb.set_trace()
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

