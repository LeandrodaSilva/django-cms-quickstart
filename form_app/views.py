from django.http import HttpResponseNotAllowed, HttpResponseBadRequest
from django.shortcuts import redirect, get_object_or_404
from django.views.decorators.csrf import csrf_protect

from .models import Form, FormSubmission


@csrf_protect
def submit_form(request, form_id: int):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])  # apenas POST

    form = get_object_or_404(Form, pk=form_id)

    # Extrai dados do POST (token CSRF é validado e não é persistido)
    payload = {}
    for key, values in request.POST.lists():
        if key in ("csrfmiddlewaretoken", "next"):
            continue
        if len(values) == 1:
            payload[key] = values[0]
        else:
            payload[key] = values

    if not payload:
        return HttpResponseBadRequest("Nenhum dado recebido")

    FormSubmission.objects.create(form=form, data=payload)

    # Redireciona para a página anterior ou raiz
    next_url = request.POST.get("next") or request.META.get("HTTP_REFERER") or "/"
    return redirect(next_url)
