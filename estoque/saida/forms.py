from django import forms
from django.forms import ModelForm
from .models import Saidas

class SaidaForm(ModelForm):

    class Meta:
        model = Saidas
        fields = ['produto', 'quantidade', 'preco']

    def clean_quantidade(self):

        quantidade = self.cleaned_data['quantidade']
        produto = self.cleaned_data.get('produto')

        if produto and quantidade > produto.quantidade:
            raise forms.ValidationError(
                f'Estoque insuficiente. Disponível: {produto.quantidade}'
            )

        return quantidade