from five import grok
from plone.directives import dexterity, form

from plone.namedfile.interfaces import IImageScaleTraversable
from plone.app.textfield import RichText

from siyavula.what import MessageFactory as _


class IAnswer(form.Schema, IImageScaleTraversable):
    """
    An answer.
    """

    text = RichText(
        title=_(u"Answer"),
        description=_("The answer."),
        required=True,
    )


class Answer(dexterity.Item):
    grok.implements(IAnswer)
