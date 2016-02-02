from Testing import ZopeTestCase as ztc

from Products.PloneTestCase import ptc
from Products.PloneTestCase import layer
from Products.Five import zcml
from Products.Five import fiveconfigure

ptc.setupPloneSite(
    extension_profiles=('collective.piwik.core:default', )
)

class PiwikLayer(layer.PloneSite):
    """Configure collective.akismet"""

    @classmethod
    def setUp(cls):
        fiveconfigure.debug_mode = True
        import collective.piwik.core
        zcml.load_config("configure.zcml", collective.piwik.core)
        fiveconfigure.debug_mode = False
        ztc.installPackage("collective.piwik.core", quiet=1)

    @classmethod
    def tearDown(cls):
        pass