from zope.interface import alsoProvides
from zope import schema
from plone.directives import form
from plone.autoform.interfaces import IFormFieldProvider

from siyavula.what import MessageFactory as _


class IAllowQuestionsBehavior(form.Schema):
    """
       Marker/Form interface for Allow Questions Behavior
    """
    form.fieldset(
        'settings',
        label=_(u'Settings'),
        fields=['allowQuestions',],
        )

    allowQuestions = schema.Bool(
           title = _(u"Allow questions"),
           description=_(u"Enables the adding of questions and aswers."),
           default=False,
           required=False,
           )

    # -*- Your Zope schema definitions here ... -*-

alsoProvides(IAllowQuestionsBehavior,IFormFieldProvider)
