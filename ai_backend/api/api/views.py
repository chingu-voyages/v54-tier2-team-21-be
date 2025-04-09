from rest_framework.response import Response
from rest_framework import status, generics
from ..models import Prompt
from .serializers import PromptSerializer, EmailSerializer
import os
import requests
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.contrib.auth.models import AnonymousUser
from django.shortcuts import get_object_or_404
from ..utils.export import generate_csv, generate_pdf, send_email
from django.http import HttpResponse

API_KEY = os.getenv('API_KEY')

class SendPromptCreateView(generics.CreateAPIView):
    serializer_class = PromptSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        prompt_instance = serializer.save(user=request.user if request.user and not isinstance(request.user, AnonymousUser) else None)

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

        public_id = prompt_instance.public_id

        prompt_instance.prompt_response = response_text
        prompt_instance.save()


        return Response({
            "public_id": public_id,
            "api_response_text": response_text,
            "api_response": data
        }, status=status.HTTP_200_OK)
    

class GetPromptListView(generics.ListAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = PromptSerializer
    queryset = Prompt.objects.all()


class GetPromptForUserListView(generics.ListAPIView):
    serializer_class = PromptSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Prompt.objects.filter(user=self.request.user)
    
    
class SendEmailCreateView(generics.CreateAPIView):
    serializer_class = EmailSerializer

    def post(self, request, public_id):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        prompt = get_object_or_404(Prompt, public_id=public_id)
        prompt_data = PromptSerializer(prompt).data

        prompt_text = prompt_data['prompt_text']
        prompt_response = prompt_data['prompt_response']
        send_email(email, prompt_text, prompt_response)

        return Response({
            "msg": "Email was sent successfully!",
            "email": email,
        }, status=status.HTTP_200_OK)



def export_prompt(request, public_id, format):
    prompt = get_object_or_404(Prompt, public_id=public_id)

    if format == 'csv':
        csv_data = generate_csv(prompt=prompt)
        response = HttpResponse(csv_data, content_type="text/csv")
        response['Content-Disposition'] = f'attachment; filename="prompt_{public_id}.csv"'
        return response
    
    if format == "pdf":
        pdf_data = generate_pdf(prompt=prompt)
        response = HttpResponse(pdf_data, content_type="application/pdf")
        response['Content-Disposition'] = f'attachment; filename="prompt_{public_id}.pdf"'
        return response
