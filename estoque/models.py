from django.db import models
from django.contrib.auth.models import User

class Produto(models.Model):
    nome = models.CharField(max_length=255)
    categoria = models.ForeignKey('Categoria', on_delete=models.CASCADE)
    descricao = models.TextField()
    codigo_de_barras = models.CharField(max_length=255)
    quantidade_minima = models.IntegerField()
    quantidade_atual = models.IntegerField()
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.nome
    
    class Meta:
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'
    
    def incrementar(self, quantidade):
        self.quantidade_atual += quantidade
        self.save()

    def decrementar(self, quantidade):
        self.quantidade_atual -= quantidade
        self.save()

class Movimentacao(models.Model):
    TIPO_CHOICES = [
        ('entrada', 'Entrada'),
        ('saida', 'Saída'),
    ]

    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=255, choices=TIPO_CHOICES)
    quantidade = models.IntegerField()
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    data = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.tipo} de {self.quantidade} {self.produto.nome} por {self.preco}'
    
    class Meta:
        verbose_name = 'Movimentação'
        verbose_name_plural = 'Movimentações'

    def save(self, *args, **kwargs):
        if self.tipo == 'entrada':
            self.produto.incrementar(self.quantidade)
        elif self.tipo == 'saida':
            self.produto.decrementar(self.quantidade)
        super().save(*args, **kwargs)

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