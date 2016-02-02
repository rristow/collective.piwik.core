import unittest

from zope.component import getMultiAdapter

from plone.registry import Registry

from Products.CMFCore.utils import getToolByName
from Products.PloneTestCase.ptc import PloneTestCase
from collective.piwik.core.tests.layer import PiwikLayer
from collective.piwik.core.interfaces import IPiwikSettings


class RegistryTest(PloneTestCase):

    layer = PiwikLayer

    def afterSetUp(self):
        # Set up the akismet settings registry
        self.loginAsPortalOwner()
        self.registry = Registry()
        self.registry.registerInterface(IPiwikSettings)

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

    def test_validators(self):
        import pdb; pdb.set_trace()
        view = getMultiAdapter((self.portal, self.portal.REQUEST),
                               name="piwik-settings")

def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)