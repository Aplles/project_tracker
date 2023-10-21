from rest_framework import serializers

from api.serializers.project.show import ProjectSerializer
from models_app.models import UserProject


class UserProjectListSerializer(serializers.ModelSerializer):
    project = ProjectSerializer(read_only=True)

    class Meta:
        model = UserProject
        fields = ('project',)
