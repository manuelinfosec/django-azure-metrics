from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from .serializers import UserSerializer, GroupSerializer

import os 
import dotenv
from pathlib import Path

from opentelemetry import trace
from opentelemetry.instrumentation.django import DjangoInstrumentor
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter

from azure.monitor.opentelemetry.exporter import AzureMonitorTraceExporter

# Enable instrymentation in Django
DjangoInstrumentor().instrument()

trace.set_tracer_provider(TracerProvider())
span_processor = BatchSpanProcessor(
    AzureMonitorTraceExporter.from_connection_string(
        os.environ.get("APPLICATIONINSIGHTS_CONNECTION_STRING")
    )
)

trace.get_tracer_provider().add_span_processor(span_processor)

class UserViewSet(viewsets.ModelViewSet):
    """
    This endpiont allows users to be viewed or edited
    """
    queryset = User.objects.all().order_by("-date_joined") 
    serializer_class = UserSerializer

class GroupViewSet(viewsets.ModelViewSet):
    """
    This endpoint allows for groups to be viewed or edited
    """
    queryset = Group.objects.all()
    serialize_class = GroupSerializer