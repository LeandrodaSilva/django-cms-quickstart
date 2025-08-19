from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from form_app.models import Hello, Form, FormPluginModel, FormFieldPlugin
from django.utils.translation import gettext_lazy as _

@plugin_pool.register_plugin
class HelloPlugin(CMSPluginBase):
    model = Hello
    name = _("Hello Plugin")
    render_template = "hello_plugin.html"
    cache = False

    class Meta:
        verbose_name = "Hello Plugin"
        verbose_name_plural = "Hello Plugins"

    def render(self, context, instance, placeholder):
        context.update({'instance': instance})
        return context

@plugin_pool.register_plugin
class FormAppPlugin(CMSPluginBase):
    model = FormPluginModel
    name = _("Form App Plugin")
    render_template = "form_plugin.html"
    cache = False
    allow_children = True  # permite adicionar plugins filhos
    # child_classes = ["TextPlugin", "LinkPlugin", ...]  # opcional: restrinja tipos permitidos

    class Meta:
        verbose_name = "Form App Plugin"
        verbose_name_plural = "Form App Plugins"

    def render(self, context, instance, placeholder):
        context.update({'instance': instance})
        return context

@plugin_pool.register_plugin
class FormFieldPlugin(CMSPluginBase):
    model = FormFieldPlugin
    name = _("Form Field Plugin")
    render_template = "form_field_plugin.html"
    cache = False

    class Meta:
        verbose_name = "Form Field Plugin"
        verbose_name_plural = "Form Field Plugins"

    def render(self, context, instance, placeholder):
        context.update({'instance': instance})
        return context