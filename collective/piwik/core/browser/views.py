""" Viewlet """
import logging

from plone import api
from zope.component import getUtility
from ZODB.POSException import ConflictError

from Products.CMFPlone.utils import safe_unicode
from plone.app.layout.viewlets.common import ViewletBase
from plone.registry.interfaces import IRegistry
from collective.piwik.core.utils import DefaultDict
from collective.piwik.core.interfaces import IPiwikSettings

logger = logging.getLogger('collective.piwik.core')

class PiwikPagesTracViewlet(ViewletBase):

    def update(self):
        pass

    def render(self):
        try:
            registry = getUtility(IRegistry)
            settings = registry.forInterface(IPiwikSettings, prefix="collective.piwik.core")

            # get the script
            pmembership = api.portal.get_tool(name='portal_membership')
            if not pmembership.isAnonymousUser() and settings.piwik_script_logged:
                script = settings.piwik_script_logged
                member=pmembership.getAuthenticatedMember()
                # Variables for the member
                script_variables = DefaultDict({
                        u'member_id': safe_unicode(member.getId()),
                        u'member_email': safe_unicode(member.getProperty('email','')),
                        u'member_lastname': safe_unicode(member.getProperty('lastname','')),
                        u'member_firstname': safe_unicode(member.getProperty('firstname','')),
                    })
            else:
                if not settings.piwik_script_anonymous:
                    logger.error(u'There is no piwik script configured in the control panel (anonymous member)')
                    return ""
                else:
                    script = settings.piwik_script_anonymous
                script_variables = DefaultDict()

            # Variables for both scripts
            script_variables.default = u''
            if not settings.piwik_server.endswith(u"/"):
                settings.piwik_server+=u"/"
            script_variables[u'piwik_server'] =  settings.piwik_server
            piwik_server_noscheme = settings.piwik_server
            if "://" in settings.piwik_server:
                piwik_server_noscheme = piwik_server_noscheme.replace(u'https://',u'//').replace(u'http://',u'//')
            script_variables[u'piwik_server_noscheme'] = piwik_server_noscheme
            script_variables[u'piwik_server_https'] =  settings.piwik_server.replace(u'http://',u'https://')
            script_variables[u'piwik_server_http'] =  settings.piwik_server.replace(u'https://',u'http://')
            script_variables[u'piwik_siteid'] =  settings.piwik_siteid
            script_variables[u'piwik_key'] =  u'UNAVAILABLE IN JAVASCRIPT'
            script_variables[u'piwik_apikey'] =  u'UNAVAILABLE IN JAVASCRIPT'

            # Replace the variable values and return
            return script%script_variables
        except (ConflictError, KeyboardInterrupt):
            raise
        except Exception, detail:
            logger.error("error rendering PiwikPagesTracViewlet: %s"%detail)
            raise
