from rest_framework.response import Response
from rest_framework.views import APIView
from service_objects.services import ServiceOutcome
from rest_framework.permissions import IsAuthenticated

from api.serializers.comment.show import CommentSerializer
from api.services.timer.end import TimerEndService
from api.services.timer.start import TimerStartService


class TimerStartView(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request, *args, **kwargs):
        outcome = ServiceOutcome(TimerStartService, kwargs | {"user": request.user})
        return Response(CommentSerializer(outcome.result).data)


class TimerEndView(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request, *args, **kwargs):
        outcome = ServiceOutcome(TimerEndService, kwargs | {"user": request.user})
        return Response(CommentSerializer(outcome.result).data)
