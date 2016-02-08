from zope import schema

from zope.i18nmessageid import MessageFactory
from zope.interface import Interface

_ = MessageFactory('collective.piwik.core')


PIWIK_CODE_ANONYMOUS = u"""
<!-- Piwik -->
<script type="text/javascript">
  var _paq = _paq || [];
  _paq.push(['trackPageView']);
  _paq.push(['enableLinkTracking']);
  (function() {
    var u="%(piwik_server_noscheme)s";
    _paq.push(['setTrackerUrl', u+'piwik.php']);
    _paq.push(['setSiteId', %(piwik_siteid)s]);
    var d=document, g=d.createElement('script'), s=d.getElementsByTagName('script')[0];
    g.type='text/javascript'; g.async=true; g.defer=true; g.src=u+'piwik.js'; s.parentNode.insertBefore(g,s);
  })();
</script>
<noscript><p><img src="%(piwik_server_noscheme)s/piwik.php?idsite=%(piwik_siteid)s" style="border:0;" alt="" /></p></noscript>
<!-- End Piwik Code -->
"""

PIWIK_CODE_LOGGED = u"""
<!-- Piwik -->
<script type="text/javascript">
  var _paq = _paq || [];

  _paq.push(['setUserId', '%(member_id)s']);

  _paq.push(['trackPageView']);
  _paq.push(['enableLinkTracking']);
  (function() {
    var u="%(piwik_server_noscheme)s";
    _paq.push(['setTrackerUrl', u+'piwik.php']);
    _paq.push(['setSiteId', %(piwik_siteid)s]);
    var d=document, g=d.createElement('script'), s=d.getElementsByTagName('script')[0];
    g.type='text/javascript'; g.async=true; g.defer=true; g.src=u+'piwik.js'; s.parentNode.insertBefore(g,s);
  })();
</script>
<noscript><p><img src="%(piwik_server_noscheme)s/piwik.php?idsite=%(piwik_siteid)s" style="border:0;" alt="" /></p></noscript>
<!-- End Piwik Code -->
"""

class IPiwikSettings(Interface):
    """Piwik settings."""

    piwik_enabled = schema.Bool(
            title=_(u"Enabled"),
            description=_(u"Enabled Piwik statistics"),
            required=True,
            default=False,
        )

    piwik_server = schema.TextLine(title=_(u"Piwik server URL"),
                                description=u'Where is your piwik located? e.g. http://demo.piwik.org ',
                                required=True,
                                default = u'',
                                )

    piwik_siteid = schema.TextLine(title=_(u"Piwik site id"),
                                description=u'integer siteId',
                                required=True,
                                default = u'',
                                )

    piwik_key = schema.TextLine(title=_(u"Piwik API key"),
                                description=u'piwik API token auth key, or anonymous if no auth',
                                required=True,
                                default = u'anonymous',
                                )

    piwik_script_anonymous =  schema.Text(title=_(u"Piwik Script (anonymous)"),
                                description=u'The "defaul" piwik code to be injected in the pages',
                                required=True,
                                default = PIWIK_CODE_ANONYMOUS,
                                )

    piwik_script_logged =  schema.Text(title=_(u"Piwik Script (authenticated)"),
                                description=u'The piwik code to be injected in the pages if the '
                                            u'user is authenticated',
                                required=False,
                                default = PIWIK_CODE_LOGGED,
                                )
