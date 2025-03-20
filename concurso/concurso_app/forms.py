from django import forms
from .models import Concurso, Examinador, Prova, Candidato, Nota
from django.forms import modelformset_factory

class ConcursoForm(forms.ModelForm):
    class Meta:
        model = Concurso
        fields = ["nome", "data", "numero_candidatos", "numero_provas"]

class ExaminadorForm(forms.ModelForm):
    class Meta:
        model = Examinador
        fields = ["nome"]

ExaminadorFormSet = modelformset_factory(Examinador, form=ExaminadorForm, extra=5)

class ProvaForm(forms.ModelForm):
    class Meta:
        model = Prova
        fields = ["nome", "peso", "eliminatoria"]

ProvaFormSet = modelformset_factory(Prova, form=ProvaForm, extra=0)

class CandidatoForm(forms.ModelForm):
    class Meta:
        model = Candidato
        fields = ["nome"]

CandidatoFormSet = modelformset_factory(Candidato, form=CandidatoForm, extra=0)

class NotaEliminatoriaForm(forms.ModelForm):
    class Meta:
        model = Nota
        fields = ["candidato", "examinador", "prova", "nota"]

NotaEliminatoriaFormSet = modelformset_factory(Nota, form=NotaEliminatoriaForm, extra=0)

class NotaRestanteForm(forms.ModelForm):
    class Meta:
        model = Nota
        fields = ["candidato", "examinador", "prova", "nota"]

NotaRestanteFormSet = modelformset_factory(Nota, form=NotaRestanteForm, extra=0)
