from django.urls import path
from .views import SendPromptCreateView, GetPromptListView, GetPromptForUserListView, export_prompt, SendEmailCreateView

urlpatterns = [
    path('send_prompt/', SendPromptCreateView.as_view(), name="send_prompt"),
    path('prompts/', GetPromptListView.as_view(), name="all_prompts"),
    path('prompts/me/', GetPromptForUserListView.as_view(), name="prompts_for_user"),
    path('prompts/export/<uuid:public_id>/email/', SendEmailCreateView.as_view(), name="send_email_prompt"),
    path('prompts/export/<uuid:public_id>/<str:format>/', export_prompt, name="export_prompt"),
]