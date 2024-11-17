from rest_framework.generics import ListAPIView
from estoque.models import Produto
from .serializers.produto_serializer import ProdutotSerializer

class ProdutoListView(ListAPIView):
    queryset = Produto.objects.all()
    serializer_class = ProdutotSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.query_params.get('nome')
        if name:
            queryset = queryset.filter(nome__icontains=name)
        return queryset
    