from zope.interface import alsoProvides
from zope import schema
from plone.directives import form
from plone.autoform.interfaces import IFormFieldProvider
from z3c.form.interfaces import IEditForm, IAddForm

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
           title = _(u"label_allowquestions", default=u"Allow questions"),
           required=False,
           default=False,
           )

    form.omitted('allowQuestions')
    form.no_omit(IEditForm, 'allowQuestions')
    form.no_omit(IAddForm, 'allowQuestions')

alsoProvides(IAllowQuestionsBehavior,IFormFieldProvider)
