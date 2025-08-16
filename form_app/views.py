import logging
import requests
from django.http import HttpResponseNotAllowed, HttpResponseBadRequest, HttpResponseServerError, JsonResponse
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
    next_url = request.POST.get(
        "next") or request.META.get("HTTP_REFERER") or "/"
    return redirect(next_url)


logger = logging.getLogger(__name__)


@csrf_protect
def get_ibge_select_data(request):
    if request.method != "GET":
        return HttpResponseNotAllowed(["GET"])
    uf = request.GET.get('uf')
    try:
        if uf:
            url = f'https://servicodados.ibge.gov.br/api/v1/localidades/estados/{uf}/municipios'
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            municipios = response.json()

            data = [{'id': m['id'], 'nome': m['nome']} for m in municipios]
            data.sort(key=lambda x: x['nome'])

        else:
            url = 'https://servicodados.ibge.gov.br/api/v1/localidades/estados'
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            estados = response.json()

            data = [{'sigla': e['sigla'], 'nome': e['nome']} for e in estados]
            data.sort(key=lambda x: x['nome'])

        return JsonResponse(data, safe=False)

    except requests.exceptions.RequestException as e:
        logger.error(f"Erro na conexão com IBGE: {str(e)}")
        return HttpResponseServerError(f"Erro na conexão com o IBGE: {str(e)}")
    except (KeyError, ValueError) as e:
        logger.error(f"Erro no processamento: {str(e)}")
        return HttpResponseServerError(f"Erro no processamento dos dados: {str(e)}")
