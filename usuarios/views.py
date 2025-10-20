from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .forms import CadastroForm, LoginForm, EditarPerfilForm, SolicitacaoProfessorForm

from django.contrib.admin.views.decorators import staff_member_required

from django.contrib import messages

from .models import Perfil  # Importe o modelo Perfil
from django.contrib.auth.decorators import login_required, permission_required

from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm



def cadastro(request):
    if request.method == "POST":
        form = CadastroForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.save()

            # Cria um perfil para o usuário recém-criado
            Perfil.objects.create(usuario=user)

            # Loga o usuário automaticamente após o cadastro
            login(request, user)  # Usando a função login do Django

            return redirect("inicio")  # Redireciona para a página inicial
    else:
        form = CadastroForm()
    return render(request, "cadastro.html", {"form": form})

# Renomeie a função login para fazer_login
def fazer_login(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            # login(request, user)  # Usando a função login do Django
            return redirect("inicio")
    else:
        form = AuthenticationForm()
    return render(request, "login.html", {"form": form})


@login_required
def perfil(request):
    usuario = request.user
    perfil = get_object_or_404(Perfil, usuario=usuario)

    return render(request, "perfil.html", {"perfil": perfil})

@login_required
def editar_perfil(request):
    perfil, created = Perfil.objects.get_or_create(usuario=request.user)
    
    if request.method == "POST":
        form = EditarPerfilForm(request.POST, request.FILES, instance=perfil)
        if form.is_valid():
            # Salva os dados do perfil
            perfil = form.save()

            # Atualiza o username do usuário
            novo_username = form.cleaned_data.get('username')
            if novo_username:
                perfil.usuario.username = novo_username
                perfil.usuario.save()

            messages.success(request, "Perfil atualizado com sucesso!")
            return redirect("perfil")
    else:
        form = EditarPerfilForm(instance=perfil)
    
    return render(request, "editar_perfil.html", {"form": form, "perfil": perfil})


@login_required
def alterar_senha(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            # Atualiza a sessão do usuário para evitar logout
            update_session_auth_hash(request, user)
            messages.success(request, 'Sua senha foi alterada com sucesso!')
            return redirect('perfil')  # Redireciona para a página de perfil
        else:
            messages.error(request, 'Por favor, corrija os erros abaixo.')
    else:
        form = PasswordChangeForm(request.user)
    
    return render(request, 'alterar_senha.html', {'form': form})



@login_required
def solicitar_permissao_professor(request):
    perfil = request.user.perfil
    if request.method == 'POST':
        form = SolicitacaoProfessorForm(request.POST, instance=perfil)
        if form.is_valid():
            perfil.solicitacao_professor = True
            perfil.save()
            messages.success(request, 'Sua solicitação foi enviada com sucesso!')
            return redirect('inicio')  # Redirecionar para a página inicial ou outra página
    else:
        form = SolicitacaoProfessorForm(instance=perfil)
    return render(request, 'solicitar_permissao_professor.html', {'form': form})


@staff_member_required
def gerenciar_solicitacoes_professor(request):
    solicitacoes = Perfil.objects.filter(solicitacao_professor=True)

    if request.method == 'POST':
        usuario_id = request.POST.get('usuario_id')
        acao = request.POST.get('acao')
        perfil = Perfil.objects.get(usuario_id=usuario_id)

        if acao == 'aprovar':
            perfil.usuario.is_staff = True  # Concede permissão de professor
            perfil.solicitacao_professor = False
            perfil.usuario.save()
            perfil.save()
        elif acao == 'rejeitar':
            perfil.solicitacao_professor = False
            perfil.save()

    return render(request, 'gerenciar_solicitacoes_professor.html', {'solicitacoes': solicitacoes})