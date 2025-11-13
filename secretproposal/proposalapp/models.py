from django.db import models

class AccessCode(models.Model):
    code = models.CharField(max_length=50)
    token = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.code