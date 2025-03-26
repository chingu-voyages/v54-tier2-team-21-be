from django.db import models

class Prompt(models.Model):
    role = models.CharField(max_length=50)
    prompt_text = models.TextField()
    prompt_response = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.role} : {self.text}"