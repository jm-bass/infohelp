from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import AuthenticationForm
from .models import User, Perfil
import re
from django.contrib.auth.forms import PasswordChangeForm

class CadastroForm(forms.ModelForm):
    username = forms.CharField(
        min_length=4,
        max_length=30,
        label="Usuário:",
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        help_text="O nome de usuário deve ter entre 4 e 30 caracteres e pode conter letras, números e _. "
    )
    
    email = forms.EmailField(
        label="Email:",
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
        help_text="Informe um email válido."
    )

    password = forms.CharField(
        label="Senha:",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        min_length=8,
        help_text="A senha deve ter pelo menos 8 caracteres, incluindo uma letra maiúscula, uma minúscula e um número."
    )

    password_confirm = forms.CharField(
        label="Confirme a senha:",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if not re.match(r'^[\w]+$', username):
            raise forms.ValidationError("O nome de usuário só pode conter letras, números e sublinhados (_).")
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Este nome de usuário já está em uso.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Este email já está cadastrado.")
        return email

    def clean_password(self):
        password = self.cleaned_data.get("password")
        if not re.search(r'[A-Z]', password):
            raise forms.ValidationError("A senha deve conter pelo menos uma letra maiúscula.")
        if not re.search(r'[a-z]', password):
            raise forms.ValidationError("A senha deve conter pelo menos uma letra minúscula.")
        if not re.search(r'\d', password):
            raise forms.ValidationError("A senha deve conter pelo menos um número.")
        return password

    def clean_password_confirm(self):
        password = self.cleaned_data.get("password")
        password_confirm = self.cleaned_data.get("password_confirm")
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("As senhas não coincidem.")
        return password_confirm
    

class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Usuário:",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        label="Senha:",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )


class EditarPerfilForm(forms.ModelForm):
    username = forms.CharField(
        label="Nome de usuário:",
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=False  # Torna o campo opcional
    )

    class Meta:
        model = Perfil
        fields = ['cidade', 'estado', 'data_nascimento', 'telefone', 'avatar']
        widgets = {
            'cidade': forms.TextInput(attrs={'class': 'form-control'}),
            'estado': forms.TextInput(attrs={'class': 'form-control'}),
            'data_nascimento': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control'}),
            'avatar': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Preenche o campo username com o valor atual do usuário
        if self.instance and self.instance.usuario:
            self.fields['username'].initial = self.instance.usuario.username

        # Torna todos os campos opcionais
        for field in self.fields:
            self.fields[field].required = False


class AlterarSenhaForm(PasswordChangeForm):
    old_password = forms.CharField(
        label="Senha atual:",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )


class SolicitacaoProfessorForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = []  # Nenhum campo será exibido, apenas o botão de solicitação