from cms.models import CMSPlugin
from django.db import models


class Form(models.Model):
    """Configuração do Formulário"""
    name = models.CharField(max_length=100)
    action = models.CharField(
        max_length=255,
        help_text="URL para onde o formulário será enviado. Deixe em branco para usar a URL atual.",
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'form_app'
        verbose_name = "Formulário"
        verbose_name_plural = "Formulários"

    def __str__(self) -> str:
        return self.name


class FormSubmission(models.Model):
    """Armazena as submissões do formulário"""
    form = models.ForeignKey(Form, on_delete=models.CASCADE)
    submitted_at = models.DateTimeField(auto_now_add=True)
    data = models.JSONField()

    class Meta:
        app_label = 'form_app'
        verbose_name = "Submissão de Formulário"
        verbose_name_plural = "Submissões de Formulário"


class FormPluginModel(CMSPlugin):
    """Configuração do Formulário"""
    form = models.ForeignKey(Form, on_delete=models.CASCADE)


class Hello(CMSPlugin):
    guest_name = models.CharField(max_length=50, default='Guest')


class FormFieldPluginModel(CMSPlugin):
    """Plugin para campos do formulário"""
    field_type = models.CharField(
        max_length=50,
        choices=[
            ('text', 'Texto'),
            ('email', 'Email'),
            ('number', 'Número'),
            ('textarea', 'Área de Texto'),
            ('select', 'Seleção'),
        ],
        default='text',
    )
    label = models.CharField(max_length=100, help_text="Rótulo do campo")
    name = models.CharField(
        max_length=100, help_text="Nome do campo (usado no HTML)", blank=True
    )
    required = models.BooleanField(
        default=True, help_text="Campo obrigatório?")

    class Meta:
        app_label = 'form_app'
        verbose_name = "Campo do Formulário"
        verbose_name_plural = "Campos do Formulário"

    def __str__(self):
        return self.label


class FormFieldOption(models.Model):
    """Model do formField Select"""
    plugin = models.ForeignKey(
        FormFieldPluginModel,
        on_delete=models.CASCADE,
        related_name="options"
    )
    label = models.CharField(
        max_length=100)
    value = models.CharField(
        max_length=100)

    class Meta:
        app_label = 'form_app'
        verbose_name = "Opção de select"
        verbose_name_plural = "Opções de select"

    def __str__(self):
        return self.label
