from django.db import models
from django.urls import reverse
from tyres import models as tyres_models


class HomePageModel(models.Model):
    tyre = models.ForeignKey(
        tyres_models.Tyre,
        related_name='tyres_home',
        on_delete=models.PROTECT,
    )
    #tyre_card = models.ForeignKey(
    #    tyres_models.TyreCard,
    #    related_name='tyre_card_home',
    #    on_delete=models.PROTECT,
    #)
    
    def get_absolute_url(self):
        return reverse('homepage:home')
