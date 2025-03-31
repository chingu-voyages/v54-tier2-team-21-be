from django.db import models

class Prompt(models.Model):

    GEMINI_MODELS = [
        ("gemini-2.0-flash", "Gemini 2.0 Flash"),
        ("gemini-1.5-pro", "Gemini 1.5 Pro"),
    ]

    role = models.CharField(max_length=50)
    prompt_text = models.TextField()
    model = models.CharField(max_length=50, choices=GEMINI_MODELS, default='gemini-1.5-pro')
    prompt_response = models.TextField(null=True, blank=True)
    rating = models.IntegerField(default=0)
    saved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.role} : {self.text}"