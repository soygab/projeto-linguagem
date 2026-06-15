from django.db import models
from produto.models import Produtos


class Saidas(models.Model):

    produto = models.ForeignKey(
        Produtos,
        on_delete=models.CASCADE
    )

    preco = models.FloatField()

    quantidade = models.IntegerField()

    criado = models.DateTimeField(
        auto_now_add=True
    )

    modificado = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return str(self.produto)