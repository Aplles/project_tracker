from rest_framework import serializers
from models_app.models import Subtask


class SubTaskShowSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subtask
        fields = (
            'title',
            'description',
            'is_done',
            'created_at'
        )
