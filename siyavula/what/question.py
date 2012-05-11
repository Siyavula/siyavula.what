from five import grok
from plone.directives import dexterity, form
from plone.indexer import indexer
from plone.uuid.interfaces import IUUID

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


class IQuestion(form.Schema, IImageScaleTraversable):
    """
    A question about a piece of content.
    """

    text = schema.Text(
        title=_(u"Question"),
        description=_("The question."),
        required=True,
    )

    relatedContent = RelationChoice(
        title=_(u'label_content_item', default=u'Related Content'),
        source=ObjPathSourceBinder(
          object_provides='Products.CMFCore.interfaces._content.IContentish'),
        required=False,
    )


@indexer(IQuestion)
def relatedContentUID(obj):
    uuid = IUUID(obj.relatedContent.to_object)
    return uuid
grok.global_adapter(relatedContentUID, name="relatedContentUID")


class Question(dexterity.Container):
    grok.implements(IQuestion)

    def Title(self):
        return self.text

    def setTitle(self, value):
        pass

    @property
    def answers(self):
        return self.getAnswers()

    def getAnswers(self):
        obs = self.objectValues()
        return [ob for ob in obs if ob.portal_type == 'siyavula.what.answer']
