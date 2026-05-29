from django.shortcuts import render

def index(request):
    template_name = 'index.html'
    context = {
        'mensagem': 'Bem-vindo ao sistemas de Estoque'
    }
    return render(request, template_name, context)
