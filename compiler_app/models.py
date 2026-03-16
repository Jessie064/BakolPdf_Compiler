from django.db import models


class UploadedFile(models.Model):
    file = models.FileField(upload_to='uploads/')
    filename = models.CharField(max_length=255)
    order = models.IntegerField(default=0)
    session_key = models.CharField(max_length=100, db_index=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', 'uploaded_at']

    def __str__(self):
        return f"{self.filename} (order={self.order})"
