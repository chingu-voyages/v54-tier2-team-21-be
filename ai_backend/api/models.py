from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator

class Prompt(models.Model):

    GEMINI_MODELS = [
        ("gemini-2.0-flash", "Gemini 2.0 Flash"),
        ("gemini-1.5-pro", "Gemini 1.5 Pro"),
    ]

    User = get_user_model()

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    role = models.CharField(max_length=50)
    prompt_text = models.TextField()
    model = models.CharField(max_length=50, choices=GEMINI_MODELS, default='gemini-1.5-pro')
    prompt_response = models.TextField(null=True, blank=True)
    rating = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(5)])
    saved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Prompt"
        verbose_name_plural = "Prompts"

    def __str__(self):
        return f"{self.role} : {self.prompt_text[:50]}"