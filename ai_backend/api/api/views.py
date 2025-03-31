from rest_framework.response import Response
from rest_framework import status, generics
from ..models import Prompt
from .serializers import PromptSerializer
import os
import requests

API_KEY = os.getenv('API_KEY')

class SendPromptCreateView(generics.CreateAPIView):
    serializer_class = PromptSerializer

    def create(self, request, *args, **kwargs):
        print(f"API_KEY: {API_KEY}")
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        prompt_instance = serializer.save()

        model = prompt_instance.model

        # api_url = f'https://generativelanguage.googleapis.com/v1/models/gemini-2.0-flash:generateContent?key={API_KEY}'
        api_url = f'https://generativelanguage.googleapis.com/v1/models/{model}:generateContent?key={API_KEY}'
        payload = {
            "contents": [
                {
                    "role": "user",
                    "parts": [
                        {"text": prompt_instance.prompt_text}
                    ]
                }
            ]
        }
        headers = {"Content-Type": "application/json"}

        response = requests.post(api_url, json=payload, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
        else:
            data = {"error": "Failed to fetch data", "status_code": response.status_code}

        response_text = data.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "No response text")

        prompt_instance.prompt_response = response_text
        prompt_instance.save()


        return Response({
            "api_response_text": response_text,
            "api_response": data
        }, status=status.HTTP_200_OK)
    

class GetPromptListView(generics.ListAPIView):
    serializer_class = PromptSerializer
    queryset = Prompt.objects.all()
    