from django.db import models


class Concurso(models.Model):
    nome = models.CharField(max_length=200)
    data = models.DateField()
    numero_candidatos = models.PositiveIntegerField()
    numero_provas = models.PositiveIntegerField()

    def __str__(self):
        return self.nome

class Examinador(models.Model):
    concurso = models.ForeignKey(Concurso, on_delete=models.CASCADE, related_name="examinadores")
    nome = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.nome} - {self.concurso}"

class Prova(models.Model):
    concurso = models.ForeignKey(Concurso, on_delete=models.CASCADE, related_name="provas")
    nome = models.CharField(max_length=100)
    peso = models.FloatField()
    eliminatoria = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.nome} - {self.concurso}"

class Candidato(models.Model):
    concurso = models.ForeignKey(Concurso, on_delete=models.CASCADE, related_name="candidatos")
    nome = models.CharField(max_length=200)

    def aprovado_eliminatoria(self):
        eliminatorias = Prova.objects.filter(concurso=self.concurso, eliminatoria=True)
        for prova in eliminatorias:
            notas_por_prova = Nota.objects.filter(candidato=self, prova=prova).values_list('nota', flat=True)
            if len([nota for nota in notas_por_prova if nota >= 7]) < 3:
                return False
        return True


    def nota_final_por_examinador(self, examinador):
        provas = Prova.objects.filter(concurso=self.concurso)
        notas = Nota.objects.filter(candidato=self, examinador=examinador, prova__in=provas)

        soma_ponderada = sum(nota.nota * nota.prova.peso for nota in notas)
        peso_total = sum(prova.peso for prova in provas)
        return soma_ponderada / peso_total if peso_total > 0 else 0

    def __str__(self):
        return f"{self.nome} - {self.concurso}"


class Nota(models.Model):
    candidato = models.ForeignKey(Candidato, on_delete=models.CASCADE)
    examinador = models.ForeignKey(Examinador, on_delete=models.CASCADE)
    prova = models.ForeignKey(Prova, on_delete=models.CASCADE)
    nota = models.FloatField()
    

    def __str__(self):
        return f"Nota: {self.nota} - {self.candidato} - {self.prova}"


