from rest_framework import serializers
from ..models import Prompt
from users.models import CustomUser

class PromptSerializer(serializers.ModelSerializer):
    email = serializers.SerializerMethodField()
    class Meta:
        model = Prompt
        fields = ["public_id", "user", "email", "id", "prompt_text", "model", "created_at", "prompt_response"]

    def get_email(self, obj):
        return obj.user.email if obj.user else None

