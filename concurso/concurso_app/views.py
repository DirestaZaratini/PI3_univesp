from django.shortcuts import render, redirect
from .models import Concurso, Examinador
from .forms import ConcursoForm, ExaminadorFormSet
from .models import Prova, Candidato
from .forms import ProvaForm, CandidatoForm
from .models import Nota
from .forms import NotaEliminatoriaForm
from .forms import NotaRestanteForm, NotaRestanteFormSet
from django.shortcuts import get_object_or_404
from django.forms import modelformset_factory

def home(request):
    return render(request, "home.html")


def criar_concurso(request):
    if request.method == "POST":
        form = ConcursoForm(request.POST)
        if form.is_valid():
            concurso = form.save()
            return redirect("cadastrar_examinadores", concurso_id=concurso.id)
    else:
        form = ConcursoForm()
    return render(request, "criar_concurso.html", {"form": form})


def cadastrar_examinadores(request, concurso_id):
    concurso = get_object_or_404(Concurso, id=concurso_id)
    
    if request.method == "POST":
        formset = ExaminadorFormSet(request.POST, queryset=Examinador.objects.none())
        if formset.is_valid():
            for form in formset:
                examinador = form.save(commit=False)
                examinador.concurso = concurso
                examinador.save()
            return redirect("cadastrar_candidatos", concurso_id=concurso.id)
    else:
        # Inicialize o formset sempre vazio
        formset = ExaminadorFormSet(queryset=Examinador.objects.none())

    return render(request, "cadastrar_examinadores.html", {"formset": formset, "concurso": concurso})


def cadastrar_candidatos(request, concurso_id):
    concurso = get_object_or_404(Concurso, id=concurso_id)

    # Define os formsets com quantidade extra baseada no concurso
    ProvaFormSet = modelformset_factory(Prova, form=ProvaForm, extra=concurso.numero_provas)
    CandidatoFormSet = modelformset_factory(Candidato, form=CandidatoForm, extra=concurso.numero_candidatos)

    if request.method == "POST":
        provas_formset = ProvaFormSet(request.POST, prefix="provas")
        candidatos_formset = CandidatoFormSet(request.POST, prefix="candidatos")
        if provas_formset.is_valid() and candidatos_formset.is_valid():
            for form in provas_formset:
                prova = form.save(commit=False)
                prova.concurso = concurso
                prova.save()
            for form in candidatos_formset:
                candidato = form.save(commit=False)
                candidato.concurso = concurso
                candidato.save()
            return redirect("cadastrar_notas_eliminatorias", concurso_id=concurso.id)
    else:
        # Inicializa formsets com extra baseado no concurso
        provas_formset = ProvaFormSet(queryset=Prova.objects.none(), prefix="provas")
        candidatos_formset = CandidatoFormSet(queryset=Candidato.objects.none(), prefix="candidatos")

    return render(request, "cadastrar_candidatos.html", {
        "provas_formset": provas_formset,
        "candidatos_formset": candidatos_formset,
        "concurso": concurso
    })


def cadastrar_notas_eliminatorias(request, concurso_id):
    concurso = get_object_or_404(Concurso, id=concurso_id)
    candidatos = Candidato.objects.filter(concurso=concurso)
    provas = Prova.objects.filter(concurso=concurso, eliminatoria=True)
    examinadores = Examinador.objects.filter(concurso=concurso)

    # Preparar o formset para as notas
    NotaFormSet = modelformset_factory(Nota, form=NotaEliminatoriaForm, extra=0, can_delete=False)

    # Criar instâncias de Nota para combinar provas, candidatos e examinadores
    for prova in provas:
        for candidato in candidatos:
            for examinador in examinadores:
                # Cria a instância apenas se não existir
                nota, created = Nota.objects.get_or_create(
                    candidato=candidato,
                    prova=prova,
                    examinador=examinador,
                    defaults={"nota": 0}  # Valor padrão caso a nota não exista
                )

    if request.method == "POST":
        formset = NotaFormSet(request.POST)
        if formset.is_valid():
            for form in formset:
                if form.cleaned_data.get("nota") is not None:  # Só salva se a nota for preenchida
                    form.save()
            return redirect("cadastrar_notas_restantes", concurso_id=concurso.id)
    else:
        # Pré-carregar o formset com as notas existentes
        formset = NotaFormSet(queryset=Nota.objects.filter(prova__in=provas))

    context = {
        "concurso": concurso,
        "candidatos": candidatos,
        "provas": provas,
        "examinadores": examinadores,
        "formset": formset,
    }
    return render(request, "cadastrar_notas_eliminatorias.html", context)


def cadastrar_notas_restantes(request, concurso_id):
    concurso = get_object_or_404(Concurso, id=concurso_id)

    # Filtrar candidatos aprovados
    candidatos_aprovados = [
        c for c in Candidato.objects.filter(concurso=concurso) if c.aprovado_eliminatoria()
    ]

    # Filtrar provas restantes
    provas_restantes = Prova.objects.filter(concurso=concurso, eliminatoria=False)

    # Obter os examinadores
    examinadores = Examinador.objects.filter(concurso=concurso)

    # Processamento de POST
    if request.method == "POST":
        formset = NotaRestanteFormSet(request.POST)
        if formset.is_valid():
            formset.save()
            return redirect("exibir_resultados", concurso_id=concurso.id)
    else:
        formset = NotaRestanteFormSet(queryset=Nota.objects.none())

    # Construção das tabelas para exibição
    tabelas = []
    for prova in provas_restantes:
        linhas = []
        for candidato in candidatos_aprovados:
            linha = []
            for examinador in examinadores:
                # Preenche cada célula com um campo de nota
                form = NotaRestanteForm(initial={
                    "candidato": candidato,
                    "prova": prova,
                    "examinador": examinador
                })
                linha.append({"form": form["nota"]})
            linhas.append({"candidato": candidato, "linha": linha})
        tabelas.append({"prova": prova, "linhas": linhas})

    # Passar os dados ao template
    return render(request, "cadastrar_notas_restantes.html", {
        "concurso": concurso,
        "tabelas": tabelas,
        "examinadores": examinadores,
        "formset": formset,
    })



def exibir_resultados(request, concurso_id):
    concurso = Concurso.objects.get(id=concurso_id)
    candidatos = [c for c in concurso.candidatos.all() if c.aprovado_eliminatoria()]
    examinadores = Examinador.objects.filter(concurso=concurso)

    # Calculando as notas finais e classificações individuais
    notas_finais = {
        examinador: sorted(
            [(candidato, candidato.nota_final_por_examinador(examinador)) for candidato in candidatos],
            key=lambda x: x[1], reverse=True
        )
        for examinador in examinadores
    }

    # Classificação final por consenso
    classificacao_geral = calcular_classificacao_geral(notas_finais)

    return render(request, "exibir_resultados.html", {
        "concurso": concurso,
        "notas_finais": notas_finais,
        "classificacao_geral": classificacao_geral,
    })

def calcular_classificacao_geral(notas_finais):
    ranking = {}
    for examinador, lista in notas_finais.items():
        for posicao, (candidato, nota) in enumerate(lista):
            ranking[candidato] = ranking.get(candidato, 0) + (1 / (posicao + 1))

    return sorted(ranking.items(), key=lambda x: x[1], reverse=True)

