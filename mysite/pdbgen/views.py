import json

from django.contrib.sessions.backends.db import SessionStore
from django.http import JsonResponse
from django.shortcuts import render
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods


class IndexView(generic.TemplateView):
    template_name = 'pdbgen_index.html'


@csrf_exempt
@require_http_methods(["POST"])
def store_pdbgen_data(request):
    try:
        data = json.loads(request.body)

        session = SessionStore()
        session.create()

        session['ccid'] = data.get('ccid')
        session['length'] = data.get('length')
        session['pdb'] = data.get('pdb')
        session['positions'] = data.get('positions')

        session.save()

        session_key = session.session_key

        return JsonResponse({"success": True, "session_key": session_key}, status=200)
    except json.JSONDecodeError:
        # Return an error if the JSON is invalid
        return JsonResponse({"success": False, "error": "Invalid JSON"}, status=400)

    except Exception as e:
        # Return an error for any other exception
        return JsonResponse({"success": False, "error": str(e)}, status=500)


@csrf_exempt
@require_http_methods(["GET"])
def read_CCID(request):
    template_name = 'pdbgen_results.html'

    session_key = request.GET.get('session_key')

    session = SessionStore(session_key=session_key)

    ccid = session.get('ccid')
    length = session.get('length')
    pdb = session.get('pdb')
    positions = session.get('positions')
    context = \
        {
            'dash_context':
                {
                    "ccid": {"children": ccid},
                    "length": {"children": length},
                    "pdb": {"children": pdb},
                    "positions": {"children": positions}
                }
        }

    return render(request, template_name=template_name, context=context)
