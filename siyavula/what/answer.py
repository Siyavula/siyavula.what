from five import grok
from plone.directives import dexterity, form

from zope import schema
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

from zope.interface import invariant, Invalid

from z3c.form import group, field

from plone.namedfile.interfaces import IImageScaleTraversable
from plone.namedfile.field import NamedImage, NamedFile
from plone.namedfile.field import NamedBlobImage, NamedBlobFile

from plone.app.textfield import RichText

from z3c.relationfield.schema import RelationList, RelationChoice
from plone.formwidget.contenttree import ObjPathSourceBinder

from siyavula.what import MessageFactory as _


class IAnswer(form.Schema, IImageScaleTraversable):
    """
    An answer.
    """

    text = schema.Text(
        title=_(u"Answer"),
        description=_("The answer."),
        required=True,
    )


class Answer(dexterity.Item):
    grok.implements(IAnswer)

    def Title(self):
        return self.text

    def setTitle(self, value):
        pass
