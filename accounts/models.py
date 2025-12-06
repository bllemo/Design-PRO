from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class DesignRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    title = models.CharField(max_length=200, verbose_name="Название заявки")
    description = models.TextField(verbose_name="Описание помещения")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Заявка на дизайн"
        verbose_name_plural = "Заявки на дизайн"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} — {self.user.username}"

    def get_absolute_url(self):
        return reverse('request-detail', kwargs={'pk': self.pk})