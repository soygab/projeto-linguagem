from django.shortcuts import render, redirect
from .models import Saidas
from .forms import SaidaForm


def list_saida(request):

    saidas = Saidas.objects.all()

    template_name = 'list_saida.html'

    context = {
        'saidas': saidas,
    }

    return render(request, template_name, context)


def new_saida(request):

    if request.method == 'POST':

        form = SaidaForm(request.POST)

        if form.is_valid():

            produto = form.cleaned_data['produto']
            quantidade = form.cleaned_data['quantidade']

            if quantidade > produto.quantidade:

                form.add_error(
                    'quantidade',
                    f'Estoque insuficiente. Disponível: {produto.quantidade}'
                )

            else:

                form.save(commit=False)

                produto.quantidade = (
                    produto.quantidade - quantidade
                )

                produto.save_base()

                form.save()

                return redirect('saida:list_saida')

    template_name = 'form_saida.html'

    context = {
        'form': form if request.method == 'POST' else SaidaForm(),
    }

    return render(request, template_name, context)


def update_saida(request, pk):

    saida = Saidas.objects.get(pk=pk)

    if request.method == 'POST':

        form = SaidaForm(
            request.POST,
            instance=saida
        )

        if form.is_valid():

            produto = saida.produto

            # devolve a quantidade antiga
            produto.quantidade += saida.quantidade

            nova_quantidade = form.cleaned_data['quantidade']

            if nova_quantidade > produto.quantidade:

                form.add_error(
                    'quantidade',
                    f'Estoque insuficiente. Disponível: {produto.quantidade}'
                )

            else:

                produto.quantidade -= nova_quantidade

                produto.save_base()

                form.save()

                return redirect('saida:list_saida')

    else:

        template_name = 'form_saida.html'

        context = {
            'form': SaidaForm(instance=saida),
            'pk': pk,
        }

        return render(request, template_name, context)

    return render(
        request,
        'form_saida.html',
        {
            'form': form,
            'pk': pk,
        }
    )


def delete_saida(request, pk):

    saida = Saidas.objects.get(pk=pk)

    saida.produto.quantidade = (
        saida.produto.quantidade +
        saida.quantidade
    )

    saida.produto.save()

    saida.delete()

    return redirect('saida:list_saida')