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

            form.save(commit=False)

            # PQT = Produto Quantidade
            form.cleaned_data['produto'].quantidade \
            = form.cleaned_data['produto'].quantidade \
            - form.cleaned_data['quantidade']

            form.cleaned_data['produto'].save_base()

            form.save()

        return redirect('saida:list_saida')

    else:

        template_name = 'form_saida.html'

        context = {
            'form': SaidaForm(),
        }

        return render(request, template_name, context)


def update_saida(request, pk):

    saida = Saidas.objects.get(pk=pk)

    if request.method == 'POST':

        form = SaidaForm(request.POST, instance=saida)

        if form.is_valid():

            # devolve quantidade antiga ao estoque
            saida.produto.quantidade += saida.quantidade

            # verifica se há estoque suficiente
            if form.cleaned_data['quantidade'] > saida.produto.quantidade:

                form.add_error(
                    'quantidade',
                    f'Estoque insuficiente. Disponível: {saida.produto.quantidade}'
                )

            else:

                saida.produto.quantidade -= form.cleaned_data['quantidade']

                saida.produto.save()

                form.save()

                return redirect('saida:list_saida')

    else:

        template_name = 'form_saida.html'

        context = {
            'form': SaidaForm(instance=saida),
            'pk': pk,
        }

        return render(request, template_name, context)

    return render(request, 'form_saida.html', {
        'form': form,
        'pk': pk,
    })


def delete_saida(request, pk):

    saida = Saidas.objects.get(pk=pk)

    # devolve ao estoque
    saida.produto.quantidade = (
        saida.produto.quantidade +
        saida.quantidade
    )

    saida.produto.save()

    saida.delete()

    return redirect('saida:list_saida')
