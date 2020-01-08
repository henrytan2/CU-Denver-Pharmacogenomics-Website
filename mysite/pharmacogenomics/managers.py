from django.db import models
from .models import SideEffect


class SideEffectManager(models.Manager):

    def get_filtered(side_effect_list):
        return SideEffect.objects.filter(side_effect__in=side_effect_list)