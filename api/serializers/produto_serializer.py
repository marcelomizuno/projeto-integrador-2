from rest_framework import serializers
from estoque.models import Produto


class ProdutotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produto
        fields = "__all__"