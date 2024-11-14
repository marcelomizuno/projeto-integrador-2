from django.test import TestCase
from estoque.models import Produto, Categoria, Log, Movimentacao
from django.utils import timezone
from django.contrib.auth.models import User

class ProdutoTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(id=1, username='user', email='user@test.com', password='password')
        self.categoria = Categoria.objects.create(nome='category_test', is_active=False)
        self.produto = Produto.objects.create(nome='product_test', descricao='product_description_test', 
                       categoria=self.categoria, quantidade=5, is_active=True)

    def test_produto_creation(self):
        self.assertTrue(isinstance(self.produto, Produto))
        self.assertEqual(self.produto.__str__(), self.produto.nome)

    def test_quantity_increase(self, quantity=1):
        product_quantity = self.produto.quantidade
        self.produto.incrementar(quantity)
        self.assertEqual(self.produto.quantidade, product_quantity + quantity)

    def test_quantity_decrease(self, quantity=1):
        product_quantity = self.produto.quantidade
        self.produto.decrementar(1)
        self.assertEqual(self.produto.quantidade, product_quantity - quantity)

class CategoriaTest(TestCase):
    def setUp(self):
        self.categoria = Categoria.objects.create(nome='category_test', is_active=True)
    
    def test_categoria_creation(self):
        self.assertTrue(isinstance(self.categoria, Categoria))
        self.assertEqual(self.categoria.__str__(), self.categoria.nome)

class LogTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(id=1, username='user', email='user@test.com', password='password')
        self.log = Log.objects.create(acao='testing', data=timezone.now(), usuario=self.user)
    
    def test_log_creation(self):
        self.assertTrue(isinstance(self.log, Log))
        self.assertEqual(self.log.__str__(), f'{self.log.acao} por {self.log.usuario}')

class MovimentacaoTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='user_test', email='user@test.com', password='test')
        self.categoria = Categoria.objects.create(nome='teste', is_active=True)
        self.produto = Produto.objects.create(nome='test', categoria=self.categoria, descricao='product test', quantidade=10, is_active=True)

    def create_movimentacao(self, tipo, quantidade=5, preco=1, data=timezone.now(), is_active=True):
        return Movimentacao.objects.create(produto=self.produto, tipo=tipo, quantidade=quantidade, preco=preco, data=data, is_active=is_active, usuario=self.user)

    def test_movimentacao_creation(self):
        movimentacao = self.create_movimentacao('entrada')
        self.assertTrue(isinstance(movimentacao, Movimentacao))
        self.assertEqual(movimentacao.__str__(), f'{movimentacao.tipo} de {movimentacao.quantidade} {movimentacao.produto.nome} por {movimentacao.preco}')

    def test_movimentacao_entrada(self):
        quantidade_produtos = self.produto.quantidade
        movimentacao = self.create_movimentacao('entrada')
        self.assertEqual(quantidade_produtos + movimentacao.quantidade, self.produto.quantidade)

    def test_movimentacao_saida(self):
        quantidade_produtos = self.produto.quantidade
        movimentacao = self.create_movimentacao('saida')
        self.assertEqual(quantidade_produtos - movimentacao.quantidade, self.produto.quantidade)
