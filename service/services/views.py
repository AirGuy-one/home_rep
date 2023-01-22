import json

from django.db.models import Prefetch
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from rest_framework.viewsets import ReadOnlyModelViewSet

from clients.models import Client
from services.models import Subscription
from services.serializers import SubscriptionSerializer


def subscription_api_view(request):
    list_json_response = []

    subscriptions = SubscriptionSerializer(
        Subscription.objects.all().prefetch_related(
            Prefetch(
                'client',
                queryset=Client.objects.all().select_related('user').only('company_name',
                                                                          'user__email')
            )
        ),
        many=True
    ).data
    for subscription in subscriptions:
        json_subscriptions = {
            'id': subscription['id'],
            'client_name': subscription['client_name'],
            'plan_id': subscription['plan_id'],
            'email': subscription['email']
        }
        list_json_response.append(json_subscriptions)

    return HttpResponse(
        json.dumps(list_json_response)
    )
