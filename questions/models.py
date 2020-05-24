from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

class Question(models.Model):
    title = models.CharField(max_length=128)
    content = models.TextField()
    date = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, related_name="questions", on_delete=models.DO_NOTHING)
    #zmienie na on_delete=SET() nieznany
    #dodać sygnał który zmienia ilość pytań użytkownika

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="answers")
    content = models.TextField()
    author = models.ForeignKey(User, related_name="answers", on_delete=models.DO_NOTHING)
    date = models.DateTimeField(default=timezone.now, blank=True)

class Stats(models.Model):
    user = models.OneToOneField(User ,related_name="stats", on_delete=models.CASCADE)

    @receiver(post_save, sender=User)
    def create_stats(sender, instance, created, **kwargs):
        if created:
            Stats.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_stats(sender, instance, **kwargs):
        instance.stats.save()