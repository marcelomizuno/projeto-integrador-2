import csv
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.http import HttpResponse
from django.http import JsonResponse
from .models import Produto, Categoria, Log
from .forms import CustomUserCreationForm, CustomUserChangeForm, ProdutoForm
from .utils import registrar_log
from django.db.models import Sum


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
    else:
        form = AuthenticationForm()
    
    return render(request, 'login.html', {'form': form})


def password_reset_confirm(request, uidb64=None, token=None, *arg, **kwargs):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        print('user is not None and default_token_generator.check_token(user, token)')
        if request.method == 'POST':
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                login(request, user)
                return redirect('dashboard')
        else:
            form = SetPasswordForm(user)
    else:
        form = None

    return render(request, 'password/password_reset_confirm.html', {
        'form': form,
        'uid': uidb64,
        'token': token
    })


@login_required
def dashboard(request):
    users = User.objects.all()
    produtos = Produto.objects.all()
    categorias = Categoria.objects.all()
    logs = Log.objects.all().order_by('-data')
    total_estoque = produtos.aggregate(Sum('quantidade'))['quantidade__sum']

    return render(request, 'dashboard.html', {
        'users': users,
        'produtos': produtos,
        'categorias': categorias,
        'logs': logs,
        'total_estoque': total_estoque
        })


@login_required
def get_user_data(request, user_id):
    try:
        user = User.objects.get(pk=user_id)
        user_data = {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'username': user.username,
            'email': user.email,
        }
        return JsonResponse(user_data)
    except User.DoesNotExist:
        return JsonResponse({'error': 'Usuário não encontrado'}, status=404)


@login_required
def save_user(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        if user_id:
            # Atualizar usuário existente
            user = User.objects.get(pk=user_id)
            form = CustomUserChangeForm(request.POST, instance=user)
            acao = f'Atualizou o usuário {user.username}'
        else:
            # Criar novo usuário
            form = CustomUserCreationForm(request.POST)
            acao = 'Criou um novo usuário'
        
        if form.is_valid():
            user = form.save(commit=False)
            if not user_id:
                user.set_password(form.cleaned_data['password1'])
                acao = f'Criou o usuário {user.username}'
            user.save()
            registrar_log(request.user, acao)
            return JsonResponse({'success': True, 'user_id': user.id})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    return JsonResponse({'success': False, 'error': 'Método não permitido'}, status=405)


@login_required
def delete_user(request, user_id):
    try:
        user = get_object_or_404(User, pk=user_id)
        username = user.username
        user.delete()
        registrar_log(request.user, f'Deletou o usuário {username}')
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@login_required
def export_users(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="funcionarios.csv"'

    writer = csv.writer(response)
    writer.writerow(['Nome', 'Sobrenome', 'Nome de Usuário', 'Email'])

    users = User.objects.all().values_list('first_name', 'last_name', 'username', 'email')
    for user in users:
        writer.writerow(user)

    return response


@login_required
def save_product(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        new_category_name = request.POST.get('new_category')
        
        if new_category_name:
            # Criar nova categoria
            categoria, created = Categoria.objects.get_or_create(nome=new_category_name)
            request.POST = request.POST.copy()
            request.POST['categoria'] = categoria.id
            acao = f'Criou a categoria {categoria.nome}'
        
        if product_id:
            # Atualizar produto existente
            product = get_object_or_404(Produto, pk=product_id)
            form = ProdutoForm(request.POST, instance=product)
            acao = f'Atualizou o produto {product.nome}'
        else:
            # Criar novo produto
            form = ProdutoForm(request.POST)
            acao = 'Criou um novo produto'
        
        if form.is_valid():
            product = form.save(commit=False)
            if not product_id:
                acao = f'Criou o produto {product.nome}'
            product.save()
            registrar_log(request.user, acao)
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    return JsonResponse({'success': False, 'error': 'Método não permitido'}, status=405)


@login_required
def get_product_data(request, product_id):
    try:
        product = get_object_or_404(Produto, pk=product_id)
        product_data = {
            'name': product.nome,
            'category': product.categoria.id,
            'description': product.descricao,
            'quantity': product.quantidade,
        }
        return JsonResponse(product_data)
    except Produto.DoesNotExist:
        return JsonResponse({'error': 'Produto não encontrado'}, status=404)
    

@login_required
def delete_product(request, product_id):
    try:
        product = get_object_or_404(Produto, pk=product_id)
        product_name = product.nome
        product.delete()
        registrar_log(request.user, f'Deletou o produto {product_name}')
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@login_required
def update_quantity(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        action = request.POST.get('action')
        quantity = request.POST.get('quantity')

        if not quantity:
            return JsonResponse({'success': False, 'error': 'Quantidade não fornecida'}, status=400)

        try:
            quantity = int(quantity)
        except ValueError:
            return JsonResponse({'success': False, 'error': 'Quantidade inválida'}, status=400)

        product = get_object_or_404(Produto, pk=product_id)

        if action == 'increase':
            product.incrementar(quantity)
            acao = f'Entrada de {quantity} unidades do produto {product.nome}'
        elif action == 'decrease':
            product.decrementar(quantity)
            acao = f'Saída de {quantity} unidades do produto {product.nome}'

        registrar_log(request.user, acao)
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'error': 'Método não permitido'}, status=405)   


@login_required
def export_products(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="produtos.csv"'

    writer = csv.writer(response)
    writer.writerow(['Nome', 'Categoria', 'Descrição', 'Quantidade'])

    products = Produto.objects.all().values_list('nome', 'categoria__nome', 'descricao', 'quantidade')
    for product in products:
        writer.writerow(product)

    return response


def custom_error_view(request, exception=None, status_code=500, message="Erro Interno do Servidor"):
    context = {
        'status_code': status_code,
        'message': message
    }
    return render(request, 'error.html', context, status=status_code)