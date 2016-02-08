import unittest

from zope.component import getMultiAdapter

from Products.CMFCore.utils import getToolByName
from collective.piwik.core.testing import INTEGRATION_TESTING


class RegistryTest(unittest.TestCase):

    layer = INTEGRATION_TESTING

    VARS_TEST_LOGGED = {
        u"piwik_server":           u"https://TEST.COM/",
        u"piwik_siteid":           u"123456",
        u"piwik_key":              u"piwik_key",
        u"piwik_script_anonymous": u"script_anonymous",
        u"piwik_script_logged":    u"script_logged",
    }

    def setUp(self):
        self.portal = self.layer['portal']
        # Set up the akismet settings registry
#        self.loginAsPortalOwner()
#        self.registry = Registry()
#        self.registry.registerInterface(IPiwikSettings)

    def test_piwik_controlpanel_view(self):
        # Test the akismet setting control panel view
        view = getMultiAdapter((self.portal, self.portal.REQUEST),
                               name="piwik-settings")
        view = view.__of__(self.portal)
        self.failUnless(view())

    def test_piwik_in_controlpanel(self):
        # Check that there is an akismet entry in the control panel
        self.controlpanel = getToolByName(self.portal, "portal_controlpanel")
        self.failUnless('collective.piwik.settings' in [a.getAction(self)['id']
                            for a in self.controlpanel.listActions()])

def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)