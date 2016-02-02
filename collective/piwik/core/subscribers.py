"""Event subscribers"""
import logging

from zope.component import adapter
from zope.component import getUtility

from plone.registry.interfaces import IRecordModifiedEvent
from collective.piwik.core.interfaces import IPiwikSettings
from Products.CMFCore.utils import getToolByName
from plone.registry.interfaces import IRegistry

log = logging.getLogger('collective.piwik.core')


@adapter(IPiwikSettings, IRecordModifiedEvent)
def updateTrackingCode(obj, event):
    ptool = getToolByName(obj, "portal_properties")
    registry = getUtility(IRegistry)
    settings = registry.forInterface(IPiwikSettings)
    if not settings.piwik_server.endswith('/'):
        settings.piwik_server+='/'
    log.info('webstats_js code updated')
