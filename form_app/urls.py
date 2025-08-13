from django.urls import path
from . import views

app_name = "form_app"

urlpatterns = [
    path("submit/<int:form_id>/", views.submit_form, name="submit_form"),
]

