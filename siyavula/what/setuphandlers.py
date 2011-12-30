import logging
import transaction
from Products.CMFCore.utils import getToolByName

log = logging.getLogger('siyavula.what-setuphandlers')

def setupWhat(portal):
    """ Create the basic structure and do initial configuration. 
    """
    sections = [
        {'id': 'questions',
        'type': 'siyavula.what.questioncontainer',
        'title': 'Questions',
        'exclude_from_nav': True,
        },
    ]

    for section_dict in sections:
        if not portal.hasObject(section_dict['id']):
            portal.invokeFactory(type_name=section_dict['type'],
                id=section_dict['id'],
                title=section_dict['title'],
                exclude_from_nav=section_dict.get('exclude_from_nav', False),
            ) 
            section = portal._getOb(section_dict['id'])
            transaction.commit()

            wf = getToolByName(portal, 'portal_workflow')
            wf.doActionFor(section,'publish')
            section.reindexObject()
        else:
            section = portal._getOb(section_dict['id'])
        

def setupVarious(context):
    if context.readDataFile('siyavula.what-marker.txt') is None:
        return
    site = context.getSite()
    setupWhat(site)
