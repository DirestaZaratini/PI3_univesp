"""
URL configuration for setup project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from concurso_app import views

urlpatterns = [
    path('', views.home, name='home'),
    path('criar-concurso/', views.criar_concurso, name='criar_concurso'),
    path('cadastrar-examinadores/<int:concurso_id>/', views.cadastrar_examinadores, name='cadastrar_examinadores'),
    path('cadastrar-candidatos/<int:concurso_id>/', views.cadastrar_candidatos, name='cadastrar_candidatos'),
    path('cadastrar-notas-eliminatorias/<int:concurso_id>/', views.cadastrar_notas_eliminatorias, name='cadastrar_notas_eliminatorias'),
    path('cadastrar-notas-restantes/<int:concurso_id>/', views.cadastrar_notas_restantes, name='cadastrar_notas_restantes'),
    path('exibir-resultados/<int:concurso_id>/', views.exibir_resultados, name='exibir_resultados'),
]



