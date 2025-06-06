from django.db import models
from django.contrib.auth import get_user_model

class Lang_Choice(models.TextChoices):
    ENGLISH = 'En', 'English'

class Collection(models.Model):
    '''
    Words collection model
    '''

    name = models.CharField(max_length=30, null=True, blank=False)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='collections', null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    lang = models.CharField (max_length=15, choices=Lang_Choice, default=Lang_Choice.ENGLISH, verbose_name='Language')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'collections'
        verbose_name_plural = 'Collections'