from rest_framework.response import Response
from rest_framework.views import APIView
from service_objects.services import ServiceOutcome
from rest_framework.permissions import IsAuthenticated

from api.serializers.subtask.get import SubTaskShowSerializer
from api.services.subtask.create import SubTaskCreateService


class SubTaskCreateView(APIView):
    permission_classes = (IsAuthenticated, )

    def post(self, request, *args, **kwargs):
        outcome = ServiceOutcome(SubTaskCreateService, request.data)
        return Response(
            SubTaskShowSerializer(outcome.result).data
        )
