from plone.app.registry.browser import controlpanel
from z3c.form.browser.textlines import TextLinesFieldWidget
from z3c.form.interfaces import WidgetActionExecutionError
from zope.interface import Invalid
from z3c.form import form, button
from Products.statusmessages.interfaces import IStatusMessage

from collective.piwik.core.interfaces import IPiwikSettings
from collective.piwik.core.interfaces import PIWIK_CODE_ANONYMOUS
from collective.piwik.core.interfaces import PIWIK_CODE_LOGGED

from zope.i18nmessageid import MessageFactory
_ = MessageFactory('plone')


class PiwikSettingsSettingsEditForm(controlpanel.RegistryEditForm):
    id = "PiwikControlPanel"
    schema_prefix = "collective.piwik.core"
    schema = IPiwikSettings
    label = u"Piwik Settings"
    description = u"Token login authentication settings."

    def updateActions(self):
        super(PiwikSettingsSettingsEditForm, self).updateActions()
        self.actions['reset'].addClass("context")

    def updateFields(self):
        super(PiwikSettingsSettingsEditForm, self).updateFields()
        self.fields['piwik_script_anonymous'].widgetFactory = TextLinesFieldWidget
        self.fields['piwik_script_logged'].widgetFactory = TextLinesFieldWidget

    def updateWidgets(self):
        super(PiwikSettingsSettingsEditForm, self).updateWidgets()
        self.widgets['piwik_script_anonymous'].rows = 12
        self.widgets['piwik_script_logged'].rows = 12

    def applyChanges(self, data):
        super(PiwikSettingsSettingsEditForm, self).applyChanges(data)
        if data["piwik_server"]:
            if not data["piwik_server"].endswith('/'):
                data["piwik_server"]+=u"/"
        else:
            raise WidgetActionExecutionError("piwik_server", Invalid(u"Please informe the URI"))

        if data["piwik_siteid"]:
            try:
                int(data["piwik_siteid"])
            except ValueError, e:
                raise WidgetActionExecutionError('piwik_siteid', Invalid(u"Is not a valid number"))

    def resetScripts(self, data):
        super(PiwikSettingsSettingsEditForm, self).applyChanges(data)
        data["piwik_script_anonymous"] = PIWIK_CODE_ANONYMOUS
        data["piwik_script_logged"] = PIWIK_CODE_LOGGED

    @button.buttonAndHandler(_(u"Save"), name='save')
    def handleSave(self, action):
        super(PiwikSettingsSettingsEditForm, self).handleSave(self, action)

    @button.buttonAndHandler(_(u"Cancel"), name='cancel')
    def handleCancel(self, action):
        super(PiwikSettingsSettingsEditForm, self).handleCancel(self, action)

    @button.buttonAndHandler(_(u"Reset Scripts"), name='reset')
    def handleReset(self, action):
        data, errors = self.extractData()
        self.resetScripts(data)
        self.applyChanges(data)
        IStatusMessage(self.request).addStatusMessage(
            u"Reset of scripts done.",
            "info")
        self.request.response.redirect(self.request.getURL())

class PiwikControlPanelView(controlpanel.ControlPanelFormWrapper):
    form = PiwikSettingsSettingsEditForm

