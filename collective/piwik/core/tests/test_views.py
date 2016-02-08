# -*- coding: utf-8 -*-

import unittest

from plone import api
from zope.component import getUtility
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID

from plone.app.testing import logout

from plone.registry.interfaces import IRegistry
from collective.piwik.core.testing import INTEGRATION_TESTING
from collective.piwik.core.interfaces import IPiwikSettings


class ViewTest(unittest.TestCase):

    layer = INTEGRATION_TESTING

    VARS_TEST_ANONYMOUS = {
        u"member_id":              u"",
        u"member_email":           u"",
        u"member_lastname":        u"",
        u"member_firstname":       u"",
        u"piwik_server":           u"https://TEST.COM/",
        u"piwik_server_noscheme":  u"//TEST.COM/",
        u"piwik_server_https":     u"https://TEST.COM/",
        u"piwik_server_http":      u"http://TEST.COM/",
        u"piwik_siteid":           u"123456",
        u"piwik_key":              u"UNAVAILABLE IN JAVASCRIPT",
        u"piwik_apikey":           u"UNAVAILABLE IN JAVASCRIPT",
    }

    VARS_TEST_LOGGED = {
        u"member_id":              u"",
        u"member_email":           u"Myuser@domaintest.com",
        u"member_lastname":        u"",
        u"member_firstname":       u"",
        u"piwik_server":           u"https://TEST.COM/",
        u"piwik_server_noscheme":  u"//TEST.COM/",
        u"piwik_server_https":     u"https://TEST.COM/",
        u"piwik_server_http":      u"http://TEST.COM/",
        u"piwik_siteid":           u"123456",
        u"piwik_key":              u"UNAVAILABLE IN JAVASCRIPT",
        u"piwik_apikey":           u"UNAVAILABLE IN JAVASCRIPT",
    }

    SCRIPT_TEST=u"TEXT;VARIABLES:%s;SPECIALS:!ö$&\\"

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.page = api.content.create(
            container=self.portal, type='Document', id='test-document')
        pmembership = api.portal.get_tool(name='portal_membership')
        self.member=pmembership.getAuthenticatedMember()
        self.VARS_TEST_LOGGED[u"member_id"] = self.member.id
        self.member.setProperties(email=self.VARS_TEST_LOGGED[u"member_email"],
                                  lastname=self.VARS_TEST_LOGGED[u"member_lastname"],
                                  firstname=self.VARS_TEST_LOGGED[u"member_firstname"])

    def test_view_anonymous(self):
        logout()

        # prepare values to test
        script_vars = u"|".join([u"%%(%s)s"%k for k in sorted(self.VARS_TEST_ANONYMOUS.keys())])
        script_values = u"|".join([u"%s"%self.VARS_TEST_ANONYMOUS[k] for k in sorted(self.VARS_TEST_ANONYMOUS.keys())])

        # configure
        registry = getUtility(IRegistry)
        settings = registry.forInterface(IPiwikSettings, prefix="collective.piwik.core")
        settings.piwik_server = self.VARS_TEST_ANONYMOUS[u"piwik_server"]
        settings.piwik_siteid = self.VARS_TEST_ANONYMOUS[u"piwik_siteid"]
        settings.piwik_script_logged = u""
        settings.piwik_script_anonymous = (self.SCRIPT_TEST%script_vars)+"%%"
        settings.piwik_key = u"TO BE IGNORED"

        # Test if the generated (fake) script is in some page
        rendered = (self.SCRIPT_TEST%script_values)+"%"
        self.assertTrue(rendered in self.page())


    def test_views(self):
        # prepare values to test
        script_vars = u"|".join([u"%%(%s)s"%k for k in sorted(self.VARS_TEST_LOGGED.keys())])
        script_values = u"|".join([u"%s"%self.VARS_TEST_LOGGED[k] for k in sorted(self.VARS_TEST_LOGGED.keys())])

        # configure
        registry = getUtility(IRegistry)
        settings = registry.forInterface(IPiwikSettings, prefix="collective.piwik.core")
        settings.piwik_server = self.VARS_TEST_LOGGED[u"piwik_server"]
        settings.piwik_siteid = self.VARS_TEST_LOGGED[u"piwik_siteid"]
        settings.piwik_script_logged = (self.SCRIPT_TEST%script_vars)+"%%"
        settings.piwik_script_anonymous = u""
        settings.piwik_key = u"TO BE IGNORED"

        # Test if the generated (fake) script is in some page
        rendered = (self.SCRIPT_TEST%script_values)+"%"
        self.assertTrue(rendered in self.page())

def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)