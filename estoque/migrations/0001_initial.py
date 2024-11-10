# Generated by Django 5.1.2 on 2024-10-13 23:45

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Categoria",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("nome", models.CharField(max_length=255)),
                ("is_active", models.BooleanField(default=False)),
            ],
            options={
                "verbose_name": "Categoria",
                "verbose_name_plural": "Categorias",
            },
        ),
        migrations.CreateModel(
            name="Log",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("acao", models.CharField(max_length=255)),
                ("data", models.DateTimeField(auto_now_add=True)),
                (
                    "usuario",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Log",
                "verbose_name_plural": "Logs",
            },
        ),
        migrations.CreateModel(
            name="Produto",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("nome", models.CharField(max_length=255)),
                ("descricao", models.TextField()),
                ("codigo_de_barras", models.CharField(max_length=255)),
                ("quantidade_minima", models.IntegerField()),
                ("quantidade_atual", models.IntegerField()),
                ("is_active", models.BooleanField(default=False)),
                (
                    "categoria",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="estoque.categoria",
                    ),
                ),
            ],
            options={
                "verbose_name": "Produto",
                "verbose_name_plural": "Produtos",
            },
        ),
        migrations.CreateModel(
            name="Movimentacao",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "tipo",
                    models.CharField(
                        choices=[("entrada", "Entrada"), ("saida", "Saída")],
                        max_length=255,
                    ),
                ),
                ("quantidade", models.IntegerField()),
                ("preco", models.DecimalField(decimal_places=2, max_digits=10)),
                ("data", models.DateTimeField(auto_now_add=True)),
                ("is_active", models.BooleanField(default=False)),
                (
                    "usuario",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "produto",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="estoque.produto",
                    ),
                ),
            ],
            options={
                "verbose_name": "Movimentação",
                "verbose_name_plural": "Movimentações",
            },
        ),
    ]