from django.contrib import admin
from .models import Concurso, Examinador, Prova, Candidato, Nota

admin.site.register(Concurso)
admin.site.register(Examinador)
admin.site.register(Prova)
admin.site.register(Candidato)
admin.site.register(Nota)

