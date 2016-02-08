from plone.app.testing import applyProfile
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting

class Fixture(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        import collective.piwik.core
        self.loadZCML(package=collective.piwik.core)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'collective.piwik.core:default')

FIXTURE = Fixture()

INTEGRATION_TESTING = IntegrationTesting(
    bases=(FIXTURE,),
    name='collective.piwik.core:Integration',
    )
