from django.shortcuts import render, redirect
from .models import Produtos
from .forms import ProdutoForm

def list_produto(request):
    produtos = Produtos.objects.all()
    template_name = 'list_produto.html'
    context = {
        'produtos': produtos
    }
    return render(request, template_name, context)

def new_produto(request):
    print('-->',request.method)
    if request.method == 'POST':
        form = ProdutoForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('produto:list_produto')
    else:
        template_name = 'form_produto.html'
        context = {
            'form': ProdutoForm()
        }
        return render(request, template_name, context)

def update_produto(request, pk):
    produto = Produtos.objects.get(id=pk)
    if request.method == 'POST':
        form = ProdutoForm(request.POST, instance=produto)
        if form.is_valid():
            form.save()
        return redirect('produto:list_produto')
    else:
        template_name = 'form_produto.html'
        context = {
            'form': ProdutoForm(instance=produto)
        }
        return render(request, template_name, context)

def delete_produto(request, pk):
    produto = Produtos.objects.get(id=pk)
    produto.delete()
    return redirect('produto:list_produto')