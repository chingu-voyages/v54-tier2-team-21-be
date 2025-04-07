from django.urls import path
from .views import SendPromptCreateView, GetPromptListView, GetPromptForUserListView

urlpatterns = [
    path('send_prompt/', SendPromptCreateView.as_view(), name="send_prompt"),
    path('prompts/', GetPromptListView.as_view(), name="all_prompts"),
    path('prompts/me/', GetPromptForUserListView.as_view(), name="prompts_for_user"),
]