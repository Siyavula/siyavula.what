from zope.interface import implements

from Products.Archetypes.Widget import BooleanWidget
from Products.Archetypes.public import BooleanField

from archetypes.schemaextender.field import ExtensionField
from archetypes.schemaextender.interfaces import ISchemaExtender

import logging
LOG = logging.getLogger('AllowQuestionsExtender')

class _AllowQuestionsExtensionField(ExtensionField, BooleanField): pass

class AllowQuestionsExtender(object):
    implements(ISchemaExtender)

    fields = [
        _AllowQuestionsExtensionField(
            "allowQuestions",
            default = False,
            widget = BooleanWidget(
                label=u"Allow questions",
                description=u"Allow questions on this content.",
            ),
            schemata='settings',
        ),
    ]

    def __init__(self, context):
        self.context = context

    def getFields(self):
        return self.fields

