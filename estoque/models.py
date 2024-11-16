from django.db import models
from django.contrib.auth.models import User

class Produto(models.Model):
    nome = models.CharField(max_length=255)
    categoria = models.ForeignKey('Categoria', on_delete=models.CASCADE)
    descricao = models.TextField()
    quantidade = models.IntegerField()
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.nome
    
    class Meta:
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'
    
    def incrementar(self, quantidade):
        self.quantidade += quantidade
        self.save()

    def decrementar(self, quantidade):
        self.quantidade -= quantidade
        self.save()


class Categoria(models.Model):
    nome = models.CharField(max_length=255)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.nome
    
    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'


class Log(models.Model):
    acao = models.CharField(max_length=255)
    data = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.acao} por {self.usuario}'
    
    class Meta:
        verbose_name = 'Log'
        verbose_name_plural = 'Logs'