from django.shortcuts import render, redirect, get_object_or_404
from .models import Curso, Salvos, Aula
from .forms import CursoForm, SalvosForm, AulaForm
from django.contrib.auth.decorators import login_required, permission_required
# Create your views here.

def index(request):

    return render(request, "index.html")

def login(request):

    return render(request, "login.html")


def inicio(request):
    context = {
        "cursos" : Curso.objects.all()
    }

    return render(request, "inicio.html", context)




#CRUD de Cursos

def listar_cursos(request):
    cursos = Curso.objects.all()
    
    curso = Curso.objects.all()

    if request.method == "POST":
        cate = request.POST.get('categoria')
        cursos = Curso.objects.filter(categoria__contains=cate)

    return render(request, "listar_cursos.html", {'cursos': cursos, 'curso' : curso})


def detalhes_curso(request, curso_id):

    cursos = get_object_or_404(Curso, pk=curso_id)

    aulas = Aula.objects.all()


    return render(request, "pag_curso.html", {'curso': cursos,'aula': aulas})


@login_required
@permission_required('infohelp.criar_curso', raise_exception=True)
def criar_curso(request):
    if request.method == "POST":
        form = CursoForm(request.POST, request.FILES)
        if form.is_valid():
            curso = form.save(commit=False)
            curso.usuario = request.user
            curso.save()
            return redirect('listar_cursos')
        else:
            form = CursoForm()
    else:
        form = CursoForm()
    
    return render(request, "criar_curso.html", {'form': form})


@permission_required('infohelp.editar_curso', raise_exception=True)
def editar_curso(request, curso_id):
    curso = get_object_or_404(Curso, id=curso_id)

    context = {
        "curso" : curso,
        "form" : CursoForm(instance=curso),
    }

    if request.method == 'POST':
        form = CursoForm(request.POST, request.FILES, instance=curso)
        if form.is_valid():
            form.save()
            return redirect('listar_cursos')
        else:
            context["form"] = form
    
    return render(request, "editar_curso.html", context)



def excluir_curso(request, curso_id):
    context = {
        "curso": get_object_or_404(Curso, id=curso_id)
    }

    if request.method == "POST":
        context["curso"].delete()
        return redirect('listar_cursos')
    else:
        return render(request, "excluir_curso.html", context)



#CRUD de Aulas

def criar_aula(request, curso_id):
    curso = get_object_or_404(Curso, id=curso_id)
    if request.method == "POST":
        form = AulaForm(request.POST, request.FILES)
        if form.is_valid():
            aula = form.save(commit=False)
            aula.curso = curso
            aula.save()
            return redirect('detalhes_curso', curso_id=curso.id)
        else:
            form["form"] = form

    else:
        form = AulaForm()

    return render(request, 'criar_aula.html', {'form': form, 'curso': curso})

def editar_aula(request, aula_id, curso_id):
    aula = get_object_or_404(Aula, id=aula_id)
    curso = get_object_or_404(Curso, id=curso_id)

    context = {
        "aula" : aula,
        "curso" : curso,
        "form" : AulaForm(instance=aula),
    }

    if request.method == 'POST':
        form = AulaForm(request.POST, instance=aula)
        if form.is_valid():
            form.save()
            return redirect('detalhes_aula', curso.id, aula.id)
        else:
            context["form"] = form
    
    return render(request, "editar_aula.html", context)


def detalhes_aula(request, curso_id, aula_id):
    aulas = Aula.objects.all()

    aula = get_object_or_404(Aula, id=aula_id)
    curso = get_object_or_404(Curso, id=curso_id)
    
    return render(request, "exibir_aula.html", {'aulas' : aulas, 'curso' : curso, 'aula' : aula})



def excluir_aula(request, curso_id, aula_id):
    aula = get_object_or_404(Aula, id=aula_id)
    curso = get_object_or_404(Curso, id=curso_id)

    context = {
        "curso": get_object_or_404(Curso, id=curso_id),
        "aula": get_object_or_404(Aula, id=aula_id)
    }

    if request.method == "POST":
        context["aula"].delete()
        return redirect('detalhes_curso', curso.id)
    else:
        return render(request, "excluir_aula.html", context)


@login_required
def biblioteca(request):
    salvos = Salvos.objects.filter(usuario=request.user)
    return render(request, 'biblioteca.html', {'salvos': salvos})


def busca(request):
    busca = request.POST.get('busca')
    cursos = Curso.objects.filter(descricao__contains=busca)

    return render(request, 'busca.html', {'cursos': cursos})


def perfil(request):

    return render(request, "perfil.html")

def editar_perfil(request):

    return render(request, "editar_perfil.html")

@login_required
def criar_salvos(request):
    if request.method == 'POST':
        form = SalvosForm(request.POST)
        if form.is_valid():
            salvos = form.save(commit=False)
            salvos.usuario = request.user  # Associar a salvos ao usuário logado
            salvos.save()
            form.save_m2m()  # Salvar a relação de muitos para muitos com músicas
            return redirect('listar_cursos')  # Redireciona para uma página de sucesso
    else:
        form = SalvosForm()

    return render(request, 'criar_salvos.html', {'form': form})