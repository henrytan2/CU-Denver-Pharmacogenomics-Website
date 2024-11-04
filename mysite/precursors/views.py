import json

from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import generic
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import AllowAny

from .models import Precursors
from rest_framework.views import APIView
from rest_framework.response import Response


class FetchAllPrecursorsAPI(APIView):
    model = Precursors
    permission_classes = (AllowAny,)

    @method_decorator(name='create', decorator=swagger_auto_schema(auto_schema=None))
    def get(self, request):
        response = list(self.model.objects.all().values())
        return Response(response)

class FetchPrecursorsForDrugsAPI(APIView):
    model = Precursors
    permission_classes = (AllowAny,)

    @swagger_auto_schema(auto_schema=None)
    def post(self, request):
        data = json.loads(request.body)
        precursor_UUIDs = data['precursor_UUIDs']
        precursors = list(self.model.objects.filter(UUID__in=precursor_UUIDs).values())
        return JsonResponse({'precursors': precursors})


class ReceivePrecursorsSelectedAPI(APIView):
    @swagger_auto_schema(auto_schema=None)
    def post(self, request):
        if request.method == 'POST':
            request.session['precursor_UUIDs'] = []
            request.session['precursor_UUIDs'] = self.request.POST.getlist('precursor_UUIDs[]')
            return Response(True)


class PrecursorsTemplateView(generic.TemplateView):
    model = Precursors
    template_name = 'precursor_results.html'


class PrecursorFetchAPIView(APIView):
    model = Precursors

    @swagger_auto_schema(auto_schema=None)
    def post(self, request):
        precursor_UUIDs = request.session['precursor_UUIDs']
        precursors = list(self.model.objects.filter(UUID__in=precursor_UUIDs).values())
        return Response(precursors)
